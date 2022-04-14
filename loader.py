from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import config

BOT_KEY = config('KEY')
bot = Bot(token=BOT_KEY, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
PGUSER = config('PGUSER')
PGPASSWORD = config('PGPASSWORD')
DATABASE = config('DATABASE')
ip = '127.0.0.1'
POSTGRES_URI = f'postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'


# loop = asyncio.get_event_loop()
# db = loop.run_until_complete(Database.create())
