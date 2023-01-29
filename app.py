from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from db.game_db import GameDB
from exceptions.empty_game import EmptyGame
from exceptions.game_existment import GameExistment
from models.game import Game
from models.player_factory import PlayerFactory
from abc import ABC, abstractmethod


class AppInterface(ABC):
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass


class ConnectFour(AppInterface):
    def __init__(self):
        self.app = Flask(_name_)
        self.app.secret_key = "secret_key"
        self.game_db = GameDB("GAME")
        self.game_db.init_db()
        print(self.game_db.game_state.get_game_state())

    def start(self):
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

    def create_game(self):
        @self.app.route("/game")
        def create_game():
            player_one = PlayerFactory.create_player_from_json(session["player_one"])
            player_two = PlayerFactory.create_player_from_json(session["player_two"])

            self.game = Game(player_one=player_one, player_two=player_two)
            self.game.set_player_dot()
            self.game.set_players()
            self.game.start()
            game_id = self.game.get_id()
            self.game_db.create_game(game_id, self.game.get_game_state())
            print(self.game_db.game_state.get_game_state())

            return render_template("game.html", game_id=game_id)

    def board(self):
        @self.app.route("/board", methods=["GET"])
        def board():
            game_id = request.args.get("game_id")
            if game_id is None:
                EmptyGame

            game_state = self.game_db.get_game_state(game_id)
            print(self.game_db.game_state.get_game_state())

            if game_state is None:
                GameExistment

            response = jsonify(
                {
                    "game_state": game_state[1],
                }
            )
            return response

    def move(self):
        @self.app.route("/move", methods=["POST"])
        def move():
            print("in move routeeeeeeeeeeee")
            if request.method == "POST":
                col = int(request.get_json()["column"])
                res = self.game.play(player=self.game.current_turn, col=col)
                game_state = self.game.get_game_state()
                self.game_db.update_game(self.game.get_id(), game_state)
                print(self.game_db.game_state.get_game_state())

            return game_state

    def run(self):
        if _name_ == "_main_":
            self.start()
            self.choose_mode()
            self.popup()
            self.create_game()
            self.board()
            self.move()
            self.app.run(debug=True)


game = ConnectFour()
game.run()
