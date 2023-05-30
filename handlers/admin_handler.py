from TelegramBot import bot
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import time
from keyboards.admin_inline import admin_start

storage = MemoryStorage()


class FSMadmin(StatesGroup):
    set_title = State()
    set_writter = State()
    set_description = State()
    set_book_link = State()
    set_photo = State()
    set_pages = State()
    set_genre = State()

global admins_id, admins_username
admins_id = [1559308187,  5375217621]
admins_username = ['Ashot_Poxpat', 'Arthur']

async def admin_menu(call: CallbackQuery, bot: Bot):
    if call.message.chat.id in admins_id:
        await call.message.edit_text(
            text="❗️Ադմինիստրատորի ռեժիմը ԱԿՏԻՎ է։",
            reply_markup=admin_start())
        await call.answer()
    else:
        await call.answer(text='Դուք ադմին չեք', show_alert=True)
        time.sleep(2)
        await call.message.delete()



async def FSM_cancel(message: Message, bot: Bot, state="*"):
    if state is None:
        return
    await state.clear()
    await message.delete()
    await bot.edit_message_text("❗️FSM գործընթացը դադարեցված է։",
                                chat_id=message.chat.id,
                                message_id=book_question_1.message_id,
                                reply_markup=admin_start())



async def addBooks_arm(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.message.delete()
    global book_question_1
    book_question_1 = await call.message.answer("Գրեք գրքի վերնագիրը։\
        \n\nԳրանցումը դադարեցնելու համար սեղմեք -> /cancel_operation")
    await state.set_state(FSMadmin.set_title)



async def handle_writter(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.delete()
    global book_question_2
    book_question_2 =  await bot.edit_message_text("Գրեք գրքի հեղինակի անունը , ազգանունը։\
        \n\nԳրանցումը դադարեցնելու համար սեղմեք -> /cancel_operation", 
                                chat_id=message.chat.id,
                                message_id=book_question_1.message_id)
    await state.set_state(FSMadmin.set_writter)



async def handle_description(message: Message, state: FSMContext):
    await state.update_data(writter=message.text)
    await message.delete()
    global book_question_3
    book_question_3 = await bot.edit_message_text("Գրեք գրքի նկարագրությունը։\
        \n\nԳրանցումը դադարեցնելու համար սեղմեք -> /cancel_operation",
                                chat_id=message.chat.id,
                                message_id=book_question_2.message_id)
    await state.set_state(FSMadmin.set_description)



async def handle_link(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.delete()
    global book_question_4
    book_question_4 = await bot.edit_message_text("Ուղարկեք գրքի ներբեռման հղումը։\
        \n\nԳրանցումը դադարեցնելու համար սեղմեք -> /cancel_operation",
                                chat_id=message.chat.id,
                                message_id=book_question_3.message_id)
    await state.set_state(FSMadmin.set_book_link)



async def handle_photo(message: Message, state: FSMContext):
    await state.update_data(book_link=message.text)
    await message.delete()
    global book_question_5
    book_question_5 = await bot.edit_message_text("Ուղարկիր գրքի նկարը։\
        \n\nԳրանցումը դադարեցնելու համար սեղմեք -> /cancel_operation",
                                chat_id=message.chat.id,
                                message_id=book_question_4.message_id)
    await state.set_state(FSMadmin.set_photo)



async def handle_page(message: Message, state: FSMContext):
    if not message.photo:
        await message.delete()
        await message.answer("Սա նկար չէ։")
        await state.set_state(FSMadmin.set_photo)
        time.sleep(2)
        await message.delete()
    else:
        await state.update_data(photo=message.photo[0].file_id)
        await message.delete()
        global book_question_6
        book_question_6 = await bot.edit_message_text("Իսկ հիմա էջերի քանակը։\
            \n\nԳրանցումը դադարեցնելու համար սեղմեք -> /cancel_operation",
                                chat_id=message.chat.id,
                                message_id=book_question_5.message_id)
        await state.set_state(FSMadmin.set_pages)


async def handle_genre(message: Message, state: FSMContext):
    from keyboards.admin_inline import genre_choice

    if message.text.isnumeric():
        await state.update_data(pages=message.text)
        await message.delete()
        global book_question_7
        book_question_7 = await bot.edit_message_text(
            "իսկ հիմա նշիր թե որ ժանրին է պատկանում գիրքը։\
                \n\nԳրանցումը դադարեցնելու համար սեղմեք -> /cancel_operation",
                chat_id=message.chat.id,
                message_id=book_question_6.message_id,
                reply_markup=genre_choice()
        )
        await state.set_state(FSMadmin.set_genre)

    else:
        await message.delete()
        await message.answer("Դա թիվ չէ։")
        time.sleep(2)
        await message.delete()


async def genre_set(call: CallbackQuery, state: FSMContext):
    from utils import sq_lite_db_books
    from utils.sq_lite_db_books import dict_genre

    try:
        await state.update_data(genre=call.message.text)
        await call.message.edit_text(
            text="Շնորհավորում ենք, ձեր պրոդուկտը ստեղծված է։",
            reply_markup=admin_start(),
        )

        dict_genre["genre_name"] = call.data

        data = await state.get_data()
        title = data["title"]
        writter = data["writter"]
        description = data["description"]
        book_link = data["book_link"]
        photo = data["photo"]
        pages = data["pages"]
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=f"<b>Գրքի Անունը</b>: {title}\
                    \n<b>Հեղինակը</b>: {writter}\
                    \n<b>Նկարագրությունը</b>: {description}\
                    \n<b>էջերի քանակը</b>: {pages}\
                    \n<b>Ներբեռման հղումը</b>: {book_link}",
            parse_mode="html",
        )

        await sq_lite_db_books.add_books(state)
        await state.clear()
    except:
        bot.send_message(
            chat_id=call.message.chat.id,
            text="❗️❗️Ներողություն, տեխնիկական խնդրի\
                                        պատճառով հարցումը (Գրքի ստեղծման ավարտ)\
                                        չի հաջողվել ավարտել, փորձեք մի փոքր ուշ կրկնել օպերացիան։\
                                        \nՇնորհակալություն ըմբռնումով մոտենալում համար։",
        )
        time.sleep(4)
        await call.message.delete()


async def register_admin_handlers(dp: Dispatcher):
    dp.callback_query.register(admin_menu, Text('admin_mode'))
    dp.callback_query.register(addBooks_arm, Text("add_book"))
    dp.message.register(FSM_cancel, Command(commands="cancel_operation"))
    dp.message.register(handle_writter, FSMadmin.set_title)
    dp.message.register(handle_description, FSMadmin.set_writter)
    dp.message.register(handle_link, FSMadmin.set_description)
    dp.message.register(handle_photo, FSMadmin.set_book_link)
    dp.message.register(handle_page, FSMadmin.set_photo)
    dp.message.register(handle_genre, FSMadmin.set_pages)
    dp.callback_query.register(genre_set, FSMadmin.set_genre)
