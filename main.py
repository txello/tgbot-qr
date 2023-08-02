import telebot # Модуль Telebot
from telebot import types # Модуль Telebot: Функция types
from lib import SQL, QR, conf # Файл lib: Функции SQL и QR, Файл конфигурации.
from lang import Lang # Файл lang
###     name - telegram Bot QR
###     author - txello
###     version - 1.0


bot = telebot.TeleBot(conf.API) # Доступ к API бота



@bot.message_handler(commands = ['start']) # /start
def start(message):
    
    conn = SQL.fetchone('SELECT {}, {} FROM {} WHERE {}=\'{}\''.format(conf.db_names[0],conf.db_names[1],conf.db_table,conf.db_names[0],message.from_user.id))
     # получаем данные пользователя.
     
    if conn:
     # ЕСЛИ пользователь существует:
        if conn[1] == 1:
         # ЕСЛИ язык пользователя Русский:
            bot.send_message(message.from_user.id, Lang.Rus('a1'))
             # отправляем сообщение.

        elif conn[1] == 2:
         # ЕСЛИ язык пользователя Английский:
            bot.send_message(message.from_user.id, Lang.Eng('a1'))
             # отправляем сообщение.

    else:
     # ЕСЛИ пользователя не существует:
        a = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton(text='🇷🇺 Русский',callback_data='ru')
        btn2 = types.InlineKeyboardButton(text='🇬🇧 English',callback_data='en')
        a.add(btn1,btn2)
         # создаем кнопки.
         
        bot.send_message(message.from_user.id,  "Your language:",  reply_markup=a)
         # отправляем сообщение.



@bot.message_handler(commands = ['lang']) # /lang
def lang(message):
    
    conn = SQL.fetchone('SELECT {}, {} FROM {} WHERE {}=\'{}\''.format(conf.db_names[0],conf.db_names[1],conf.db_table,conf.db_names[0],message.from_user.id))
     # получаем данные пользователя.
    
    a = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text='🇷🇺 Русский',callback_data='ru')
    btn2 = types.InlineKeyboardButton(text='🇬🇧 English',callback_data='en')
    a.add(btn1,btn2)
     # создаем кнопки.
    
    if conn:
     # ЕСЛИ пользователь существует:
        if conn[1] == 1:
         # ЕСЛИ язык пользователя Русский:
            bot.send_message(message.from_user.id,  Lang.Rus('a0'),  reply_markup=a)
             # отправляем сообщение.
        
        if conn[1] == 2:
         # ЕСЛИ язык пользователя Английский:
            bot.send_message(message.from_user.id,  Lang.Rus('a1'),  reply_markup=a)
             # отправляем сообщение.
    
    else:
     # ЕСЛИ пользователь не существует:
        start(message)
         # /start



@bot.message_handler(content_types='text') # Любое текстовое сообщение
def qr(message):

    conn = SQL.fetchone('SELECT {}, {} FROM {} WHERE {}=\'{}\''.format(conf.db_names[0],conf.db_names[1],conf.db_table,conf.db_names[0],message.from_user.id))
     # получаем данные пользователя.
    
    if conn:
     # ЕСЛИ пользователь существует:
        if conn[1] == 1:
         # ЕСЛИ язык пользователя Русский:
            bot.send_photo(message.from_user.id, open(QR.create(message.from_user.id,message.text),'rb'),Lang.Rus('a2'))
             # отправляем сообщение с QR кодом.
        
        elif conn[1] == 2:
         # ЕСЛИ язык пользователя Английский:
            bot.send_photo(message.from_user.id, open(QR.create(message.from_user.id,message.text),'rb'),Lang.Eng('a2'))
             # отправляем сообщение с QR кодом.
    else:
     # ЕСЛИ пользователь не существует:
        start(message)
         # /start
    


@bot.callback_query_handler(func=lambda call:True) # Кнопки
def callback(call):
    
    if call.message:
     # ЕСЛИ кнопка нажата:
    
        conn = SQL.fetchone('SELECT {}, {} FROM {} WHERE {}=\'{}\''.format(conf.db_names[0],conf.db_names[1],conf.db_table,conf.db_names[0],call.message.chat.id))
         # получаем данные пользователя.
        
        if call.data == 'ru':
         # ЕСЛИ нажата кнопка 'Русский':
            if conn:
             # ЕСЛИ пользователь существует:
                 SQL.query('UPDATE {} SET {}=\'{}\' WHERE {}=\'{}\''.format(conf.db_table,conf.db_names[1],1,conf.db_names[0],call.message.chat.id))
                 # изменяем в Базе Данных значение на новое.
            
            else:
             # ЕСЛИ пользователь не существует:
                SQL.query('INSERT INTO {} ({},{}) VALUES({},{})'.format(conf.db_table,conf.db_names[0],conf.db_names[1],call.message.chat.id,1))
                 # назначаем в Базе Данных новое значение.
            
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id, text=Lang.Rus('a0')+Lang.Rus('a0_1'))
             # меняем сообщение на нужное.
            
            bot.send_message(call.message.chat.id, Lang.Rus('a1'))
             # отправляем сообщение.
            
        if call.data == 'en':
         # ЕСЛИ нажата кнопка 'Английский':
            if conn:
             # ЕСЛИ пользователь существует:
                SQL.query('UPDATE {} SET {}=\'{}\' WHERE {}=\'{}\''.format(conf.db_table,conf.db_names[1],2,conf.db_names[0],call.message.chat.id))
                 # изменяем в Базе Данных значение на новое.
            
            else:
             # ЕСЛИ пользователь не существует:
                SQL.query('INSERT INTO {} ({},{}) VALUES({},{})'.format(conf.db_table,conf.db_names[0],conf.db_names[1],call.message.chat.id,2))
                 # назначаем в Базе Данных новое значение.
            
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id, text=Lang.Eng('a0')+Lang.Eng('a0_1'))
             # меняем сообщение на нужное.

            bot.send_message(call.message.chat.id, Lang.Eng('a1'))
            # отправляем сообщение.
            
bot.polling(none_stop=True, interval=0)
# заставляем бота не прекращать работу.
