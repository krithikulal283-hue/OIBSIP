from datetime import datetime


class PasswordHistory:

    def __init__(self):
        self.history = []

    def add_password(self, password, strength):
        record = {
            "password": password,
            "strength": strength,
            "date_time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        self.history.append(record)

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history.clear()