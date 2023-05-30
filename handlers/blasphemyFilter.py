from aiogram import types, Dispatcher, Bot
import json, string


async def blasphemy_filter(message : types.Message, bot: Bot):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('badwords.json')))) != set():
            await message.reply('Матерные слова в чате запрещены❌')
            await message.delete()
            
            

async def register_blasphemy_handlers(dp: Dispatcher):
    dp.message.register(blasphemy_filter)