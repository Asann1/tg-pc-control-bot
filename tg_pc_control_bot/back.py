
# ВСЕ ИМПОРТЫ
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler, filters, CallbackQueryHandler
import psutil


# ИНИЦИАЛИЗАЦИЯ И НАСТРОЙКИ
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
owner_chat_id = int(os.getenv("OWNER_CHAT_ID"))

application = Application.builder().token(BOT_TOKEN).build()


# ФУНКЦИИ
async def status_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != owner_chat_id:
        await update.message.reply_text("Отказано в доступе")
        return
    status_button = InlineKeyboardButton(text='📊 Проверить статус', callback_data="trigger_status_check")
    keyboard_layout = [[status_button]]
    keyboard_markup = InlineKeyboardMarkup(keyboard_layout)
    await update.message.reply_text('Привет! Я бот-сервер.', reply_markup=keyboard_markup)

async def handle_status_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback_query = update.callback_query
    await callback_query.answer()
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent 
    response_text = f"Статус сервера:\n💻 Процессор: {cpu_usage}%\n📊 Память: {ram_usage}%"
    await callback_query.edit_message_text(text=response_text)


# РЕГИСТРАЦИЯ И ЗАПУСК
application.add_handler(CommandHandler("start", status_check))

application.add_handler(CallbackQueryHandler(handle_status_request, pattern="trigger_status_check"))


if __name__ == "__main__":
    application.run_polling()




