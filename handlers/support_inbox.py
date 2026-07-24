from telegram import (
    Update,
    ReplyKeyboardMarkup,
)

from telegram.ext import (
    ContextTypes,
    MessageHandler,
    filters,
)

from config import ADMIN_ID
from database import get_open_support_tickets


async def support_inbox(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    tickets = get_open_support_tickets()

    if not tickets:
        await update.message.reply_text(
            "📩 Support Inbox\n\n"
            "There are no open support tickets."
        )
        return

        keyboard = []

    for ticket in tickets:

        ticket_id = ticket[0]
        user_id = ticket[1]
        full_name = ticket[2]

        keyboard.append(
            [f"💬 {full_name} ({ticket_id})"]
        )

    keyboard.append(["🛠 Admin Panel"])

    await update.message.reply_text(
        "📩 *Support Inbox*\n\n"
        "Select a conversation.",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
        ),
    )

support_inbox_handler = MessageHandler(
    filters.Regex("^📩 Support Inbox$"),
    support_inbox,
        )
