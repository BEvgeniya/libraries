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


def parse_book_page(soup, url_site):
    book_page = []

    return book_page

def parse_title(soup):
    header = soup.find('h1')

    titles = header.text.split('::')
    if len(titles) == 0:
        title = header.text
        author = ''
    else:
        title = titles[0]
        author = titles[-1]

    return title.strip(), author.strip()


def parse_image_url(soup, url_site):
    image_path = soup.find('div', class_='bookimage').find('img')['src']
    image_url = urljoin(url_site, image_path)

    return image_url


def parse_comments(soup):
    comments_result = []
    comments = soup.find_all('div', class_='texts')
    for comment in comments:
        comment_text = comment.find('span').text
        comments_result.append(comment_text)
    return comments_result


def parse_genres(soup):
    result = []
    genres = soup.find('span', class_='d_book').find_all('a')
    for genre in genres:
        genre_text = genre.text
        result.append(genre_text)
    return result


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


def parse_book_page(url_site):
    book_page = {}

    response = http_request(url_site)
    if response == None:
        return book_page

    soup = BeautifulSoup(response.text, 'lxml')
    book_page['title'], book_page['author'] = parse_title(soup)
    book_page['image_url'] = parse_image_url(soup, url_site)
    book_page['comments'] = parse_comments(soup)
    book_page['genres'] = parse_genres(soup)
    return book_page


def main():
    for id in range(10):
        book_id = id + 1
        url_site = "https://tululu.org/b" + str(book_id) + '/'
        parse_book_page(url_site)

        # if title != '':
        #     url_book = "https://tululu.org/txt.php?id=" + str(book_id)
        #     download_txt(url_book, book_id, title)
        #
        # if image_url != '':
        #     download_image(image_url, book_id)


main()


