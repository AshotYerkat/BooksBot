from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart, Text

async def start(message: Message):
    from keyboards.inline_user_arm import start_inline
    await message.answer(
            "🇦🇲 Բարև👋 սիրելի գրքանսեր, ես քեզ կօգնեմ գտնել քեզ հետաքրքրող գիրքը📚:\
        \n\n🇷🇺 Привет👋 дорогой читатель, я помогу тебе найти ту книгу📚 которую ты ищешь.\
        \n\n🇬🇧Hi👋, dear, I will help you find the book📚 you are looking for.",
            reply_markup=start_inline(),
        )

        
        
async def menu_action(call: CallbackQuery):
    from utils.sq_lite_db_users import user_singed_check
    from keyboards.inline_user_arm import menu_arm

    await call.answer()
    if await user_singed_check(call) is False:
        await call.message.edit_text(
            "⏳Ընտրեք գործողություններից մեկը:\n\
            \n❗️❗️Քանի որ մեր գրադարանից օգտվելը\
                \nամբողջովին <a>անվճար է</a>՝ բոտի գրադարանից\n օգտվելու համար անհրաժեշտ է գրանցում կատարել\
                    \nԳրանցումը կտևի ընդամենը ~2 րոպե:",
            reply_markup=menu_arm(),
        )
    else:
        await call.message.edit_text('⏳Ընտրեք գործողություններից մեկը:',
        reply_markup=menu_arm()
        )


async def user_delete_func(call: CallbackQuery):
    from keyboards.inline_user_arm import user_delete_kb
    from utils.sq_lite_db_users import user_delete
    if await user_delete(call) == True:
        await call.message.edit_text('⏳Հաստատեք ձեր օգտահաշվի ջնջումը:', reply_markup=user_delete_kb())
        await call.answer() 
    else:
        await call.answer(text='Դուք չունեք ակտիվ օգտահաշիվ', show_alert=True)
async def user_delete_alert(call: CallbackQuery):
    await call.answer(text='Ձեր օգտահաշիվը ջնջված է', show_alert=True)



async def genre_list_arm(call: CallbackQuery):
    from TelegramBot import bot
    from keyboards.inline_user_arm import genre_list
    from utils.sq_lite_db_users import user_singed_check

    if await user_singed_check(call) == True:
        await call.message.edit_text(
            "😃Ահա մեր գրադարանի գրքերի ժանրերի ցանկը․ \nԸնտրեք ձեզ հետաքրքրող ժանրը:",
            reply_markup=genre_list()
        )
        await call.answer()
    elif await user_singed_check(call) == False:
        await call.answer(text="Դուք գրանցված չեք", show_alert=True)



async def language_change(call: CallbackQuery):
    from keyboards.inline_user_arm import start_inline

    await call.answer()
    await call.message.edit_text(
            "🇦🇲 Ընտրեք լեզուն \n\n🇷🇺 Выберите язык \n\n 🇬🇧Choice a language",
            reply_markup=start_inline(),
        )

        
        
async def english_menu(call: CallbackQuery):
    await call.answer(text='Sorry, the English version of the bot is currently unavailable',
                          show_alert=True)
    

async def russian_menu(call: CallbackQuery):
    await call.answer(text='Извините, русская версия бота на данный момент недоступен',
                          show_alert=True)
    



from utils.callback_factory import Genre_Choice_CallbackFactory
async def books(call: CallbackQuery, callback_data: Genre_Choice_CallbackFactory):
    from utils import sq_lite_db_books
    from utils.sq_lite_db_books import dict_genre
    if callback_data.action == "choice":
        dict_genre["genre_name"] = callback_data.genre
    await sq_lite_db_books.select_genre(call)
    await call.answer()



async def back_to_genre(call: CallbackQuery):
    from keyboards.inline_user_arm import genre_list

    await call.message.answer(
            "😃Ահա մեր գրադարանի գրքերի ժանրերի ցանկը: \nԸնտրեք ձեզ հետաքրքրող ժանրը:",
            reply_markup=genre_list())
    await call.answer()
    

async def none_skipper(call: CallbackQuery):
    await call.answer()

    
async def register_client_handlers(dp: Dispatcher):
    dp.message.register(start, CommandStart())
    dp.callback_query.register(menu_action, Text("arm_start"))
    dp.callback_query.register(user_delete_func, Text('delete_account'))
    dp.callback_query.register(user_delete_alert, Text('delete_user'))
    dp.callback_query.register(genre_list_arm, Text("genre_show"))
    dp.callback_query.register(language_change, Text("language_choice"))
    dp.callback_query.register(english_menu, Text('eng_start'))
    dp.callback_query.register(russian_menu, Text('rus_start'))
    dp.callback_query.register(books, Genre_Choice_CallbackFactory.filter())
    dp.callback_query.register(none_skipper, Text('none'))
