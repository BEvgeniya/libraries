import requests
import os

url = "https://dvmn.org/filer/canonical/1542890876/16/"

response = requests.get(url)
response.raise_for_status()

filename = 'dvmn.svg'
with open(filename, 'wb') as file:
    file.write(response.content)

for id in range(10):
    book_id = id + 1
    url_book = "http://tululu.org/txt.php?id=" + str(book_id)

    response = requests.get(url_book)
    response.raise_for_status()

    filename = "id" + str(book_id) + ".txt"

    dirname = "books"
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(dirname + "\\" + filename, 'wb') as file:
        file.write(response.content)
