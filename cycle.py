from pyrogram import Client, filters, enums
from config import (SESSION_NAME, API_ID, API_HASH, TARGET_CHAT_ID, REQUIRED_WORDS, DB_NAME,
                    SEARCH_MESSAGES_LIMIT, SEARCH_MESSAGES_QUERY, TABLE_NAME, FORWARD_CHAT_ID)
from database import Database
from finder import Finder


app = Client(name=SESSION_NAME, api_id=API_ID, api_hash=API_HASH)


@app.on_message(filters.text & filters.chat(TARGET_CHAT_ID))
async def finder(client, message):
    if SEARCH_MESSAGES_QUERY in message.text:
        for word in REQUIRED_WORDS:
            if word in message.text:
                if not finder.find_in_db(message.id):

                    res = await message.forward(FORWARD_CHAT_ID)

                    if res:

                        db.insert_data(TABLE_NAME, {'message_id': message.id, 'message': message.text, 'is_send': 1})
                        print(f"The message ({message.id}) has been forwarded and stored in the database")
                break



if __name__ == '__main__':
    print('Start')
    db = Database(DB_NAME)
    db.create_table(TABLE_NAME, ["id INTEGER PRIMARY KEY", "message_id INTEGER", "message TEXT", "is_send INTEGER"])
    finder = Finder(db=db)
    app.run()
    print('end')
