from abc import ABC, abstractmethod
import sqlite3


class Database(ABC):
    @abstractmethod
    def init_db(self):
        """Initialize the database and create the table"""
        pass

    @abstractmethod
    def add_move(self, id, move):
        """Add a move to the table"""
        pass

    @abstractmethod
    def get_move(self):
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


class GameDB(Database):
    def __init__(self, table_name):
        self.table_name = table_name

    def init_db(self):
        connection = self._get_connection()
        try:
            connection.execute(
                f"CREATE TABLE IF NOT EXISTS {self.table_name} (ID INT, DATA TEXT)"
            )
            print(f"Table {self.table_name} created.")
        except sqlite3.Error as e:
            raise Exception(f"Error creating table: {e}")

    def add_move(self, id, move):
        connection = self._get_connection()
        try:
            cur = connection.cursor()
            cur.execute(f"INSERT INTO {self.table_name} VALUES (?, ?)", (id, move))
            connection.commit()
            print("Player's move added to db.")
        except sqlite3.Error as e:
            print(e)
            # raise Exception(f"Error adding move: {e}")

    def get_move(self):
        connection = self._get_connection()
        try:
            cur = connection.cursor()
            cur.execute(f"SELECT * FROM {self.table_name}")
            result = cur.fetchall()
            return result[0]
        except sqlite3.Error as e:
            # raise Exception(f"Error retrieving move: {e}")
            print(e)

    def clear(self):
        connection = self._get_connection()
        try:
            connection.execute(f"DROP TABLE IF EXISTS {self.table_name}")
            print("Table dropped.")
        except sqlite3.Error as e:
            raise Exception(f"Error dropping table: {e}")

    def _get_connection(self):
        try:
            connection = sqlite3.connect("game_db")
            return connection
        except sqlite3.Error as e:
            raise Exception(f"Error connecting to database: {e}")
