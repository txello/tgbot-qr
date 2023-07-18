import sqlite3 # Модуль SQLITE3
import qrcode # Модуль QRcode
import conf # Файл конфигурации.

class SQL:
    
    def query(query):
        
        db = sqlite3.connect(conf.db)
         # файл Базы Данных.

        conn = db.cursor().execute(query)
         # выполняем запрос.
        
        db.commit()
         # завершаем запрос.
        
        return conn
         # возвращаем запрос.
    
    def fetchone(query):
        
        db = sqlite3.connect(conf.db)
         # файл Базы Данных.
        
        conn = db.cursor().execute(query).fetchone()
         # выполняем запрос и получаем данные из одного пользователя.
        
        db.commit()
         # завершаем запрос.
        
        return conn
         # возвращаем запрос.

class QR:
    def create(name,text):
        
        img = qrcode.make(text)
         # создаем QR код с текстом text
        img.save(conf.QR_path + conf.QR_prefix + '{}.png'.format(name))
         # сохраняем в путь:
        return conf.QR_path + conf.QR_prefix + '{}.png'.format(name)