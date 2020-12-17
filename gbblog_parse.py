# Lesson 03. Home work. Vers.1
# Урок 3. Системы управления базами данных MongoDB и SQLite в Python

"""Задание
Необходимо обойти все записи в блоге и извлеч из них информацию следующих полей:
url страницы материала
Заголовок материала
Первое изображение материала (Ссылка)
Дата публикации (в формате datetime)
имя автора материала
ссылка на страницу автора материала
комментарии в виде (автор комментария и текст комментария)
писок тегов
реализовать SQL структуру хранения данных c следующими таблицами
    Post
    Comment
    Writer
    Tag
Организовать реляционные связи между таблицами
При сборе данных учесть, что полученый из данных автор уже может быть в БД и значит необходимо это заблаговременно проверить.
Не забываем закрывать сессию по завершению работы с ней
"""
#gbblog_parse.py, database.py, models.py

from typing import Tuple, Set
import bs4
import requests
from urllib.parse import urljoin
from database import GBDataBase
import datetime

class GbBlogParse:

    def __init__(self, start_url):
        self.start_url = start_url
        self.page_done = set()
        self.db = GBDataBase('sqlite:///gb_blog.db')

    def _get(self, url):
        response = requests.get(url)
        self.page_done.add(url)
        return bs4.BeautifulSoup(response.text, 'lxml')

    def get_datetime(self, soup):
        format = "%Y-%m-%dT%H:%M:%S"
        f_data = soup.find('div', attrs={'class': 'blogpost-date-views'}).time['datetime'].split('+')[0]
        return datetime.datetime.strptime(f_data, format)

    def get_tag(self, soup):
        tags = []
        for tag in soup.find_all('a', attrs={'class': "small"}):
            tag_data = {
                'url': urljoin(self.start_url, tag.get('href')),
                'name': tag.text
            }
            tags.append(tag_data)
        return tags

    def get_img_url(self, soup):
        try:
            img_url = soup.find('div', attrs={'class': 'blogpost-content'}).img['src']
        except TypeError:
            img_url = None
        return img_url

    def get_comments(self, soup):
        url_id = soup.find('div', attrs={'class': 'm-t-xl'}).comments['commentable-id']
        param = {
            'commentable_type': 'Post',
            'commentable_id': int(url_id),
            'order': 'desc'
        }
        comments = requests.get('https://geekbrains.ru/api/v2/comments', param).json()
        comments_list = []

        def g_c(comment):
            for i in comment:
                name = i['comment']['user']['full_name']
                text = i['comment']['body']
                comments_list.append([name, text])
                if i['comment']['children'] != []:
                    g_c(i['comment']['children'])
        g_c(comments)
        return comments_list

    def run(self, url=None):
        if not url:
            url = self.start_url

        if url not in self.page_done:
            soup = self._get(url)
            posts, pagination = self.parse(soup)
            for post_url in posts:
                page_data = self.page_parse(self._get(post_url), post_url)
                # print(page_data['post_data']['title'])
                self.save(page_data)
            for pag_url in pagination:
                self.run(pag_url)

    def parse(self, soup) -> Tuple[Set[str], Set[str]]:
        pag_ul = soup.find('ul', attrs={'class': 'gb__pagination'})
        paginations = set(
            urljoin(self.start_url, p_url.get('href')) for p_url in pag_ul.find_all('a') if p_url.get('href')
        )
        posts_wrapper = soup.find('div', attrs={'class': 'post-items-wrapper'})

        posts = set(
            urljoin(self.start_url, post_url.get('href')) for post_url in
            posts_wrapper.find_all('a', attrs={'class': 'post-item__title'})
        )

        return posts, paginations

    def page_parse(self, soup, url) -> dict:

        data = {
            'post_data': {
                'url': url,
                'title': soup.find('h1', attrs={'class': 'blogpost-title'}).text,
                'img_url': self.get_img_url(soup),
                'date_time': self.get_datetime(soup)
            },
            'writer': {
                'name': soup.find('div', attrs={'itemprop': 'author'}).text,
                'url': urljoin(self.start_url, soup.find('div', attrs={'itemprop': 'author'}).parent.get('href'))
            },
            'tags': self.get_tag(soup),
            'comments': []
        }

#Переделать. Память используется не оптимально!!!
        for comment in  self.get_comments(soup):
            com_data = {
                # 'url': data['post_data']['url'],
                'name': comment[0],
                'text': comment[1]
            }
            data['comments'].append(com_data)

        return data

    def save(self, post_data: dict):
        self.db.create_post(post_data)


if __name__ == '__main__':
    parser = GbBlogParse('https://geekbrains.ru/posts')
    parser.run()
