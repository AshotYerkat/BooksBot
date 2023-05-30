from TelegramBot import bot
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import time
from handlers.admin_handler import admins_id, admins_username
from keyboards.admin_inline import admin_start


storage_admin = MemoryStorage()
class FSM_admin(StatesGroup):
    admin_id = State()
    username = State()
    
    
async def FSM_admin_cancel(message: Message, bot: Bot, state="*"):
    if state is None:
        return
    await state.clear()
    await message.delete()
    await bot.edit_message_text("❗️Գործընթացը դադարեցված է։",
                                chat_id=message.chat.id,
                                message_id=msg1.message_id,
                                reply_markup=admin_start())    
    
    
    
async def get_admin_id(call: CallbackQuery, state: FSMContext):
    global msg1
    msg1 = await call.message.edit_text(
                     text='Ուղարկեք օգտատիրոջ id-ն` նրան ադմինի արտոնություններ տալու համար։\
                         \n\nԳրանցումը դադարեցնելու համար սեղմեք -> /cancel_admin')
    await state.set_state(FSM_admin.admin_id)
    
    
        
async def check_id(message: Message, state: FSMContext):
    j = 0 
    while j < len(admins_id):
        if admins_id[j] != int(message.text):
            j =  j + 1
        elif admins_id[j] == int(message.text):
            return False
    
    
async def get_name(message: Message, state: FSMContext):
    if await check_id(message, state) == False:
        await message.delete()
        InvalidID = await message.answer('Այդպիսի id-ով մոդերատոր արդեն գոյություն ունի')
        await state.set_state(FSM_admin.admin_id)
        time.sleep(2)
        await bot.delete_message(chat_id=message.chat.id,
                                     message_id=InvalidID.message_id)
    else:   
        if message.text.isnumeric():
            await state.update_data(admin_id = int(message.text))
            await message.delete()
            global msg2
            msg2 = await bot.edit_message_text(text='Շատ լավ, իսկ հիմա նշեք ադմինի անունը (կամ username)\
            \n\nԳրանցումը դադարեցնելու համար սեղմեք -> /cancel_admin։',
                                    chat_id=message.chat.id,
                                    message_id=msg1.message_id)
            await state.set_state(FSM_admin.username)
        
        else:
            await message.delete()
            InvalidID = await message.answer('Նշեք իրական գործող id-ն')
            await state.set_state(FSM_admin.admin_id)
            time.sleep(2)
            await bot.delete_message(chat_id=message.chat.id,
                                 message_id= InvalidID.message_id)
       
     
     
async def finish_admin_add(message: Message, state: FSMContext):
    await state.update_data(username = message.text)
    await message.delete()
    await bot.edit_message_text(text="Շնորհակալություն, գրանցումը ավարտված է։",
                                    chat_id=message.chat.id,
                                    message_id=msg2.message_id,
                                    reply_markup=admin_start()
                                    )
        
    data = await state.get_data()
    admin_id = data['admin_id']
    username = data['username']
    admins_id.append(admin_id)
    admins_username.append(username)
    await state.clear()
    
    
    
async def show_admins(call: CallbackQuery):
    await call.message.edit_text(text='Համակարգում գրանցված ադմինները։',
                                 reply_markup=admin_start())
    i = 0
    while i < len(admins_id):
        await call.message.answer(text=f'<b>ID</b>: {admins_id[i]}\
                                    \n<b>username</b>: {admins_username[i]}')
        await call.answer()
        i = i + 1
        



class AdminsList(StatesGroup):
    admin_id = State()


async def admin_delete(call: CallbackQuery, state: FSMContext):
    global del_admin
    await call.message.delete()
    del_admin = await call.message.answer(text='Ուղարկեք այն մոդերատորի id-ն, որին\
        \nցանկանում եք հեռացնել մոդերատորների ցանկից:\
            \n\nԳրանցումը դադարեցնելու համար սեղմեք -> /cancel_admin')
    await state.set_state(AdminsList.admin_id)
    
    
    
async def admin_del_func(message: Message, state: FSMContext):
    j = 0
    while j < len(admins_id):
        if message.text.isnumeric():
            if int(admins_id[j]) == int(message.text): 
                await state.update_data(admin_id = message.text)
                await message.delete()
                admins_id.pop(j)
                admins_username.pop(j)
                await bot.edit_message_text(text='Գործողությունը հաջողությամբ ավարտված է։',
                                            chat_id=message.chat.id,
                                            message_id=del_admin.message_id,
                                            reply_markup=admin_start())
                await state.clear()
            else:
                j = j + 1
        else:
            await message.delete()
            InvalidID = await message.answer('Նշեք իրական գործող id-ն')
            await state.set_state(AdminsList.admin_id)
            time.sleep(2)
            await bot.delete_message(chat_id=message.chat.id,
                                 message_id= InvalidID.message_id)
            
         
    

async def register_admins(dp: Dispatcher):
    dp.message.register(FSM_admin_cancel, Command(commands='cancel_admin'))
    dp.callback_query.register(get_admin_id, Text('add_admin'))
    '''dp.message.register(check_id, Message)'''
    dp.message.register(get_name, FSM_admin.admin_id)
    dp.message.register(finish_admin_add, FSM_admin.username)
    dp.callback_query.register(show_admins, Text('show_admins'))
    dp.callback_query.register(admin_delete, Text('remove_admin'))
    dp.message.register(admin_del_func, AdminsList.admin_id)
    
    