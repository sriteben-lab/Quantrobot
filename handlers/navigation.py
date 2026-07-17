from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from keyboards import main_menu
from handlers.wallet import wallet


async def navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "🏠 Main Menu":

        await update.message.reply_text(
            "🏠 Main Menu",
            reply_markup=main_menu
        )

    elif update.message.text == "⬅ Back to Wallet":

        await wallet(update, context)


navigation_handler = MessageHandler(
    filters.Regex("^(🏠 Main Menu|⬅ Back to Wallet)$"),
    navigation,
)
