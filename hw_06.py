#Урок 6. Scrapy. Парсинг фото и файлов / ДЗ. Версия 1 - 16.12.2020
#Источник instgram
#Readme

'''
Задача авторизованным пользователем обойти список произвольных тегов,
Сохранить структуру Item олицетворяющую сам Tag (только информация о теге)

Сохранить структуру данных поста, Включая обход пагинации. (каждый пост как отдельный item, словарь внутри node)

Все структуры должны иметь след вид

    date_parse (datetime) время когда произошло создание структуры
    data - данные полученые от инстаграм

Скачать изображения всех постов и сохранить на диск



******
Files:
******

/gb_parse/spiders/autoyoula.py
/gb_parse/spiders/hhru.py
/gb_parse/spiders/__init__.py
/gb_parse/spiders/instagram.py
/gb_parse/items.py
/gb_parse/loaders.py
/gb_parse/middlewares.py 
/gb_parse/pipelines.py 
/gb_parse/settings.py
main.py
scrapy.cfg

'''
