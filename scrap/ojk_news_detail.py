import requests
from bs4 import BeautifulSoup
import logging

from scrap.common import *


def fetch_article_detail(Judul, path):
    response = fetch(path)
    soup = BeautifulSoup(response.text, 'html.parser')

    pdf_link_div = soup.find('span', {"class", "attachments"})
    if pdf_link_div is None:
        logging.warning('Failed to fetch article file for path ' + path)
        return

    pdf_link_element = pdf_link_div.find_all('a')
    for link in pdf_link_element:
        if link:
            pdf_filename = link.get_text(strip=True)
            if "pdf" not in pdf_filename:
                logging.warning('Fail not pdf ' + path)
                continue

            pdf_url = f"{base_url}{link['href']}"
            return {
                "Judul": Judul,
                "NamaFile": pdf_filename,
                "Filepath": pdf_url,
            }

    return None

def fetch(path):
    url = f"{base_url}{path}"

    session = requests.Session()
    return session.post(url)
