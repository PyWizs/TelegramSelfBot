import sqlite3
import config

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
            session_string TEXT NOT NULL,

            enabled INTEGER NOT NULL DEFAULT 1,
            show_time INTEGER NOT NULL DEFAULT 0,
            edit_enabled INTEGER NOT NULL DEFAULT 0,

            font TEXT NOT NULL DEFAULT '₀,₁,₂,₃,₄,₅,₆,₇,₈,₉,:',

            edit_time REAL NOT NULL DEFAULT 0.1
        )
        """, commit=True)


    def add_account(self, user_id: int, session_string: str, enabled: bool = True, show_time: bool = False, edit_enabled: bool = False, font: str = config.DEFAULT_FONT, edit_time: float = 0.1):
        self.execute(
            """
            INSERT INTO accounts(
                user_id,
                session_string,
                enabled,
                show_time,
                edit_enabled,
                font,
                edit_time
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                session_string,
                enabled,
                show_time,
                edit_enabled,
                font,
                edit_time
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
    
class User:
    def __init__(self, db, user_id):
        self.db = db
        self.user_id = user_id

        self.reload()


    def reload(self):
        account = self.db.get_account(self.user_id)

        self.session = account["session_string"]
        self.enabled = bool(account["enabled"])
        self.show_time = bool(account["show_time"])
        self.edit_enabled = bool(account["edit_enabled"])
        self.font = account["font"]
        self.edit_time = account["edit_time"]


    def update(self, **kwargs):
        if not kwargs: return

        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(self.user_id)

        query = f"UPDATE accounts SET {set_clause} WHERE user_id = ?"
        self.db.execute(query, tuple(values), commit=True)

        self.reload()