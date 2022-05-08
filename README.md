## Installation

1. Download github-repo
2. Install Flask with the following command: `pip install Flask`

## Routes

Route | Type | Description
--- | --- | ---
/send | `POST` | Submit a message to a defined recipient
/messages/new | `GET` | Fetch new messages
/messages/all?id=<id-id> | `GET` | Fetch all messages in range according
to start and stop index
/delete?id=<id,id> | `DELETE` | Delete a single or multiple messages

## How to use the service
Execute `main.py`:  
`python3 main.py`

Submit a message to a defined recipient:  
`$ curl -i -H "Content-Type: application/json" -X POST -d '{"name":"Johanna", "message": "Hej Johanna!"}' http://localhost:5000/send `

Fetch new messages:  
`$ curl -i http://localhost:5000/messages/new `

Fetch all messages:  
`$ curl -i http://localhost:5000/messages/all `

Delete a single message with id 1:  
`$ curl -X DELETE http://localhost:5000/delete?id=1 `

Delete multiple messages with id 1 and 2:  
`$ curl -X DELETE http://localhost:5000/delete?id=1,2 `
