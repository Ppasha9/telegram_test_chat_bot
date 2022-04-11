import yaml


class ConfigYamlParser:
    def __init__(self, config_file_name):
        self._settings = dict()
        self.init(config_file_name)

    def init(self, config_file_name):
        with open(config_file_name, "r") as f:
            # для упрощения решил не вставлять проверку на правильность структуры файла настроек
            self._settings = yaml.load(f, Loader=yaml.SafeLoader)

    def get_bot_token(self):
        return self._settings["bot"]["settings"]["token"]

    def get_chat_products(self):
        return self._settings["bot"]["chat"]["products"]

    def get_chat_products_sizes(self):
        return self._settings["bot"]["chat"]["products_sizes"]

    def get_chat_payment_method(self):
        return self._settings["bot"]["chat"]["payment_method"]
