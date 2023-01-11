from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from database.database import db, History


if __name__ == '__main__':
    with db:
        if not db.table_exists(table_name='History'):
            db.create_tables([History])
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
