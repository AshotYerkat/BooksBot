from aiogram.utils.keyboard import InlineKeyboardBuilder



def admin_start():
    start = InlineKeyboardBuilder()
    start.button(
        text='📚Ավելացնել գիրք', callback_data='add_book'
        )
    
    start.button(
        text='🧑🏻‍💻Ավելացնել ադմին', callback_data='add_admin'
        )
    
    start.button(
        text="🧑🏻‍💻Հեռացնել ադմինին", callback_data='remove_admin'
        )
    
    start.button(
        text="🧑🏻‍💻Տեսնել ադմինների ցանկը", callback_data='show_admins'
        )
    
    start.button(
        text='🔙Հետ վերադառնալ', callback_data='arm_start'
        )
    
    start.adjust(1)
    return start.as_markup()
    

    
def genre_choice():
    builder =  InlineKeyboardBuilder()
    builder.button(
        text = 'Պատմական ժանրում', callback_data='history_books'
        )
    
    builder.button(
        text = 'Դետեկտիվ ժանրում', callback_data='detective_books'
        )
    
    builder.button(
        text='Վեպ/Վիպակ', callback_data='novel_books'
        )
    
    builder.adjust(1)
    return builder.as_markup()    


