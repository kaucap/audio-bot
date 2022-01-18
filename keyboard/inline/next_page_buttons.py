from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

choice = InlineKeyboardMarkup(
                              inline_keyboard=[
                                  [
                                      InlineKeyboardButton(
                                          text="Следующая страница",
                                          callback_data="next_page"
                                      )
                                  ],
                                  [
                                      InlineKeyboardButton(
                                          text="Отмена",
                                          callback_data="cancel"
                                      )
                                  ]
                              ])
