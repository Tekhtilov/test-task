import telebot
from bot_creds import bot
from logic.models.keyboards import UserInlineKeyboard
from logic.models.groups import Groups


class UserFlow:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot
        self.keyboard = UserInlineKeyboard()
        self.groups = Groups()

    # Обработчик команды /start
    def get_started(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            bot.send_message(message.chat.id, "Привет! Я бот, который поможет тебе выбрать группу "
                                              "по твоим интересам.",
                             reply_markup=self.keyboard.get_keyboard(key_type='main'))

    # Обработчик нажатий на кнопки
    def get_interests(self):
        @self.bot.callback_query_handler(func=lambda call: call.data in ['cb_show_group', 'cb_match_group'])
        def handle_match_group(call):
            groups = self.groups.groups_list()
            if call.data == 'cb_match_group':
                self.bot.send_message(call.message.chat.id, "Чем вы интересуетесь?",
                                      reply_markup=self.keyboard.get_keyboard(key_type='interests'))
            elif call.data == 'cb_show_group':
                self.bot.send_message(call.message.chat.id, f"Вот список всех доступных групп: {groups}")

        # Обработчик нажатий на кнопки с интересами
        @self.bot.callback_query_handler(
            func=lambda call: call.data in ['cb_psychology', 'cb_cryptocurrency', 'cb_startups'])
        def handle_interests(call):

            # Для варианта "Психология"
            if call.data == 'cb_psychology':
                self.bot.send_message(call.message.chat.id, "Вы психолог?",
                                      reply_markup=self.keyboard.get_keyboard(key_type='psy_yes/no'))

                # Обработчик ответа на вопрос "Вы психолог?"
                @self.bot.callback_query_handler(func=lambda call: call.data in ['cb_psy_yes', 'cb_psy_no'])
                def handle_answer(call):
                    if call.data == 'cb_psy_yes' or call.data == 'cb_psy_no':
                        self.bot.send_message(call.message.chat.id,
                                              '<a href="https://t.me/psychologists_chat">Вот наш чат для психологов</a>',
                                              parse_mode="HTML",
                                              reply_markup=self.keyboard.get_keyboard(key_type='back to menu'))

            # Для варианта "Криптовалюта"
            elif call.data == 'cb_cryptocurrency':
                self.bot.send_message(call.message.chat.id, "Вы торгуете криптовалютой?",
                                      reply_markup=self.keyboard.get_keyboard(key_type='crypto_yes/no'))

                # Обработчик ответа на вопрос "Вы торгуете криптовалютой?"
                @self.bot.callback_query_handler(func=lambda call: call.data in ['cb_crypto_yes', 'cb_crypto_no'])
                def handle_answer(call):
                    if call.data == 'cb_crypto_yes' or call.data == 'cb_crypto_no':
                        self.bot.send_message(call.message.chat.id,
                                              '<a href="https://t.me/crypto_chat">Вот наш чат для криптовалюты </a>',
                                              parse_mode="HTML",
                                              reply_markup=self.keyboard.get_keyboard(key_type='back to menu'))

            # Для варианта "Стартап"
            elif call.data == 'cb_startups':
                self.bot.send_message(call.message.chat.id, "Вы создаете стартап?",
                                      reply_markup=self.keyboard.get_keyboard(key_type='startup_yes/no'))

                # Обработчик ответа на вопрос "Вы создаете стартап?"
                @self.bot.callback_query_handler(func=lambda call: call.data in ['cb_startup_yes', 'cb_startup_no'])
                def handle_answer(call):
                    if call.data == 'cb_startup_yes' or call.data == 'cb_startup_no':
                        self.bot.send_message(call.message.chat.id,
                                              '<a href="https://t.me/startup_chat">Вот наш чат для стартапов</a>',
                                              parse_mode="HTML",
                                              reply_markup=self.keyboard.get_keyboard(key_type='back to menu'))

            # Кнопка возврата в главное меню
            @self.bot.callback_query_handler(func=lambda call: call.data == 'cb_back_to_menu')
            def get_back_to_menu(call):
                if call.data == 'cb_back_to_menu':
                    self.bot.send_message(call.message.chat.id, "Привет! Я бот, который поможет тебе выбрать группу "
                                              "по твоим интересам.",
                             reply_markup=self.keyboard.get_keyboard(key_type='main'))

