import sqlite3
from abc import ABC, abstractmethod
from sqlite3 import Error


class db(ABC):
    @abstractmethod
    def close_connection():
        pass

    @abstractmethod
    def create_table():
        pass

    @abstractmethod
    def add_move(move):
        pass

    @abstractmethod
    def getMove():
        pass

    @abstractmethod
    def clear():
        pass


class GameDB(db):
    def __init__(self, table_name):
        self.__table_name = table_name
        self.__connection = sqlite3.connect("game_db")

    def close_connection(self):
        if self.__connection:
            self.__connection.close()

    def create_table(self):
        try:
            self.__connection.execute(
                f"CREATE TABLE {self.__table_name} (current_turn TEXT, board TEXT, winner TEXT, player_one TEXT, player_two TEXT, remaining_moves INT)"
            )
            print(f"Table {self.__table_name} created.")
        except Error as e:
            print(e)

        finally:
            self.close_connection()

    def add_move(self, move):  # will take in a tuple
        self.clear()
        self.create_table()
        try:
            cur = self.__connection.cursor()
            cur.execute(
                f"INSERT INTO {self.__table_name} VALUES (?, ?, ?, ?, ?, ?)", move
            )
            self.__connection.commit()
            print("Player's move added to db.")
        except Error as e:
            print(e)

        finally:
            self.close_connection()

    def getMove(self):
        conn = None
        try:
            conn = sqlite3.connect("sqlite_db")
            cur = conn.cursor()

            cur.execute(f"SELECT * FROM {self.__table_name}")
            result = cur.fetchall()
            return result[0]

        except Error as e:
            print(e)
            return None

        finally:
            self.close_connection()

    def clear(self):
        try:
            self.__connection.execute(f"DROP TABLE {self.__table_name}")
            print("Table droped.")
        except Error as e:
            print(e)

        finally:
            self.close_connection()
