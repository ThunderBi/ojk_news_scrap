import requests
from bs4 import BeautifulSoup

from model.pengumuman_ojk import *
from model.pengumuman_ojk_file import *
from scrap.common import *
from scrap.ojk_news_detail import fetch_article_detail

count = 0
is_first_pagination = True


def call_ojk_news(request):
    global count
    logging.info(f"Running page {count +1}")
    count += 1

    response = fetch(request)
    articles = get_ojk_articles(response)

    urls = [article['url'] for article in articles]
    exist_articles = get_url_by_urls(urls)
    exist_urls = [article[0] for article in exist_articles]

    save_articles = []
    save_file = []
    need_fetch_next = True

    for article in articles:
        if article['url'] in exist_urls:
            logging.info(f"Stop because last article in db {article['url']}")
            need_fetch_next = False
            break

        file = fetch_article_detail(article['Judul'], article['url'])
        save_articles.append(article)
        if file is not None:
            save_file.append(file)

    if save_articles:
        save_bulk(save_articles)

    if save_file:
        save_bulk_file(save_file)

    if need_fetch_next:
        fetch_next(request, response)


def get_next_event_target(request):
    global is_first_pagination

    page = request.get('__EVENTTARGET')
    if not page:
        return "ctl00$PlaceHolderMain$ctl00$DataPagerArticles$ctl01$ctl01"

    base_page = page.rsplit('$', 1)[0]
    current_page_number = int(page.split('$')[-1].replace('ctl', ''))
    next_page = current_page_number + 1

    if is_first_pagination and next_page > 10:
        next_page -= 9
    if next_page > 11:
        next_page -= 10

    return f"{base_page}$ctl{next_page:02d}"


def fetch_next(request, response):
    soup = BeautifulSoup(response.content, 'html.parser')

    if soup.find('a', {'class': 'aspNetDisabled bluebutton'}, text='Last'):
        return

    viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
    eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
    viewstategenerator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']

    payload = {
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategenerator,
        '__EVENTVALIDATION': eventvalidation,
        '__EVENTTARGET': get_next_event_target(request),
        '__EVENTARGUMENT': ''
    }

    call_ojk_news(payload)


def get_ojk_articles(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    article_elements = soup.find_all('div', {"class": "article-list-view-wrap"})

    articles = []
    for article_element in article_elements:
        title_element = article_element.find('a')
        date_element = article_element.find('span', {"class": "date"})
        description_element = article_element.find('p', {"class": "descr"})

        articles.append({
            "Judul": title_element.get_text(strip=True),
            "url": title_element.get('href'),
            "Date": convert_date(date_element.get_text(strip=True)),
            "Detail": description_element.get_text(strip=True)
        })

    return articles


def fetch(request):
    url = f"{base_url}/id/berita-dan-kegiatan/pengumuman/default.aspx"

    session = requests.Session()
    return session.post(url, data=request)
