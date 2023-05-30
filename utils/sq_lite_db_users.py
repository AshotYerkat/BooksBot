import sqlite3
from aiogram.fsm.context import FSMContext
from aiogram.types import  CallbackQuery


async def db_connect_users():
    global db_user, cur_user
    db_user = sqlite3.connect("user_info.db")
    cur_user = db_user.cursor()

    cur_user.execute(
        "CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, user_first_name TEXT, user_last_name TEXT, user_age INTEGER, user_gender TEXT)"
    )
    db_user.commit()


async def add_user(state: FSMContext):

    data = await state.get_data()
    users_reg = cur_user.execute(
            "INSERT INTO users(user_id, user_first_name, user_last_name, user_age, user_gender) VALUES (?, ?, ?, ?, ?)",
            (data["user_id"],
             data["user_first_name"],
             data["user_last_name"],
             data['user_age'],
             data['user_gender']
            ),
        )
    db_user.commit()
    return users_reg



async def user_singed_check(call: CallbackQuery):
    user_id = call.message.chat.id
    cur_user.execute('SELECT * FROM users WHERE user_id = ?', [user_id])
    users = cur_user.fetchall()
    if len(users) > 0:
        db_user.commit()
        return True
    elif len(users) == 0:
        db_user.commit()
        return False
    
    
  
async def user_delete(call: CallbackQuery):
    user_id = call.message.chat.id
    cur_user.execute('SELECT * FROM users WHERE user_id = ?', [user_id])
    users = cur_user.fetchall()
    if len(users) > 0:
         cur_user.execute('DELETE FROM users WHERE user_id = ?', [user_id])
         db_user.commit()
         return True
          
    else:
        db_user.commit()
        return False