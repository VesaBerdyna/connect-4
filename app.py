from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from db.game_db import GameDB
from models.game import Game
from models.player_factory import PlayerFactory
from exceptions.game_existment import GameExistment
from exceptions.empty_game import EmptyGame

app = Flask(__name__)
app.secret_key = "secret_key"

game_db = GameDB("GAME")
game_db.init_db()


@app.route("/")
def start_game():
    return render_template("start_game.html")


@app.route("/modes")
def choose_mode():
    return render_template("choose_mode.html")


@app.route("/popup", methods=["POST", "GET"])
def popup():
    if request.method == "GET":
        session["mode"] = request.args.get("mode")
        mode = session["mode"]
        return render_template("popup.html", mode=mode)
    if request.method == "POST":
        mode = request.form["mode"]
        player_one_name = request.form["player_one"]
        player_two_name = request.form["player_two"]
        print(player_one_name, player_two_name)

        player_one, player_two = PlayerFactory.create_player(
            mode, player_one_name=player_one_name, player_two_name=player_two_name
        )

        session["player_one"] = player_one.to_dict()
        session["player_two"] = player_two.to_dict()

        return redirect(url_for("create_game"))
    return render_template("popup.html")


@app.route("/game")
def create_game():
    global game
    player_one = PlayerFactory.create_player_from_json(session["player_one"])
    player_two = PlayerFactory.create_player_from_json(session["player_two"])

    game = Game(player_one=player_one, player_two=player_two)
    game.set_player_dot()
    game.set_players()
    game.start()
    game_id = game.get_id()
    game_db.create_game(game_id, game.get_game_state())
    return render_template("game.html", game_id=game_id)


@app.route("/board", methods=["GET"])
def board():
    game_id = request.args.get("game_id")
    if game_id is None:
        EmptyGame

    game_state = game_db.get_game_state(game_id)
    if game_state is None:
        GameExistment

    print("gameeeeeeeeeeeeeeeeeeeeeeeeeeee:", game_state)

    response = jsonify(
        {
            "game_state": game_state[1],
        }
    )
    return response


@app.route("/move", methods=["POST"])
def move():
    print("in move routeeeeeeeeeeee")
    if request.method == "POST":
        col = int(request.get_json()["column"])
        # col = int(request.get_json()["column"]) - 1
        print("coooooooooool", col)
        print("typeeeeeee", type(col))
        print(game.get_game_state())
        res = game.play(player=game.current_turn, col=col)
        game_state = game.get_game_state()
        print(game_state)
        game_db.update_game(game.get_id(), game_state)
    return game_state

if __name__ == "__main__":
    app.run(debug=True)
