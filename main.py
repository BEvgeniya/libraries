import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests import HTTPError


def check_for_redirect(response):
    if response.status_code != 200:
        raise HTTPError("Achtung! Redirect detekted!!! Capitulir")


def download_txt(url, filename, folder='books'):
    # """Функция для скачивания текстовых файлов.
    # Args:
    #     url (str): Cсылка на текст, который хочется скачать.
    #     filename (str): Имя файла, с которым сохранять.
    #     folder (str): Папка, куда сохранять.
    # Returns:
    #     str: Путь до файла, куда сохранён текст.
    # """

    response = requests.get(url, allow_redirects=True)
    try:
        response.raise_for_status()
    except HTTPError:
        print("Unable to download file ", url)

    # soup = BeautifulSoup(response.text, 'lxml')
    # header = soup.find('h1')
    # title, author = header.text.split('::')

    filename = sanitize_filename(filename) + '.txt'
    folder = sanitize_filename(folder)

    filepath = os.path.join(folder, filename)

    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


# def main():
    # for id in range(10):
    #     book_id = id + 1
    #     url_book = "http://tululu.org/txt.php?id=" + str(book_id)
    #
    #     response = requests.get(url_book, allow_redirects=False)
    #     try:
    #         response.raise_for_status()
    #         check_for_redirect(response)
    #         save_book(book_id, response)
    #     except HTTPError:
    #         print("Unable to download file ", url_book)


def test():
    # Примеры использования
    url = 'http://tululu.org/txt.php?id=1'

    filepath = download_txt(url, 'Алиби')
    print(filepath)  # Выведется books/Алиби.txt

    filepath = download_txt(url, 'Али/би', folder='books/')
    print(filepath)  # Выведется books/Алиби.txt

    filepath = download_txt(url, 'Али\\би', folder='txt/')
    print(filepath)  # Выведется txt/Алиби.txt


# main()
test()