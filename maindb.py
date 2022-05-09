from flask import Flask, request, abort
from datetime import datetime, time
import sqlite3 as sql

app = Flask(__name__)

con = sql.connect('msg_database.db')
con.execute('CREATE TABLE IF NOT EXISTS messages (ID INTEGER PRIMARY KEY AUTOINCREMENT,'
            + 'read NULL, name TEXT, messege TEXT)')
con.close

@app.route('/messages/all', methods=['GET'])
def get_all_messages():
    msg = []
    try:
        con = sql.connect('msg_database.db')
        c =  con.cursor() # cursor
        # read question : SQLite index start from 1 (see index.html)
        if request.args:
            id = request.args.get('id')
            messageRange = id.split('-')
            for i in range(int(messageRange[0]), int(messageRange[1]) + 1):
                query = "Select * FROM messages WHERE id = {0} ORDER BY read".format(i)
                c.execute(query)
                for row in c:
                    msg.append(row)
                    con.commit() # apply changes
            return str(msg)
        query = "Select * FROM messages ORDER BY read"
        c.execute(query)
        for row in c:
            msg.append(row)
            con.commit()
        return str(msg)
    except con.Error as err: # if error
        return "An error occured: " + str(err)
    finally:
        con.close() # close the connection

@app.route('/messages/new', methods=['GET'])
def get_new_messages():
    now = datetime.now()
    timeNow = datetime.time(now)
    dt_string = timeNow.strftime("%H:%M:%S")
    msg = []
    try:
        con = sql.connect('msg_database.db')
        c =  con.cursor() # cursor
        # read question : SQLite index start from 1 (see index.html)
        query = "UPDATE messages SET read = '" + dt_string + "' WHERE read IS NULL;"
        c.execute(query)
        querySelect = "Select * FROM messages WHERE read = '" + dt_string + "';"
        c.execute(querySelect)
        for row in c:
            print(row)
            msg.append(row)
            con.commit()
        con.commit() # apply changes
        return str(msg)
    except con.Error as err: # if error
        return "An error occured: " + str(err)
    finally:
        con.close() # close the connection

@app.route('/send', methods=['POST'])
def send_message():
    if not request.json or not 'name' in request.json:
        abort(400)

    name = request.json["name"]
    message = request.json["message"]

    try:
        con = sql.connect('msg_database.db')
        c =  con.cursor() # cursor
        # insert data
        c.execute("INSERT INTO messages (name, messege) VALUES (?,?)",
            (name, message))
        con.commit() # apply changes
        return "Message sent to: " + name, 201
    except con.Error as err: # if error
        # then display the error in 'database_error.html' page
        return "An error occured: " + str(err)
    finally:
        con.close() # close the connection

@app.route('/delete', methods=['DELETE'])
def delete_messages():
    args = request.args.get('id')
    ids = args.split(',')
    try:
        con = sql.connect('msg_database.db')
        c =  con.cursor() # cursor
        # insert data
        for id in ids:
            query = "DELETE FROM messages WHERE id = {0}".format(id)
            c.execute(query)
        con.commit() # apply changes
        return "Deleted messages with id: " + args, 201
    except con.Error as err: # if error
        # then display the error in 'database_error.html' page
        return "An error occured: " + str(err)
    finally:
        con.close() # close the connection

if __name__ == '__main__':
    app.run(debug=True)
