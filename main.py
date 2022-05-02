import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests import HTTPError
from urllib.parse import urljoin
from urllib.parse import urlparse

def check_for_redirect(url, response):
    if url != response.url:
        raise HTTPError("Redirect detected. Download canceled")


def http_request(url):
    response = requests.get(url, allow_redirects=True)
    try:
        response.raise_for_status()
        check_for_redirect(url, response)
    except HTTPError as e:
        print("Unable to download file ", url, ' cause ', str(e))
        return None

    return response

def parse_title(soup):
    header = soup.find('h1')

    titles = header.text.split('::')
    if len(titles) == 0:
        title = header.text
    else:
        title = titles[0]

    return title


def parse_image_url(soup, url_site):
    image_path = soup.find('div', class_='bookimage').find('img')['src']
    image_url = urljoin(url_site, image_path)

    return image_url

def parse_comments(soup):
    comments = soup.find_all('div', class_='texts')
    for comment in comments:
        comment_text = comment.find('span').text
        print(comment_text)


def download_txt(url, book_id, title,  folder='books'):

    title = sanitize_filename(title.strip())
    folder = sanitize_filename(folder.strip())

    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = str(book_id) + '. ' + title + '.txt'
    filepath = os.path.join(folder, filename)

    response = http_request(url)
    if response == None:
        return ''

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def download_image(url, book_id, folder='images'):
    parse_result = urlparse(url)
    image_name = os.path.basename(parse_result.path)

    image_name = sanitize_filename(image_name.strip())
    folder = sanitize_filename(folder.strip())

    if not os.path.exists(folder):
        os.makedirs(folder)

    filepath = os.path.join(folder, image_name)

    response = http_request(url)
    if response == None:
        return ''

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def main():
    for id in range(10):
        book_id = id + 1
        url_site = "https://tululu.org/b" + str(book_id) + '/'

        response = http_request(url_site)
        if response == None:
            continue

        soup = BeautifulSoup(response.text, 'lxml')
        title = parse_title(soup)
        image_url = parse_image_url(soup, url_site)
        parse_comments(soup)

        if title != '':
            url_book = "https://tululu.org/txt.php?id=" + str(book_id)
            download_txt(url_book, book_id, title)

        if image_url != '':
            download_image(image_url, book_id)


main()


