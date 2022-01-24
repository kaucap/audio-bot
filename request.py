import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


async def book_information(book):
    genre = book.find("div", class_="articles__item--topline").find("a")
    finished_genre = genre.text.strip()

    book_name = book.find("a", class_="content__article-main-link").find("h2")
    book_name_finished = book_name.text.strip()

    book_description = book.find("a", class_="content__article-main-link").find("span")
    book_description_finished = book_description.text.strip()

    author_and_performer_exist = book.find_all("span", class_="link__action")
    if len(author_and_performer_exist) == 3:
        author = book.find("div", class_="additional-info").find("div", class_="oneline")
        author_continue = author.find("span", class_="link__action").find("a")
        author_finished = author_continue.text.strip()
        performer = book.find("div", class_="additional-info").find("div", class_="oneline")
        performer_continue = performer.find_all("span", class_="link__action")
        performer_finished = performer_continue[1].find("a").text.strip()
    elif len(author_and_performer_exist) == 2:
        check_value = book.find_all("span", class_="link__action")
        check_value_finished = check_value[0].find("svg", class_="icon").find("use")
        if check_value_finished.get("xlink:href") == "#author":
            author = book.find("div", class_="additional-info").find("div", class_="oneline")
            author_continue = author.find("span", class_="link__action").find("a")
            author_finished = author_continue.text.strip()
            performer_finished = 'Неизвестный'
        elif check_value_finished.get("xlink:href") == "#performer":
            performer = book.find("div", class_="additional-info").find("div", class_="oneline")
            performer_continue = performer.find_all("span", class_="link__action")
            performer_finished = performer_continue[0].find("a").text.strip()
            author_finished = 'Неизвестный'
    else:
        author_finished = 'Неизвестный'
        performer_finished = 'Неизвестный'

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


async def give_book_info(response, bot, message):
    html = await response.text()
    soup = BeautifulSoup(html, "lxml")
    paging = soup.find("div", class_="paging")
    paging_exist = paging.find("a", class_='page__nav--next')
    books = soup.find_all("div", class_="content__main__articles--item")
    for book in books:
        info = await book_information(book)

        await bot.send_photo(chat_id=message.from_user.id, photo=info.get("photo_url"),
                             caption=f'Автор: {info.get("author")}\nНазвание книги: {info.get("book_name")}\n'
                                     f'Жанр: {info.get("genre")}\nИсполнитель: {info.get("performer")}\n'
                                     f'Длительность книги: {info.get("time")}\n'
                                     f'Описание: {info.get("book_description")}\n'
                                     f'Ссылка: {info.get("book_url")}')

    if paging_exist:
        return paging.find("a", class_='page__nav--next').get('href')
    else:
        return None


async def find_book(answer, bot, message):
    async with aiohttp.ClientSession() as session:
        adapted_answer = answer.replace(' ', '%20')
        ua = UserAgent()
        async with session.get(url=f'https://akniga.org/search/books?q={adapted_answer}',
                               headers={'user-agent': f'{ua.random}'}) as response:
            book_info = await give_book_info(response=response, bot=bot, message=message)
            return book_info


async def find_book_next_page(url, bot, message):
    async with aiohttp.ClientSession() as session:
        ua = UserAgent()
        async with session.get(url=url, headers={'user-agent': f'{ua.random}'}) as response:
            book_info = await give_book_info(response=response, bot=bot, message=message)
            return book_info


async def find_new_book(bot, message):
    async with aiohttp.ClientSession() as session:
        ua = UserAgent()
        async with session.get(url='https://akniga.org/index/',
                               headers={'user-agent': f'{ua.random}'}) as response:
            book_info = await give_book_info(response=response, bot=bot, message=message)
            return book_info


async def best_book_day(bot, message):
    async with aiohttp.ClientSession() as session:
        ua = UserAgent()
        async with session.get(url='https://akniga.org/index/top?period=1',
                               headers={'user-agent': f'{ua.random}'}) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "lxml")
            books = soup.find_all("div", class_="content__main__articles--item")

            for book in books:
                info = await book_information(book)

                await bot.send_photo(chat_id=message.from_user.id, photo=info.get("photo_url"),
                                     caption=f'Автор: {info.get("author")}\nНазвание книги: {info.get("book_name")}\n'
                                             f'Жанр: {info.get("genre")}\nИсполнитель: {info.get("performer")}\n'
                                             f'Длительность книги: {info.get("time")}\n'
                                             f'Описание: {info.get("book_description")}\n'
                                             f'Ссылка: {info.get("book_url")}')


async def best_book_week(bot, message):
    async with aiohttp.ClientSession() as session:
        ua = UserAgent()
        async with session.get(url='https://akniga.org/index/top?period=7',
                               headers={'user-agent': f'{ua.random}'}) as response:
            book_info = await give_book_info(response=response, bot=bot, message=message)
            return book_info


async def best_book_month(bot, message):
    async with aiohttp.ClientSession() as session:
        ua = UserAgent()
        async with session.get(url='https://akniga.org/index/top?period=30',
                               headers={'user-agent': f'{ua.random}'}) as response:
            book_info = await give_book_info(response=response, bot=bot, message=message)
            return book_info


async def best_book_all_time(bot, message):
    async with aiohttp.ClientSession() as session:
        ua = UserAgent()
        async with session.get(url='https://akniga.org/index/top?period=all',
                               headers={'user-agent': f'{ua.random}'}) as response:
            book_info = await give_book_info(response=response, bot=bot, message=message)
            return book_info


async def paid_book_new(bot, message):
    async with aiohttp.ClientSession() as session:
        ua = UserAgent()
        async with session.get(url='https://akniga.org/paid/',
                               headers={'user-agent': f'{ua.random}'}) as response:
            book_info = await give_book_info(response=response, bot=bot, message=message)
            return book_info


async def paid_book_best(bot, message):
    async with aiohttp.ClientSession() as session:
        ua = UserAgent()
        async with session.get(url='https://akniga.org/paid/top?period=all',
                               headers={'user-agent': f'{ua.random}'}) as response:
            book_info = await give_book_info(response=response, bot=bot, message=message)
            return book_info


async def paid_book_popular(bot, message):
    async with aiohttp.ClientSession() as session:
        ua = UserAgent()
        async with session.get(url='https://akniga.org/paid/discussed/?period=all',
                               headers={'user-agent': f'{ua.random}'}) as response:
            book_info = await give_book_info(response=response, bot=bot, message=message)
            return book_info


async def get_genre(data):
    genre = data["genre"]
    if genre == 'Фантастика 🛸':
        appropriate_genre = 'fantasy'
    elif genre == 'Детективы 🕵️‍♂️':
        appropriate_genre = 'detective'
    elif genre == 'Роман ❤️':
        appropriate_genre = 'roman'
    elif genre == 'Психология 📚':
        appropriate_genre = 'psihologiya'
    elif genre == 'Классика ✨':
        appropriate_genre = 'classic'
    else:
        appropriate_genre = 'uzhasy_mistika'

    return appropriate_genre


async def new_book_by_genre(bot, message, data):
    async with aiohttp.ClientSession() as session:
        genre = await get_genre(data)
        ua = UserAgent()
        async with session.get(url=f'https://akniga.org/section/{genre}/',
                               headers={'user-agent': f'{ua.random}'}) as response:
            book_info = await give_book_info(response=response, bot=bot, message=message)
            return book_info


async def best_book_by_genre(bot, message, data):
    async with aiohttp.ClientSession() as session:
        genre = await get_genre(data)
        ua = UserAgent()
        async with session.get(url=f'https://akniga.org/section/{genre}/top/?period=all',
                               headers={'user-agent': f'{ua.random}'}) as response:
            book_info = await give_book_info(response=response, bot=bot, message=message)
            return book_info


async def popular_book_by_genre(bot, message, data):
    async with aiohttp.ClientSession() as session:
        genre = await get_genre(data)
        ua = UserAgent()
        async with session.get(url=f'https://akniga.org/section/{genre}/discussed/?period=all',
                               headers={'user-agent': f'{ua.random}'}) as response:
            book_info = await give_book_info(response=response, bot=bot, message=message)
            return book_info
