import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from utils.book_information import book_information, get_genre


async def send_message_to_user_about_book(book, bot, message):
    info = await book_information(book)
    await bot.send_photo(chat_id=message.from_user.id, photo=info.get("photo_url"),
                         caption=f'🖊  Автор: {info.get("author")}\n📖  Название книги: {info.get("book_name")}\n'
                                 f'📌  Жанр: {info.get("genre")}\n🔈  Исполнитель: {info.get("performer")}\n'
                                 f'🕰  Длительность книги: {info.get("time")}\n'
                                 f'\n🗒  Описание: {info.get("book_description")}\n'
                                 f'\n📥  Ссылка: {info.get("book_url")}')


async def give_book_info(response, bot, message):
    html = await response.text()
    soup = BeautifulSoup(html, "lxml")
    books = soup.find_all("div", class_="content__main__articles--item")

    if books:
        for book in books:
            await send_message_to_user_about_book(book, bot, message)
    else:
        await message.answer('К сожалению поиск не дал результатов. Попробуйте ввести другие данные')

    return soup


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
                await send_message_to_user_about_book(book, bot, message)


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
