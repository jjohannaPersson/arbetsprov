from flask import Flask, jsonify, request, abort
import json

app = Flask(__name__)

with open('data/allmessages.json') as f:
        allmessages = json.load(f)

with open('data/newmessages.json') as f:
        newmessages = json.load(f)

@app.route('/messages/all', methods=['GET'])
def get_all_messages():
    return jsonify({'messages': allmessages})

@app.route('/messages/new', methods=['GET'])
def get_new_messages():
    try:
        with open('data/newmessages.json') as f:
                newmessages = json.load(f)
        return jsonify({'messages': newmessages})
    finally:
        for message in newmessages:
            allmessages.append(message)
            with open('data/allmessages.json', 'w') as outfile:
                json.dump(allmessages, outfile,
                                indent=4,
                                separators=(',',': '))
            with open('data/newmessages.json', 'w') as outfile:
                json.dump([], outfile)

@app.route('/send', methods=['POST'])
def new_message():
    with open('data/allmessages.json') as f:
            allmessages = json.load(f)

    with open('data/newmessages.json') as f:
            newmessages = json.load(f)

    if not request.json or not 'name' in request.json:
        abort(400)

    if len(newmessages) > 0:
        id = newmessages[-1]["id"] + 1
    elif len(allmessages) > 0:
        id = allmessages[-1]["id"] + 1
    else:
        id = 1

    message = {
        'id': id,
        'name': request.json["name"],
        'message': request.json["message"]
    }
    newmessages.append(message)
    with open('data/newmessages.json', 'w') as outfile:
        json.dump(newmessages, outfile,
                        indent=4,
                        separators=(',',': '))

    return jsonify({'message': message}), 201

# @app.route('/delete/<int:id>', methods=['DELETE'])
# def delete_message(id):
#     message = [message for message in allmessages if message["id"] == id]
#     if len(message) == 0:
#         abort(400)
#     allmessages.remove(message[0])
#     with open('data/allmessages.json', 'w') as outfile:
#         json.dump(allmessages, outfile,
#                         indent=4,
#                         separators=(',',': '))
#     return jsonify({'result': "Deleted message with id: " + str(message[0]["id"])})

@app.route('/delete', methods=['DELETE'])
def delete_messages():
    args = request.args.get('id')
    ids = args.split(',')
    for id in ids:
        for message in allmessages:
            if message["id"] == int(id):
                allmessages.remove(message)
                with open('data/allmessages.json', 'w') as outfile:
                    json.dump(allmessages, outfile,
                                    indent=4,
                                    separators=(',',': '))

    return jsonify({'result': "Deleted message with id: " + args})

if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app
