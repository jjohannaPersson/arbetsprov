from flask import Flask, request, abort
from datetime import datetime, time
import sqlite3 as sql

app = Flask(__name__)

# Connect to database and create table
con = sql.connect('msg_database.db')
con.execute('CREATE TABLE IF NOT EXISTS messages (ID INTEGER PRIMARY KEY AUTOINCREMENT,'
            + 'read NULL, name TEXT, messege TEXT)')
con.close

@app.route('/messages/all', methods=['GET'])
def get_all_messages():
    # current time
    now = datetime.now()
    timeNow = datetime.time(now)
    dt_string = timeNow.strftime("%H:%M:%S")
    # list of selected messages
    msg = []
    try:
        con = sql.connect('msg_database.db') # connect
        c =  con.cursor() # cursor
        if request.args:
            id = request.args.get('id') # get start and stop index
            messageRange = id.split('-') # split args
            # loop through the range
            for i in range(int(messageRange[0]), int(messageRange[1]) + 1):
                # update new messages, set read to current time
                queryUpdate = "UPDATE messages SET read = '" + dt_string + "' WHERE read IS NULL AND ID = {0};".format(i)
                c.execute(queryUpdate) # exectue query
                # select the messages according o start and stop index
                query = "Select * FROM messages WHERE id = {0}".format(i)
                c.execute(query) # exectue query
                # loop through the result and append each row to list
                for row in c:
                    msg.append(row)
                con.commit() # apply changes
            # sort list by time
            msg.sort(key=lambda tup: tup[1])
            # return list
            return str(msg)
        # update new messages, set read to current time
        queryUpdate = "UPDATE messages SET read = '" + dt_string + "' WHERE read IS NULL;"
        c.execute(queryUpdate)# exectue query
        # select all messages if no index range, order by the time the message was fetched
        query = "Select * FROM messages ORDER BY read"
        c.execute(query) # exectue query
        # loop through the result and append each row to list
        for row in c:
            msg.append(row)
        con.commit() # apply changes
        # return list
        return str(msg)
    except con.Error as err: # if error
        return "An error occured: " + str(err)
    finally:
        con.close() # close the connection

@app.route('/messages/new', methods=['GET'])
def get_new_messages():
    # current time
    now = datetime.now()
    timeNow = datetime.time(now)
    dt_string = timeNow.strftime("%H:%M:%S")
    # list of selected messages
    msg = []
    try:
        con = sql.connect('msg_database.db') # connect
        c =  con.cursor() # cursor
        # update new messages, set read to current time
        query = "UPDATE messages SET read = '" + dt_string + "' WHERE read IS NULL;"
        c.execute(query)# exectue query
        # select all the newly updated messages
        querySelect = "Select * FROM messages WHERE read = '" + dt_string + "';"
        c.execute(querySelect)# exectue query
        # loop through the result and append each row to list
        for row in c:
            msg.append(row)
        con.commit() # apply changes
        # return list
        return str(msg)
    except con.Error as err: # if error
        return "An error occured: " + str(err)
    finally:
        con.close() # close the connection

@app.route('/send', methods=['POST'])
def send_message():
    # need to have a defined recipient
    if not request.json or not 'name' in request.json:
        abort(400)

    # get name and message
    name = request.json["name"]
    message = request.json["message"]

    try:
        con = sql.connect('msg_database.db') # connect
        c =  con.cursor() # cursor
        # insert name and message to database
        c.execute("INSERT INTO messages (name, messege) VALUES (?,?)",
            (name, message))
        con.commit() # apply changes
        # return message
        return "Message: " + message + ", was sent to: " + name, 201
    except con.Error as err: # if error
        return "An error occured: " + str(err)
    finally:
        con.close() # close the connection

@app.route('/delete', methods=['DELETE'])
def delete_messages():
    args = request.args.get('id') # get ids
    ids = args.split(',') # split args with ids
    try:
        con = sql.connect('msg_database.db') # connect
        c =  con.cursor() # cursor
        # loop through ids
        for id in ids:
            # delete the messages
            query = "DELETE FROM messages WHERE id = {0}".format(id)
            c.execute(query) # execute query
        con.commit() # apply changes
        # return message
        return "Deleted messages with id: " + args, 201
    except con.Error as err: # if error
        return "An error occured: " + str(err)
    finally:
        con.close() # close the connection

if __name__ == '__main__':
    app.run(debug=True)
