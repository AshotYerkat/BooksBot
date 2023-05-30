
from aiogram import Bot, Dispatcher
from TelegramBot import bot
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Text, Command
import time



storage = MemoryStorage()
class FSMclient(StatesGroup):
    user_id = State()
    user_first_name = State()
    user_last_name = State()
    user_age = State()
    user_gender = State()



async def user_registration(call: CallbackQuery, state: FSMContext):
    from utils.sq_lite_db_users import user_singed_check
    if await user_singed_check(call) == False:
        await call.message.delete()
        global question_1
        question_1 = await call.message.answer(
            "📝 1/5: Խնդրում եմ գրեք ձեր անունը։\
            \n❗️Խնդրում ենք նշել այն անունը, որով գրանցված եք <i>տելեգրամում</i>․\
            \nՀակառակ դեպքում գրանցումը <b>չի շարունակվի</b>։\
            \n\nԳրանցումը դադարեցնելու համար սեղմեք -> /cancel", 
            parse_mode="html"
        )
        await state.set_state(FSMclient.user_first_name)
        
    elif await user_singed_check(call) == True:
        await call.answer(text='Դուք արդեն գրանցված եք', show_alert=True)



async def FSM_cancel_client(message: Message, bot: Bot, state="*"):
    from keyboards.inline_user_arm import menu_arm

    if state is None:
        return
    await state.clear()
    await message.delete()
    await bot.edit_message_text("❗️Գրանցումը դադարեցված է",
                                chat_id=message.chat.id,
                                message_id=question_1.message_id,
                                reply_markup=menu_arm())



async def handle_first_name(message: Message, state: FSMContext):
    if message.text == message.from_user.first_name:
        await state.update_data(user_first_name=message.text)
        await message.delete()
        global question_2
        question_2 = await bot.edit_message_text(text="📝2/5: Շատ լավ, իսկ հիմա նշիր ազգանունը:\
                \n\n❗️Խնդրում ենք նշել այն ազգանունը, որով գրանցված եք <i>տելեգրամում</i>։\
                \nՀակառակ դեպքում գրանցումը <b>չի շարունակվի</b>։\
                 \n\nԵթե ձեր տելեգրամ պրոֆիլում նծված չէ ձեր ազգանունը, ապա\
                 \nգրեք 'pass' (առանց չակերտների):\
                \n\nԳրանցումը դադարեցնելու համար սեղմեք -> /cancel", 
                 chat_id=message.chat.id,
                 message_id=question_1.message_id,
            parse_mode="html",
        )

        await state.set_state(FSMclient.user_last_name)
    else:
        await message.delete()
        invalidName = await message.answer("❗️Նշեք իրական անունը:")
        await state.set_state(FSMclient.user_first_name)
        time.sleep(2)
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id= invalidName.message_id)
        
     
        
async def handle_last_name(message: Message, state: FSMContext):
    if (message.text == message.from_user.last_name) or message.text.lower() == "pass":
        await state.update_data(user_last_name=message.text)
        await message.delete()
        global question_3
        question_3 = await bot.edit_message_text(text='📝3/5: Լավ, իսկ հիմա նշեք ձեր տարիքը:\
            \n\nԳրանցումը դադարեցնելու համար սեղմեք -> /cancel', 
           chat_id=message.chat.id, 
           message_id=question_2.message_id)
        await state.set_state(FSMclient.user_age)
    else:
        await message.delete()
        invalidLastName = await message.answer("❗️Նշեք իրական ազգանունը կամ գրեք 'pass':\
            \n\nԳրանցումը դադարեցնելու համար սեղմեք -> /cancel")
        await state.set_state(FSMclient.user_last_name)
        time.sleep(2)
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=invalidLastName.message_id)
        
        

async def handle_age(message: Message, state: FSMContext):
    from keyboards.inline_user_arm import gender_keyboard
    
    if message.text.isnumeric():
        if (int(message.text) > 5) and int(message.text) < 90:
            await state.update_data(user_age = int(message.text))
            await message.delete()
            await bot.edit_message_text(text='📝4/5:Գրեթե վերջացրել ենք գրանցումը 😄, խնդրում ենք նշել նաև ձեր սեռը🚺🚹:\
                \n\nԳրանցումը դադարեցնելու համար սեղմեք -> /cancel',
                    chat_id=message.chat.id,
                    message_id=question_3.message_id,
                    reply_markup=gender_keyboard()
                    )
            await state.set_state(FSMclient.user_gender)
        else:
            await message.delete()
            invalidAge = await message.answer("❗️Նշեք իրական տարիքը:")
            await state.set_state(FSMclient.user_age)
            time.sleep(2)
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id= invalidAge.message_id
            )
    else:
        await message.delete()
        invalidNumeric = await message.answer("❗️Օգտագործեք միայն թվեր:")
        await state.set_state(FSMclient.user_age)
        time.sleep(2)
        await bot.delete_message(
                chat_id=message.chat.id,
                message_id= invalidNumeric.message_id
            )



async def handle_gender(call: CallbackQuery,  state: FSMContext):
    from utils import sq_lite_db_users
    from keyboards.inline_user_arm import menu_arm
    
    await state.update_data(user_gender = call.data)
    await call.message.edit_text(
            "📝5/5: 🥳Շնորհակալություն, գրանցումը ավարտված է։\
            \n😃Արդեն կարող եք ազատ օգտվել ԲիբլոԳրամի📗 <b>բոլոր հնարավորություններից</b>:",
            reply_markup=menu_arm()
        )
    await state.set_state(FSMclient.user_id)
    await state.update_data(user_id=int(call.message.chat.id))

    await sq_lite_db_users.add_user(state)
    await state.clear()
    
    
    
    
    
    
async def register_client_registration(dp: Dispatcher):
    dp.callback_query.register(user_registration, Text("registration"))
    dp.message.register(FSM_cancel_client, Command(commands="cancel"))
    dp.message.register(handle_first_name, FSMclient.user_first_name)
    dp.message.register(handle_last_name, FSMclient.user_last_name)
    dp.message.register(handle_age, FSMclient.user_age)
    dp.callback_query.register(handle_gender, FSMclient.user_gender)    
    