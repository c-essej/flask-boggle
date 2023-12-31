from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game
    board = game.board
    newgame = {"gameId": game_id, "board": board}
    # return_obj = {"gameId": game_id, "board": board, 'games': games}
    #

    newgame_jsonify = jsonify(newgame)
    # return_obj_jsonify = jsonify(return_obj)
    # print('***newgame=', newgame)
    # print('***games=', games)
    # TODO: check if the new game is in games
    return newgame_jsonify
    # return return_obj_jsonify


@app.post("/api/score-word")
def valid_word():
    """check to see if the word is on the board/valid
       get JSON {"word":"CAT", "id": "asdasd"}
    """
    # breakpoint()
    word = request.json['word']
    id = request.json['id']
    game = games[id]
    word_on_board = game.check_word_on_board(word)
    word_in_word_list = game.check_word(word)

    if not word_in_word_list:
        return jsonify({"result": 'not-word'})
    elif not word_on_board:
        return jsonify({"result": "not-on-board"})
    else:
        game.play_and_score_word(word)
        return jsonify({"result": "ok"})
