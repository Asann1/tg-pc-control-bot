"""
keyboards.py — кнопки (UI Telegram).

"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard() -> InlineKeyboardMarkup:
    
    status_button = InlineKeyboardButton(
        text="📊 Проверить статус",
        callback_data="status:check",  
    )
    return InlineKeyboardMarkup([[status_button]])


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    
    back_button = InlineKeyboardButton(
        text="⬅️ Назад",
        callback_data="menu:back",
    )
    return InlineKeyboardMarkup([[back_button]])