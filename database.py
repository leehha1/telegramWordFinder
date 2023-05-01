import sqlite3
from typing import Union

class Database:
    def __init__(self, db_name: str = None):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name: str = None, columns: Union[list, tuple, set] = None):
        columns_str = ", ".join(columns)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")

    def insert_data(self, table_name: str = None, data: dict = None):
        placeholders = ", ".join("?" * len(data))
        self.cursor.execute(f"INSERT INTO {table_name} {tuple(data.keys())} VALUES ({placeholders})", tuple(data.values()))
        self.conn.commit()

    def delete_data(self, table_name: str = None, condition: str = None):
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
        self.conn.commit()

    def update_data(self, table_name: str = None, data: dict = None, condition: str = None):
        updates = ", ".join([f"{k} = ?" for k in data.keys()])
        values = tuple(data.values())
        self.cursor.execute(f"UPDATE {table_name} SET {updates} WHERE {condition}", values)
        self.conn.commit()

    def select_data(self, table_name: str = None, columns: Union[list, tuple] = None, condition: str = None):
        columns_str = "*"
        if columns:
            columns_str = ", ".join(columns)
        query = f"SELECT {columns_str} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    db = Database("example.db")
    db.create_table("users", ["id INTEGER PRIMARY KEY", "name TEXT", "age INTEGER"])
    db.insert_data("users", {'name': "John", 'age': 100})
    # db.update_data("users", {"name": "Mike", "age": 28}, "id = 1")
    # db.delete_data("users", "id = 2")
    rows = db.select_data("users",
                          columns= ['name', 'age'],
                          # condition='id = 3',
                          )
    print(rows)  # Output: [('Mike', 28)]