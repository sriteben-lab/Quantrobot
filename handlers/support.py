from telegram import Update
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

from config import ADMIN_CHAT_ID
from keyboards import main_menu

SUPPORT = 0


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💬 *Customer Support*\n\n"
        "Please type your message below.\n\n"
        "Our support team will respond as soon as possible.",
        parse_mode="Markdown",
    )

    return SUPPORT


async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    text = (
        "📩 *New Support Message*\n\n"
        f"👤 Name: {user.full_name}\n"
        f"🆔 User ID: `{user.id}`\n"
        f"📛 Username: @{user.username or 'None'}\n\n"
        f"💬 Message:\n{update.message.text}"
    )

    # Send message to admin
    sent = await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=text,
        parse_mode="Markdown",
    )

    # Save user id so admin replies go back to this user
    context.bot_data[sent.message_id] = user.id

    await update.message.reply_text(
        "✅ Your message has been sent successfully.\n\n"
        "Our support team will reply shortly.",
        reply_markup=main_menu,
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Support request cancelled.",
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
        CommandHandler("cancel", cancel),
    ],
)
