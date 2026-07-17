from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from keyboards import main_menu


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏠 Main Menu",
        reply_markup=main_menu
    )


back_handler = MessageHandler(
    filters.Regex("^⬅ Back$|^🔙 Back$"),
    back
              )
