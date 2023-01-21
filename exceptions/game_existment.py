class GameExistment(Exception):
    def __init__(self, message="Game doesn't exist!") -> None:
        self.message = message
        super().__init__(self.message)