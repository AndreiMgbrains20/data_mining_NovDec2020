#Урок 5. Scrapy / ДЗ. Версия 1 - 14.12.2020
#Readme

'''
Источник https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113
вакансии удаленной работы.

Задача: Обойти с точки входа все вакансии и собрать след данные:
1. название вакансии
2. оклад (строкой от до или просто сумма)
3. Описание вакансии
4. ключевые навыки - в виде списка названий
5. ссылка на автора вакансии

Перейти на страницу автора вакансии, собрать данные:
1. Название
2. сайт ссылка (если есть)
3. сферы деятельности (списком)
4. Описание

Обойти и собрать все вакансии данного автора.
'''

'''
******
Files:
******

main.py
hw_05/spiders/hhru.py
hw_05/spiders/autoyoula.py
hw_05/settings.py
hw_05/pipelines.py 
hw_05/loaders.py
hw_05/items.py