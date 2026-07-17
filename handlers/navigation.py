from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from keyboards import main_menu
from handlers.wallet import wallet


async def navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🏠 Main Menu":
        await update.message.reply_text(
            "🏠 Main Menu",
            reply_markup=main_menu
        )

    elif text == "⬅ Back" or text == "⬅ Back to Wallet":
        await wallet(update, context)


navigation_handler = MessageHandler(
    filters.Regex("^(🏠 Main Menu|⬅ Back|⬅ Back to Wallet)$"),
    navigation,
)
