from flask import Flask, request, jsonify, make_response
import random

# Initialize the Flask app
app = Flask(__name__)

# Defining game rooms with initial states
# TODO: Make sure you can connect to 'n' number of game rooms
#       Which move it is?
#       How much time is left?
#       Has the game ended?
#       Poll for move ending from Client B
#       Poll for game ending from client C
#       Send safe coordinates to Client A (from client C) at the start of each move
game_rooms = {
    "101": {"clients": [], "safe_coordinates": None},
    "102": {"clients": [], "safe_coordinates": None},
    "103": {"clients": [], "safe_coordinates": None},
    "104": {"clients": [], "safe_coordinates": None},
}

# Endpoint to connect a client to a game room
@app.route('/connect', methods=['POST'])
def connect():
    data = request.json
    client = data.get("client")
    game_room = data.get("game_room")

    # Validate input and add client to the game room if there is space
    if not client or not game_room:
        return "Client or game room information missing.", 400

    if game_room in game_rooms and len(game_rooms[game_room]["clients"]) < 3:
        game_rooms[game_room]["clients"].append(client)
        response = make_response(f"{client} connected to room {game_room}")
        response.set_cookie("client_id", client)
        return response
    else:
        return "Game room full or not found.", 400

# Endpoint to acknowledge safe coordinates by Client A
# TODO: write the spec in the README file so that 
#       the clients can work according to your decisions
@app.route('/acknowledge_safe_coordinates/<game_room>', methods=['POST'])
def acknowledge_safe_coordinates(game_room):
    data = request.json
    client = data.get("client")

    # Ensure game room exists and acknowledgment is from Client A
    if game_room in game_rooms and client == 'A' and game_rooms[game_room]["safe_coordinates"]:
        return jsonify({"message": "Start game for Client B and Client C"}), 200
    return "Safe coordinates not acknowledged or not Client A.", 400

# Endpoint to get the current game state for a specific game room
# FIXME: what is a game state?????
@app.route('/get_game_state/<game_room>', methods=['GET'])
def get_game_state(game_room):
    if game_room in game_rooms:
        state = {
            "safe_coordinates": game_rooms[game_room]["safe_coordinates"],
            "clients": game_rooms[game_room]["clients"]
        }
        return jsonify(state), 200
    else:
        return "Game room not found.", 404

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
