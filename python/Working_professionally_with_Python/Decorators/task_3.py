import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from task_2 import logger

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

@logger('log_scraping.log')
def fetch_and_filter_news_by_keywords(keywords: list, num_pages: int, search_in_articles=False):
    """
    Парсит статьи с сайта HABR и фильтрует их по заданным ключевым словам в заголовках.
    Опционально ищет ключевые слова в тексте статьи.

    Args:
        keywords (list of str): Список ключевых слов для поиска в заголовках и/или тексте статей.
        num_pages (int): Количество страниц, которые будут парситься.
        search_in_articles (bool): Флаг, указывающий, следует ли искать ключевые слова
        в тексте статей.

    Returns:
        None: Функция выводит в консоль информацию о статьях, содержащих ключевые слова.
    """
    base_url = 'https://habr.com'
    articles_found = []

    for page in range(1, num_pages + 1):
        print(f'Обрабатываем страницу {page}')

        response = requests.get(base_url + f'/ru/articles/page{page}')
        response.raise_for_status()

        soup = bs(response.text, features='html.parser')
        articles = soup.findAll('div', class_='tm-article-snippet')

        for article in articles:
            title = article.find('a', class_='tm-title__link').find('span').text
            link = base_url + article.find('a', class_='tm-title__link').get('href')
            date_ = article.find('time').get('title').split(',')

            if search_in_articles:
                if search_keywords_in_text(link, keywords):
                    articles_found.append((date_[0], title, link))

            elif any(keyword.lower() in title.lower() for keyword in keywords):
                articles_found.append((date_[0], title, link))

    for date, title, link in articles_found:
        print(date, title, link)
    print(f'Найдено {len(articles_found)} статей ')



def search_keywords_in_text(link: str, keywords: list) -> bool:
    """
    Ищет ключевые слова в тексте статьи по указанной ссылке.

    Args:
        link (str): Ссылка на статью.
        keywords (list of str): Список ключевых слов для поиска.

    Returns:
        bool: True, если ключевые слова найдены в тексте статьи, иначе False.
    """
    response = requests.get(link)
    response.raise_for_status()

    soup = bs(response.text, features='html.parser')
    article_text = soup.find('div', class_='tm-article-body').text

    return any(keyword.lower() in article_text.lower() for keyword in keywords)


if __name__ == '__main__':
    fetch_and_filter_news_by_keywords(KEYWORDS, 5, search_in_articles=False)
