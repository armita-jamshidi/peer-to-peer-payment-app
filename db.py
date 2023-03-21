import os
import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for the Task app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        #connecting databse to program
        self.conn = sqlite3.connect(
            "users.db", check_same_thread=False
        )

        self.delete_users_table()
        self.create_users_table()

    def create_users_table(self):
        """
        Using SQL, create user table
        """

        try:
            self.conn.execute(
                """
                CREATE TABLE users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    balance INTEGER NOT NULL
                );
                """
            )
        except Exception as e:
            print(e)

    def delete_users_table(self):
        """
        Using SQL, deletes a users table
        """
        self.conn.execute("DROP TABLE IF EXISTS users;")

    def get_all_users(self):
        """
        Using SQL, gets all users in the users table
        """
        cursor = self.conn.execute("SELECT * FROM users;")
        users = []

        for row in cursor:
            users.append({"id": row[0], "name": row[1], "username": row[2]})
        return users

    def get_users_by_id(self, user_id):
        """
        Using SQL, get user by ID
        """
        cursor = self.conn.execute("SELECT * FROM users WHERE ID = ?", (user_id,))

        for row in cursor:
            return {"id": row[0], "name": row[1], "username": row[2], "balance": row[3]}
        
        return None
    

    def insert_users_table(self, name, username, balance):
        """
        Using SQL, adds a new user in the users table
        """
        if not balance:
            cursor = self.conn.execute("INSERT INTO users (name, username, balance) VALUES (?, ?, ?);", (name, username, 0))
        else:
            cursor = self.conn.execute("INSERT INTO users (name, username, balance) VALUES (?, ?, ?);", (name, username, balance))
        self.conn.commit()
        return cursor.lastrowid

    def delete_user_by_id(self, id):
        """
        Using SQL, deleting a user from the user table
        """
       
        self.conn.execute(
            """DELETE FROM users WHERE id = ?;""",
            (id,)
        )

        self.conn.commit()

    def send_money(self, sender, reciever, amount):
        """
        Using SQL, sending amount money from sender to reciever
        """
        cursor = self.conn.execute("""SELECT balance FROM users WHERE
        ID = ?;""", (sender,))
        #cursor is a 2d list, and we're getting the first value which is an object
        for row in cursor:
            sender_balance = row[0]
        
        if sender_balance < amount:
            return 0
        new_s_balance = sender_balance - amount

        cursor2 = self.conn.execute("""SELECT balance FROM users WHERE
        id = ?;""", (reciever,))
        for row in cursor2:
            reciever_balance = row[0]

        new_r_balance = reciever_balance + amount

        self.conn.execute(
            """
            UPDATE users 
            SET balance = ? WHERE id = ?;
            """,
            (new_s_balance, sender)
        )

        self.conn.execute(
            """
            UPDATE users 
            SET balance = ? WHERE id = ?;
            """,
            (new_r_balance, reciever)
        )
        self.conn.commit()

        return 1

# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
