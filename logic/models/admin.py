import telebot
import pandas as pd
from bot_creds import bot
from logic.models.keyboards import AdminInlineKeyboard
from database import cur


class Admin:
    def __init__(self, bot: telebot.TeleBot):
        self.admin_ids = [1988940601]  # список чат айди администраторов
        self.bot = bot
        self.keyboard = AdminInlineKeyboard()
        self.cur = cur

    # проверка, является ли отправитель сообщения администратором
    def admin_check(self):
        @self.bot.message_handler(commands=['admin'])
        def handle_admin(message):
            if message.chat.id in self.admin_ids:  # если является, то выводим опции
                bot.send_message(message.chat.id, "Выберите опцию:",
                                 reply_markup=self.keyboard.get_keyboard(key_type='main'))
            else:  # если не является, выводим сообщение об ошибке
                bot.send_message(message.chat.id, "Вы не админ.")

    def select_all(self):
        @self.bot.callback_query_handler(
            func=lambda call: call.data in ['cb_upload_users'])  # получение всех пользователей из базы данных
        def handle_select_all(call):
            self.cur.execute("SELECT * FROM bots_users")
            rows = cur.fetchall()
            pd.DataFrame(rows).to_excel('output.xlsx', header=False, index=False)  # экспорт данных в файл Excel
            result_list = []
            for i, row in enumerate(rows):
                row_str = f"{i + 1}. User's name and last name: {row['user_name']} {row['user_last_name']}, Telegram name: @{row['username']}"
                result_list.append(row_str)
            print()
            result = "\n".join(result_list)

            with open('output.xlsx', 'rb') as f:  # отправка файла пользователям
                bot.send_message(call.message.chat.id, result,
                                 reply_markup=self.keyboard.get_keyboard(key_type='back_to_panel'))
                bot.send_document(call.message.chat.id, f)

        # кнопка возврата на главную страницу
        @self.bot.callback_query_handler(func=lambda call: call.data == 'cb_back_to_admin_panel')
        def handle_back_to_panel(call):
            if call.data == 'cb_back_to_admin_panel':
                self.bot.send_message(call.message.chat.id, "Выберите опцию:",
                                      reply_markup=self.keyboard.get_keyboard(key_type='main'))

    # отправка сообщения всем пользователям
    def send_everyone_message(self):
        @self.bot.callback_query_handler(func=lambda call: call.data == 'cb_send_message')
        def handle_message(call):
            if call.data == 'cb_send_message':
                msg = self.bot.send_message(call.message.chat.id, "Введите сообщение:")
                self.bot.register_next_step_handler(msg, process_input)

        def process_input(message):
            self.cur.execute("SELECT id FROM bots_users")
            users = cur.fetchall()
            for user in users:
                try:
                    if user['id'] in self.admin_ids:  # если пользователь является администратором, отправляем
                        # сообщение с клавиатурой "Вернуться на главную страницу"
                        self.bot.send_message(user['id'], message.text,
                                              reply_markup=self.keyboard.get_keyboard(key_type='back_to_panel'))
                    else:  # если пользователь не является администратором, отправляем сообщение
                        self.bot.send_message(user['id'], message.text)
                except Exception as e:  # выводим сообщение
                    print(f"Message wasn't sent to: {user['id']} because of {e}")

        # Кнопка возврата на админскую панель
        @self.bot.callback_query_handler(func=lambda call: call.data == 'cb_back_to_admin_panel')
        def handle_back_to_panel(call):
            if call.data == 'cb_back_to_admin_panel':
                self.bot.send_message(call.message.chat.id, "Выберите опцию:",
                                      reply_markup=self.keyboard.get_keyboard(key_type='main'))
