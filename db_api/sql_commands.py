from asyncpg import UniqueViolationError

from db_api.schemas.user_request import Info
from db_api.schemas.user import User


async def add_user(id: int, name: str):
    try:
        user = User(id=id, name=name)

        await user.create()

    except UniqueViolationError:
        pass


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()

    return user


async def add_info(id: int, request: str):
    request = Info(id=id, request=request)
    await request.create()


async def choose_info(user_id: int):
    request = await Info.query.where(Info.id == user_id).gino.all()
    return request
