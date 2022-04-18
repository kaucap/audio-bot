import bs4


async def get_book_genre(book: bs4) -> str:
    genre = book.find("div", class_="articles__item--topline").find("a")
    finished_genre = genre.text.strip()
    return finished_genre


async def get_book_name(book: bs4) -> str:
    book_name = book.find("a", class_="content__article-main-link").find("h2")
    book_name_finished = book_name.text.strip()
    return book_name_finished


async def get_book_description(book: bs4) -> str:
    book_description = book.find("a", class_="content__article-main-link").find("span")
    book_description_finished = book_description.text.strip()
    return book_description_finished


async def get_author_and_performer_info(book: bs4) -> dict:
    author_finished = None
    performer_finished = None
    author_and_performer_exist = book.find_all("span", class_="link__action")
    if len(author_and_performer_exist) == 3:
        common_information = book.find("div", class_="additional-info").find("div", class_="oneline")
        author = common_information.find("span", class_="link__action").find("a")
        author_finished = author.text.strip()
        try:
            performer = common_information.find_all("span", class_="link__action")
            performer_finished = performer[1].find("a").text.strip()
        except AttributeError:
            performer_finished = 'Неизвестный'
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

    info = {'author': author_finished, 'performer': performer_finished}
    return info


async def get_book_duration(book: bs4) -> str:
    time = book.find("div", class_="additional-info").find("div", class_="oneline")
    time_continue = time.find("span", class_="link__action--label--time").find_all("span")
    time_finished = time_continue[0].text + ' ' + time_continue[1].text
    return time_finished


async def get_photo_url(book: bs4) -> str:
    photo_url = book.find("div", class_="container__remaining-width").find("a")
    photo_url_finished = photo_url.find("img").get("src")
    return photo_url_finished


async def get_book_url(book: bs4) -> str:
    book_url = book.find("div", class_="container__remaining-width").find("a")
    book_url_finished = book_url.get("href")
    return book_url_finished


async def book_information(book: bs4) -> dict:
    genre = await get_book_genre(book)
    book_name = await get_book_name(book)
    book_description = await get_book_description(book)
    author_and_performer = await get_author_and_performer_info(book)
    author = author_and_performer.get('author')
    performer = author_and_performer.get('performer')
    time = await get_book_duration(book)
    photo_url = await get_photo_url(book)
    book_url = await get_book_url(book)

    information = {'genre': genre, 'book_name': book_name,
                   'book_description': book_description, 'author': author,
                   'performer': performer, 'time': time, 'photo_url': photo_url,
                   'book_url': book_url}

    return information


async def get_genre(data: dict) -> str:
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


async def if_search_results_have_pages(soup: bs4.BeautifulSoup):
    paging = soup.find("div", class_="paging")
    if paging:
        paging_exist = paging.find("a", class_='page__nav--next')
        if paging_exist:
            return paging.find("a", class_='page__nav--next').get('href')
        else:
            return None
    else:
        return None
