import sqlite3
from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def init_db(self):
        """Initialize the database and create the table"""
        pass

    @abstractmethod
    def create_game(self, id, move):
        """Add the first move"""
        pass

    @abstractmethod
    def update_game(self, id, data):
        """Update table"""

    @abstractmethod
    def get_game_state(self):
        """Retrieve the last move from the table"""
        pass

    @abstractmethod
    def clear(self):
        """Clear the table"""
        pass

    @abstractmethod
    def _get_connection(self):
        """Return a connection to the database"""
        pass


class GameState:
    def __init__(self):
        self.state = None

    def update_game(self, data):
        self.state = data

    def get_game_state(self):
        return self.state


class GameDB(Database):
    def __init__(self, table_name):
        self.table_name = table_name
        self.game_state = GameState()


    def init_db(self):
        connection = self._get_connection()
        try:
            connection.execute(
                f"CREATE TABLE IF NOT EXISTS {self.table_name} (ID TEXT PRIMARY KEY, DATA TEXT)"
            )
            self.game_state.update_game(f"Table {self.table_name} created.")
        except sqlite3.Error as e:
            raise Exception(f"Error creating table: {e}")

    def create_game(self, id, data):
        connection = self._get_connection()
        try:
            cur = connection.cursor()
            cur.execute(f"INSERT INTO {self.table_name} VALUES (?, ?)", (id, data))
            connection.commit()
            self.game_state.update_game(f"First move added to the {self.table_name} table.")
        except sqlite3.Error as e:
            raise Exception(f"Error adding move: {e}")

    def update_game(self, id, data):
        connection = self._get_connection()
        try:
            cur = connection.cursor()
            cur.execute(f"UPDATE {self.table_name} SET DATA=? WHERE ID=?", (data, id))
            connection.commit()
            self.game_state.update_game("Player's move updated to db.")
        except sqlite3.Error as e:
            raise Exception(f"Error adding move: {e}")

    def get_game_state(self, id):
        connection = self._get_connection()
        try:
            cur = connection.cursor()
            cur.execute(f"SELECT * FROM {self.table_name} WHERE ID='{id}'")
            result = cur.fetchall()
            # print("result from db", result, id)
            self.game_state.update_game("Retrieved game state.")
            return result[-1]
        except sqlite3.Error as e:
            raise Exception(f"Error retrieving move: {e}")

    def clear(self):
        connection = self._get_connection()
        try:
            connection.execute(f"DROP TABLE IF EXISTS {self.table_name}")
            self.game_state.update_game(f"Table {self.table} dropped.")
        except sqlite3.Error as e:
            raise Exception(f"Error dropping table: {e}")

    def _get_connection(self):
        try:
            connection = sqlite3.connect("game_db")
            self.game_state.update_game(f"Created connection with sqlite db.")
            return connection
        except sqlite3.Error as e:
            raise Exception(f"Error connecting to database: {e}")
