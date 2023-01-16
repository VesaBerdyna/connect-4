from models.human_player import HumanPlayer
from models.minimax_ai import MinimaxAI
from enums.player_type import PlayerType


class PlayerFactory:
    @staticmethod
    def create_player(mode: str, player_one_name: str, player_two_name: str):
        if mode == "multi":
            return HumanPlayer(player_one_name), HumanPlayer(player_two_name)
        else:
            return HumanPlayer(player_one_name), MinimaxAI("Bot")

    @staticmethod
    def create_player_from_json(data: str):
        if data["type"] == PlayerType.HumanPlayer.value:
            return HumanPlayer.from_dict(data)
        else:
            return MinimaxAI.from_dict(data)

    
