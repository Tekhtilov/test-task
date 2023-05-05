import telebot
import logging
from logic.models.user import UserFlow
from logic.models.admin import Admin
from bot_creds import bot

telebot.logger.setLevel(logging.DEBUG)

user_flow = UserFlow(bot)
admin_validation = Admin(bot)


user_flow.get_started()
user_flow.get_interests()

admin_validation.admin_check()
admin_validation.select_all()
admin_validation.send_everyone_message()


bot.polling(non_stop=True)
