import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, filters

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
owner_chat_id = int(os.getenv("OWNER_CHAT_ID"))

application = Application.builder().token(BOT_TOKEN).build()



async def status_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != owner_chat_id:
        await update.message.reply_text("Отказано в доступе")
        return
    await update.message.reply_text('Привет! Я бот для проверки статуса сервера.')



application.add_handler(CommandHandler("start", status_check))

application.run_polling()



# ПЕРЕД ДЕПЛОЕМ ПОЧИСТИТЬ ТОКЕН И АЙДИ ВСЕ ОФОРМИТЬ