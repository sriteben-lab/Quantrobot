from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

from database import get_user

wallet_keyboard = ReplyKeyboardMarkup(
    [
        ["💳 Fund Wallet"],
        ["📜 Transaction History"],
        ["🔙 Back"],
    ],
    resize_keyboard=True,
)

async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    if not user:
        await update.message.reply_text(
            "❌ Please register first."
        )
        return

    message = f"""
💼 *QUANTRO WALLET*

━━━━━━━━━━━━━━

💰 Wallet Balance: ${user[7]:.2f}

💵 Affiliate Balance: ${user[8]:.2f}

━━━━━━━━━━━━━━

Choose an option below.
"""

    await update.message.reply_text(
        message,
        reply_markup=wallet_keyboard,
        parse_mode="Markdown"
    )

wallet_handler = MessageHandler(
    filters.Regex("^💼 Wallet$"),
    wallet,
)
