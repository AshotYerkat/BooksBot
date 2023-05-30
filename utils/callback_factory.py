from typing import Optional
from aiogram.filters.callback_data import CallbackData

class NumbersCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int]
    

class Genre_Choice_CallbackFactory(CallbackData, prefix='choice'):
    action: str
    genre: str