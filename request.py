from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent


async def book_information(book):
    genre = book.find("div", class_="articles__item--topline").find("a")
    finished_genre = genre.text.strip()

    book_name = book.find("a", class_="content__article-main-link").find("h2")
    book_name_finished = book_name.text.strip()

    book_description = book.find("a", class_="content__article-main-link").find("span")
    book_description_finished = book_description.text.strip()

    author = book.find("div", class_="additional-info").find("div", class_="oneline")
    author_continue = author.find("span", class_="link__action").find("a")
    author_finished = author_continue.text.strip()

    performer = book.find("div", class_="additional-info").find("div", class_="oneline")
    performer_continue = performer.find_all("span", class_="link__action")
    performer_finished = performer_continue[1].find("a").text.strip()

    time = book.find("div", class_="additional-info").find("div", class_="oneline")
    time_continue = time.find("span", class_="link__action--label--time").find_all("span")
    time_finished = time_continue[0].text + ' ' + time_continue[1].text

    photo_url = book.find("div", class_="container__remaining-width").find("a")
    photo_url_finished = photo_url.find("img").get("src")

    book_url = book.find("div", class_="container__remaining-width").find("a")
    book_url_finished = book_url.get("href")

    information = {'genre': finished_genre, 'book_name': book_name_finished,
                   'book_description': book_description_finished, 'author': author_finished,
                   'performer': performer_finished, 'time': time_finished, 'photo_url': photo_url_finished,
                   'book_url': book_url_finished}

    return information


async def find_book(answer, bot, message):
    adapted_answer = answer.replace(' ', '%20')
    ua = UserAgent()
    response = requests.get(
        url=f'https://akniga.org/search/books?q={adapted_answer}',
        headers={'user-agent': f'{ua.random}'}
    )

    soup = BeautifulSoup(response.content, "lxml")
    paging = soup.find("div", class_="paging")
    books = soup.find_all("div", class_="content__main__articles--item")

    for book in books:
        info = await book_information(book)

        await bot.send_photo(chat_id=message.from_user.id, photo=info.get("photo_url"),
                             caption=f'Автор: {info.get("author")}\nНазвание книги: {info.get("book_name")}\n'
                                     f'Жанр: {info.get("genre")}\nИсполнитель: {info.get("performer")}\n'
                                     f'Длительность книги: {info.get("time")}\n'
                                     f'Описание: {info.get("book_description")}\n'
                                     f'Ссылка: {info.get("book_url")}')

    if paging:
        return paging.find("a", class_='page__nav--next').get('href')
    else:
        return None


async def next_page(url, bot, message):
    ua = UserAgent()
    response = requests.get(
        url=url,
        headers={'user-agent': f'{ua.random}'}
    )

    soup = BeautifulSoup(response.content, "lxml")
    paging = soup.find("div", class_="paging")
    books = soup.find_all("div", class_="content__main__articles--item")

    for book in books:
        info = await book_information(book)

        await bot.send_photo(chat_id=message.from_user.id, photo=info.get("photo_url"),
                             caption=f'Автор: {info.get("author")}\nНазвание книги: {info.get("book_name")}\n'
                                     f'Жанр: {info.get("genre")}\nИсполнитель: {info.get("performer")}\n'
                                     f'Длительность книги: {info.get("time")}\n'
                                     f'Описание: {info.get("book_description")}\n'
                                     f'Ссылка: {info.get("book_url")}')

    if paging:
        return paging.find("a", class_='page__nav--next').get('href')
    else:
        return None
