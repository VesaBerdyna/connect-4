from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for)

from db.game_db import GameDB
from exceptions.empty_game import EmptyGame
from exceptions.game_existment import GameExistment
from models.game import Game
from models.player_factory import PlayerFactory


class ConnectFour:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = "secret_key"
        self.game_db = GameDB("GAME")
        self.game_db.init_db()

    def start_game(self):
        @self.app.route("/")
        def start():
            return render_template("start_game.html")

    def choose_mode(self):
        @self.app.route("/modes")
        def choose_mode():
            return render_template("choose_mode.html")

    def popup(self):
        @self.app.route("/popup", methods=["POST", "GET"])
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
                    mode,
                    player_one_name=player_one_name,
                    player_two_name=player_two_name,
                )

                session["player_one"] = player_one.to_dict()
                session["player_two"] = player_two.to_dict()

                return redirect(url_for("create_game"))
            return render_template("popup.html")
