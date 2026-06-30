import sqlite3


class Database:
    def __init__(self, db_name: str = "database.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.create_tables()


    def execute(self, query: str, params: tuple = (), *, fetchone: bool = False, fetchall: bool = False, commit: bool = False):
        self.cursor.execute(query, params)

        if commit:
            self.conn.commit()

        if fetchone:
            return self.cursor.fetchone()

        if fetchall:
            return self.cursor.fetchall()


    def create_tables(self):
        self.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            session_string TEXT NOT NULL
        )
        """, commit=True)


    def add_account(self, user_id: int, session_string: str):
        self.execute(
            """
            INSERT INTO accounts(
                user_id,
                session_string
            )
            VALUES (?, ?)
            """,
            (
                user_id,
                session_string
            ),
            commit=True
        )

    def get_account(self, user_id: int):
        return self.execute(
            """
            SELECT *
            FROM accounts
            WHERE user_id = ?
            """,
            (user_id,),
            fetchone=True
        )

    def get_all_accounts(self):
        return self.execute(
            """
            SELECT *
            FROM accounts
            """,
            fetchall=True
        )