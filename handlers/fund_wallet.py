from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from keyboards import fund_keyboard


async def fund_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💳 *Fund Wallet*\n\n"
        "Select the cryptocurrency you want to deposit:",
        reply_markup=fund_keyboard,
        parse_mode="Markdown"
    )


fund_wallet_handler = MessageHandler(
    filters.Regex("^💳 Fund Wallet$"),
    fund_wallet,
)
