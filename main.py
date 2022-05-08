from flask import Flask, jsonify, request, abort
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/messages/all', methods=['GET'])
def get_all_messages():
    with open('data/messages.json') as f:
            messages = json.load(f)
    msg = []

    if request.args:
        id = request.args.get('id')
        messageRange = id.split('-')
        for i in range(int(messageRange[0]), int(messageRange[1]) + 1):
            for message in messages:
                if message["read"] is None:
                    pass
                elif message["id"] == i:
                    msg.append(message)

        return jsonify({'messages': msg})

    for message in messages:
        if message["read"] is not None:
            msg.append(message)
    return jsonify({'messages': msg})

@app.route('/messages/new', methods=['GET'])
def get_new_messages():
    try:
        with open('data/messages.json') as f:
                messages = json.load(f)

        newMsg = []

        for message in messages:
            if message["read"] is None:
                newMsg.append(message)

        return jsonify({'messages': newMsg})
    finally:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        for message in newMsg:
            message["read"] = dt_string
            with open('data/messages.json', 'w') as outfile:
                json.dump(messages, outfile,
                                indent=4,
                                separators=(',',': '))

@app.route('/send', methods=['POST'])
def new_message():
    with open('data/messages.json') as f:
            messages = json.load(f)

    if not request.json or not 'name' in request.json:
        abort(400)

    if len(messages) > 0:
        id = messages[-1]["id"] + 1
    else:
        id = 1

    message = {
        'id': id,
        'read': None,
        'name': request.json["name"],
        'message': request.json["message"]
    }
    messages.append(message)
    with open('data/messages.json', 'w') as outfile:
        json.dump(messages, outfile,
                        indent=4,
                        separators=(',',': '))

    return jsonify({'message': message}), 201

@app.route('/delete', methods=['DELETE'])
def delete_messages():
    args = request.args.get('id')
    ids = args.split(',')
    for id in ids:
        for message in messages:
            if message["id"] == int(id):
                messages.remove(message)
                with open('data/messages.json', 'w') as outfile:
                    json.dump(messages, outfile,
                                    indent=4,
                                    separators=(',',': '))

    return jsonify({'result': "Deleted message with id: " + args})

if __name__ == '__main__':
    app.run(debug=True)
