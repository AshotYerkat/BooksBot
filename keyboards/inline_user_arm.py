from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_inline():
    markup = InlineKeyboardBuilder()
    markup.button(
        text="🇦🇲Հայերեն", callback_data="arm_start"
    )
    markup.button(
        text="🇷🇺Русский (В РАЗРАБОТКЕ)", callback_data="rus_start"
    )
    markup.button(
        text="🇬🇧English (IN DEVELOPING)", callback_data="eng_start"
    )
    markup.adjust(1)
    return markup.as_markup()


def menu_arm():
    menu_markup = InlineKeyboardBuilder()

    menu_markup.button(
        text="🔙 🇷🇺/🇦🇲 Փոխել լեզուն", callback_data="language_choice"
    )
    
    menu_markup.button(
        text="📙Գրքերի Ժանրերի ցանկը", callback_data="genre_show"
    )
    
    menu_markup.button(
        text='🗣👥ՄԵր տելեգրամյան խումբը', url='https://t.me/+5FnqHw4DFC9iOGUy'
    )
    
    menu_markup.button(
        text="✍🏻📄Գրանցում", callback_data="registration"
    )
    
    menu_markup.button(
        text="🗑 Ջնջել օգտահաշիվը", callback_data="delete_account"
    )
    
    menu_markup.button(
        text="📨Հետադարձ կապ", url='https://t.me/Ashot_Poxpat'
    )
    
    menu_markup.button(
        text='💼Ադմինիստրատորի ռեժիմ', callback_data='admin_mode'
    )
    menu_markup.adjust(1)
    return menu_markup.as_markup()



def genre_list():
    from utils.callback_factory import Genre_Choice_CallbackFactory
    list_markup = InlineKeyboardBuilder()
    
    list_markup.button(
        text="🔙 Հետ վերադառնալ", callback_data="arm_start"
    )
    
    list_markup.button(
        text='🧙🏻‍♂️Ֆենտեզի',
        callback_data=Genre_Choice_CallbackFactory(
            action='choice', genre='fantasy_books'
        ),
    )
    
    list_markup.button(
        text="📙Վեպ/Վիպակ",
        callback_data=Genre_Choice_CallbackFactory(
            action="choice", genre="novel_books"
        ),
    )

    list_markup.button(
        text="🕵🏻‍♂️Դետեկտիվ",
        callback_data=Genre_Choice_CallbackFactory(
            action="choice", genre="detective_books"
        ),
    )
    
    list_markup.button(
        text='📒Մոտիվացիոն',
        callback_data=Genre_Choice_CallbackFactory(
            action='choice', genre='motivation_books'
        ),
    )

    list_markup.button(
        text="⚔️Պատմական",
        callback_data=Genre_Choice_CallbackFactory(
            action="choice", genre="history_books"
        ),
    )
    
    list_markup.button(
        text='😬Սարսափ/Թրիլեր',
        callback_data=Genre_Choice_CallbackFactory(
            action='choice', genre='horror_books'
        ),
    )
    
    list_markup.adjust(1)
    return list_markup.as_markup()



def control_button():
    from utils.callback_factory import NumbersCallbackFactory
    from utils.sq_lite_db_books import list_book, records_check, records_num

    builder = InlineKeyboardBuilder()
    
    if list_book[0] > 1:
        builder.button(
            text="<<", callback_data=NumbersCallbackFactory(action="change", value=-1)
        )
        
    builder.button(
        text=f'{list_book[0]}/{records_num()}',
        callback_data='none'
    )    
        
    if records_check() == True:
        builder.button(
            text=">>", callback_data=NumbersCallbackFactory(action="change", value=1)
        )

    builder.button(
        text="🔙Վերադառնալ հետ", callback_data=NumbersCallbackFactory(action="back")
    )
    
    if (list_book[0] == 1) or records_check() == False:
        builder.adjust(1)
        return builder.as_markup()
        
    else:
        builder.adjust(3, 1)
        return builder.as_markup()



def gender_keyboard():
    gender_markup = InlineKeyboardBuilder()
    gender_markup.button(
        text='🚹Արական', callback_data='male'
    )
    
    gender_markup.button(
        text='🚺Իգական', callback_data='female'
    )
    gender_markup.adjust(1)
    return gender_markup.as_markup()



def user_delete_kb():
    delete_markup = InlineKeyboardBuilder()
    delete_markup.button(
        text='☑️Հաստատել', callback_data='delete_user'
    )
    
    delete_markup.button(
    text="🔙 Հետ վերադառնալ", callback_data="arm_start"
    )
    delete_markup.adjust(1)
    return delete_markup.as_markup()
    