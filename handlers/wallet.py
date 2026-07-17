from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from keyboards import wallet_menu
from database import get_user


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
        reply_markup=wallet_menu,
        parse_mode="Markdown"
    )


wallet_handler = MessageHandler(
    filters.Regex("^💼 Wallet$"),
    wallet,
)
