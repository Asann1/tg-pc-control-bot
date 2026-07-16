"""
handlers.py — слой Telegram.

handler проверяет доступ и вызывает use case.

"""

from telegram import Update
from telegram.ext import ContextTypes

from tg_pc_control_bot.bot.keyboards import back_to_menu_keyboard, main_menu_keyboard
from tg_pc_control_bot.domain.commands import CommandScope
from tg_pc_control_bot.domain.use_cases.get_status import GetStatusUseCase
from tg_pc_control_bot.security.policies import AuthPolicy


class BotHandlers:
    def __init__(
        self,
        auth_policy: AuthPolicy,
        get_status_use_case: GetStatusUseCase,
    ) -> None:
        self._auth = auth_policy
        self._get_status = get_status_use_case

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
        chat_id = update.effective_chat.id
        if not self._auth.is_allowed(chat_id, CommandScope.READ):
            await update.message.reply_text("⛔ Доступ запрещён")
            return

        await update.message.reply_text(
            "Привет! Я бот для мониторинга твоего ПК.",
            reply_markup=main_menu_keyboard(),
        )

    async def status_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
        query = update.callback_query
        await query.answer()  # убирает «часики» на кнопке в Telegram

        chat_id = update.effective_chat.id
        if not self._auth.is_allowed(chat_id, CommandScope.READ):
            await query.edit_message_text("⛔ Доступ запрещён")
            return

        text = self._get_status.execute()
        await query.edit_message_text(text=text, reply_markup=back_to_menu_keyboard())

    async def back_to_menu_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
        query = update.callback_query
        await query.answer()

        chat_id = update.effective_chat.id
        if not self._auth.is_allowed(chat_id, CommandScope.READ):
            await query.edit_message_text("⛔ Доступ запрещён")
            return

        await query.edit_message_text(
            text="Главное меню:",
            reply_markup=main_menu_keyboard(),
        )