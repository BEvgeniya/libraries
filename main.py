import requests
import os

from requests import HTTPError


def check_for_redirect(response):
    if response.status_code != 200:
        raise HTTPError("Achtung! Redirect detekted!!! Capitulir")


def save_book(book_id, response):
    filename = "id" + str(book_id) + ".txt"
    dirname = "books"

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(dirname + "\\" + filename, 'wb') as file:
        file.write(response.content)


def main():
    for id in range(10):
        book_id = id + 1
        url_book = "http://tululu.org/txt.php?id=" + str(book_id)

        response = requests.get(url_book, allow_redirects=False)
        try:
            response.raise_for_status()
            check_for_redirect(response)
            save_book(book_id, response)
        except HTTPError:
            print("Unable to download file ", url_book)


main()