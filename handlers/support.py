from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

from keyboards import main_menu
from config import ADMIN_CHAT_ID

SUPPORT = 0

cancel_keyboard = ReplyKeyboardMarkup(
    [
        ["🏠 Main Menu"]
    ],
    resize_keyboard=True,
)


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "💬 Support\n\n"
        "Please describe your issue.\n\n"
        "Our support team will respond as soon as possible.",
        reply_markup=cancel_keyboard,
    )

    return SUPPORT


async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    text = f"""
📩 New Support Message

👤 {user.full_name}
🆔 {user.id}
📛 @{user.username}

━━━━━━━━━━━━━━

{update.message.text}
"""

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=text,
    )

    await update.message.reply_text(
        "✅ Your message has been sent successfully.\n\n"
        "Our support team will contact you shortly.",
        reply_markup=main_menu,
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Support chat cancelled.",
        reply_markup=main_menu,
    )

    return ConversationHandler.END


support_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex("^💬 Chat with Support$"),
            support,
        )
    ],
    states={
        SUPPORT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                receive_message,
            )
        ]
    },
    fallbacks=[
        CommandHandler("cancel", cancel)
    ],
)
