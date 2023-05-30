import sqlite3 as sq
from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


async def db_connect():
    global db, cur
    db = sq.connect("books.db")
    cur = db.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS history_books(book_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, writter TEXT, description TEXT, book_link TEXT, photo TEXT, pages INTEGER)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS detective_books(book_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, writter TEXT, description TEXT, book_link TEXT, photo TEXT, pages INTEGER)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS novel_books(book_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, writter TEXT, description TEXT, book_link TEXT, photo TEXT, pages INTEGER)"
    )
    cur.execute(
         "CREATE TABLE IF NOT EXISTS horror_books(book_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, writter TEXT, description TEXT, book_link TEXT, photo TEXT, pages INTEGER)"
    )
    cur.execute(
         "CREATE TABLE IF NOT EXISTS motivation_books(book_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, writter TEXT, description TEXT, book_link TEXT, photo TEXT, pages INTEGER)"
    )
    cur.execute(
         "CREATE TABLE IF NOT EXISTS fantasy_books(book_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, writter TEXT, description TEXT, book_link TEXT, photo TEXT, pages INTEGER)"
    )


global dict_genre
dict_genre = {"genre_name": None}


async def add_books(state: FSMContext):

    data = await state.get_data()
    products = cur.execute(
        f'INSERT INTO {dict_genre["genre_name"]}(title, writter, description, book_link, photo, pages) VALUES ( ?, ?, ?, ?, ?, ?)',
        (
            data["title"],
            data["writter"],
            data["description"],
            data["book_link"],
            data["photo"],
            data["pages"],
        ),
    )
    db.commit()
    return products


global list_book
list_book = [1]


async def select_genre(call: CallbackQuery):
    from keyboards.inline_user_arm import control_button
    from TelegramBot import bot

    book_id = list_book[-1]
    call.answer()
    cur.execute(f'SELECT * FROM {dict_genre["genre_name"]} WHERE book_id = ?', [book_id])
    records = cur.fetchall()
    for item in records:
        if list_book[0] == 1:
            await call.message.delete()
            await bot.send_photo(
                chat_id=call.message.chat.id,
                photo=item[5],
                caption=f"<b>Գրքի Անունը</b>: {item[1]} \
                \n\n<b>Հեղինակը</b>: {item[2]}\
                \n\n<b>Նկարագրությունը</b>: {item[3]}\
                \n\n<b>էջերի քանակը</b>: {item[6]}\
                \n\n<b>Ներբեռման հղումը</b>: {item[4]}\
                \n\n<i>Գրքի id: {item[0]}</i>",
                parse_mode="HTML", 
                reply_markup=control_button(),
                protect_content=True,
            )

        elif list_book[-1] > 1:
            await bot.edit_message_caption(
                chat_id=call.message.chat.id,
                message_id= call.message.message_id,
                caption=f'<b>Գրքի Անունը</b>: {item[1]} \
                \n\n<b>Հեղինակը</b>: {item[2]}\
                \n\n<b>Նկարագրությունը</b>: {item[3]}\
                \n\n<b>էջերի քանակը</b>: {item[6]}\
                \n\n<b>Ներբեռման հղումը</b>: {item[4]}\
                \n\n<i>Գրքի id: {item[0]}</i>',
                reply_markup=control_button()
            )
            
    if len(records) == 0:
        await call.answer(text='Տվյալ ժանրում առկա գրքեր չկան։\
            \nԳրքերի առակայության դեպքում մենք կտեղեկացնենք ձեզ։\
                \n\nՄինչև այդ կարող եք տեսնել մեր գրադարանի այլ ժանրի գրքերը:', 
                          show_alert=True) 
    
    
def records_check():
    cur.execute(f'SELECT * FROM {dict_genre["genre_name"]}')
    row_count = cur.fetchall()
    if len(row_count) > list_book[0]:
        return True
    elif len(row_count) == list_book[0]:
        return False
    

def records_num():
    cur.execute(f'SELECT * FROM {dict_genre["genre_name"]}')
    row_count = cur.fetchall()
    return len(row_count)


from utils.callback_factory import NumbersCallbackFactory
async def callbacks_num_change_fab(call: CallbackQuery, callback_data: NumbersCallbackFactory):
    from handlers.client_arm import back_to_genre

    if callback_data.action == "change":
        list_book.append(list_book[-1] + callback_data.value)
        list_book.pop(0)
        await select_genre(call)
        await call.answer()

    elif callback_data.action == "back":
        await call.message.delete()
        await back_to_genre(call)
        await call.answer()
        list_book.append(1)
        list_book.pop(0)



async def register_DB_handlers(dp: Dispatcher):
    dp.callback_query.register(
        callbacks_num_change_fab, NumbersCallbackFactory.filter()
    )

