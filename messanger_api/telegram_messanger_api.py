from telebot import TeleBot, types

from config.config import ConfigYamlParser
from state.bot_state import BotState

# для простоты захардкодим путь до конфиг файла
_CONFIG_FILE_NAME = "./config/bot.yaml"
_config = ConfigYamlParser(config_file_name=_CONFIG_FILE_NAME)
_bot_state = BotState()
_bot = TeleBot(_config.get_bot_token())


def _show_start_message(chat_id):
    _bot.send_message(chat_id=chat_id,
                      text="Привет!\nЯ тестовый чат-бот для заказа еды.")


def _show_products_list_message(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for pr_name in _config.get_chat_products():
        markup.add(types.KeyboardButton(pr_name))
    _bot.send_message(chat_id=chat_id,
                      text="У вас есть возможность заказать несколько блюд.",
                      reply_markup=markup)


def _product_selected_reply(message):
    _bot_state.trigger("product_selected", message.text)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for pr_size in _config.get_chat_products_sizes():
        markup.add(types.KeyboardButton(pr_size))
    _bot.send_message(chat_id=message.chat.id,
                      text=f"Вы выбрали продукт '{_bot_state.get_product_name().lower()}'.\nКакой размер вы хотите?",
                      reply_markup=markup)


def _product_size_selected_reply(message):
    _bot_state.trigger("size_selected", message.text)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for payment_method in _config.get_chat_payment_method():
        markup.add(types.KeyboardButton(payment_method))
    _bot.send_message(chat_id=message.chat.id,
                      text=f"Вы выбрали продукт '{_bot_state.get_product_name().lower()}'"
                           f" размера '{_bot_state.get_product_size().lower()}'.\nКакой метод оплаты?",
                      reply_markup=markup)


def _payment_selected_reply(message):
    _bot_state.trigger("payment_selected", message.text)

    _bot.send_message(chat_id=message.chat.id,
                      text=f"Вы выбрали продукт '{_bot_state.get_product_name().lower()}'"
                           f" размера '{_bot_state.get_product_size().lower()}."
                           f" Оплата {_bot_state.get_payment_method().lower()}.\nСпасибо за заказ")

    _show_products_list_message(message.chat.id)


@_bot.message_handler(commands=['start'])
def _start_message(message):
    chat_id = message.chat.id
    _show_start_message(chat_id)
    _show_products_list_message(chat_id)


@_bot.message_handler(content_types="text")
def _message_reply(message):
    if _bot_state.is_waiting_for_product_name():
        _product_selected_reply(message)
    elif _bot_state.is_waiting_for_product_size():
        _product_size_selected_reply(message)
    elif _bot_state.is_waiting_for_payment_method():
        _payment_selected_reply(message)


def telegram_bot_start():
    _bot.infinity_polling()
