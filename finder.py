from pyrogram import Client, filters, enums
from config import (SESSION_NAME, API_ID, API_HASH, TARGET_CHAT_ID, REQUIRED_WORDS, DB_NAME,
                    SEARCH_MESSAGES_LIMIT, SEARCH_MESSAGES_QUERY, TABLE_NAME, FORWARD_CHAT_ID)
from database import Database


class Finder:
    def __init__(self, app=None, db=None):
        self.db = db
        self.app = app

    def find_in_db(self, message_id):
        res = self.db.select_data(TABLE_NAME, condition=f'message_id = {message_id} AND is_send = 1')
        if len(res) != 0:
            return True
        return False

    async def read_last_mess(self):
        async with self.app:
            messages: list = []
            async for message in self.app.search_messages(TARGET_CHAT_ID, query=SEARCH_MESSAGES_QUERY,
                                                          limit=SEARCH_MESSAGES_LIMIT):
                for word in REQUIRED_WORDS:
                    if word in message.text:
                        if not self.find_in_db(message.id):
                            if message not in messages:
                                messages.append(message)
            for mess in messages:
                res = await mess.forward(FORWARD_CHAT_ID)
                if res:
                    self.db.insert_data(TABLE_NAME, {'message_id': mess.id, 'message': mess.text, 'is_send': 1})

    def __del__(self):
        print('del')
        del self.db
        del self.app


app = Client(name=SESSION_NAME, api_id=API_ID, api_hash=API_HASH)


if __name__ == '__main__':
    db = Database(DB_NAME)
    db.create_table(TABLE_NAME, ["id INTEGER PRIMARY KEY", "message_id INTEGER", "message TEXT", "is_send INTEGER"])
    finder = Finder(app, db)
    app.run(finder.read_last_mess())
    del finder

