class EmptyGame(Exception):
    def __init__(self, message="Empty game id!") -> None:
        self.message = message
        super().__init__(self.message)