import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests import HTTPError


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

def parse_title(url, book_id, folder='books'):
    response = http_request(url)
    if response == None:
        return ''

    soup = BeautifulSoup(response.text, 'lxml')
    header = soup.find('h1')

    titles = header.text.split('::')
    if len(titles) == 0:
        title = header.text
    else:
        title = titles[0]

    title = sanitize_filename(title.strip())
    folder = sanitize_filename(folder.strip())

    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = str(book_id) + '. ' + title + '.txt'

    return os.path.join(folder, filename)


def download_txt(url, filepath):
    # """Функция для скачивания текстовых файлов.
    # Args:
    #     url (str): Cсылка на текст, который хочется скачать.
    #     filepath (str): Полный путь сохраняемого файла
    # Returns:
    #     str: Путь до файла, куда сохранён текст. Имя файла формируется из заголовка скачанной книги
    # """

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
        filename = parse_title(url_site, book_id)

        if filename != '':
            url_book = "https://tululu.org/txt.php?id=" + str(book_id)
            download_txt(url_book, filename)


main()


