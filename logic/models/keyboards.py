from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class UserInlineKeyboard:
    def __init__(self):
        self.markup = InlineKeyboardMarkup()

    # Метод для получения инлайн-клавиатуры, в зависимости от типа
    def get_keyboard(self, key_type='main'):

        # Очищаем клавиатуру перед её заполнением
        self.markup.keyboard = []

        # Добавление кнопок для подбора и просмотра групп
        if key_type == 'main':
            match_group_button = InlineKeyboardButton("Подобрать группу", callback_data="cb_match_group")
            show_group_button = InlineKeyboardButton("Список групп", callback_data="cb_show_group")
            self.markup.add(match_group_button,show_group_button, row_width=2)

        # Добавление кнопок для выбора интересов
        elif key_type == 'interests':
            self.markup.row_width = 3
            self.markup.add(InlineKeyboardButton("Психология", callback_data="cb_psychology"))
            self.markup.add(InlineKeyboardButton("Криптовалюты", callback_data="cb_cryptocurrency"))
            self.markup.add(InlineKeyboardButton("Стартапы", callback_data="cb_startups"))

        # Добавление кнопок для ответа "Да" или "Нет" на вопрос о психологии
        elif key_type == 'psy_yes/no':
            psy_yes_button = InlineKeyboardButton("Да", callback_data="cb_psy_yes")
            psy_no_button = InlineKeyboardButton("Нет", callback_data="cb_psy_no")
            self.markup.add(psy_yes_button,psy_no_button)

        # Добавление кнопок для ответа "Да" или "Нет" на вопрос о криптовалюте
        elif key_type == 'crypto_yes/no':
            crypto_yes_button = InlineKeyboardButton("Да", callback_data="cb_crypto_yes")
            crypto_no_button = InlineKeyboardButton("Нет", callback_data="cb_crypto_no")
            self.markup.add(crypto_yes_button,crypto_no_button)

        # Добавление кнопок для ответа "Да" или "Нет" на вопрос о стартапах
        elif key_type == 'startup_yes/no':
            startup_yes_button = InlineKeyboardButton("Да", callback_data="cb_startup_yes")
            startup_no_button = InlineKeyboardButton("Нет", callback_data="cb_startup_no")
            self.markup.add(startup_yes_button,startup_no_button)

        # Добавление кнопки для возврата к главному меню
        elif key_type == 'back to menu':
            self.markup.row_width = 1
            self.markup.add(InlineKeyboardButton("Вернуться в меню", callback_data="cb_back_to_menu"))

        return self.markup


class AdminInlineKeyboard:
    def __init__(self):
        self.markup = InlineKeyboardMarkup()

    # Очищаем клавиатуру перед её заполнением
    def get_keyboard(self, key_type):
        self.markup.keyboard = []

        # Добавляем кнопки для выгрузки пользователей и отправки сообщения
        if key_type == 'main':
            self.markup.add(InlineKeyboardButton("Выгрузить пользователей", callback_data="cb_upload_users"))
            self.markup.add(InlineKeyboardButton("Отправить сообщение пользователям", callback_data="cb_send_message"))

        # Добавляем кнопку для возврата в админскую панель
        elif key_type == 'back_to_panel':
            self.markup.add(InlineKeyboardButton("Возврат в админ панель", callback_data="cb_back_to_admin_panel"))
        return self.markup
