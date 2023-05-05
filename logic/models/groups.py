import telebot


class Groups:
    def __init__(self):
        self.psychology = 'Психология'
        self.crypto = 'Криптовалюты'
        self.startup = 'Стартапы'

    def groups_list(self):
        all_groups = [f"{self.psychology}, {self.crypto}, {self.startup}"]
        return "\n".join(all_groups)
