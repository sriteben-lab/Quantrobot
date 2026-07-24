from telegram import Update
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

    text = "📩 *Support Inbox*\n\n"

    for ticket in tickets:

        ticket_id = ticket[0]
        user_id = ticket[1]
        updated = ticket[4]

        text += (
            f"🎫 Ticket #{ticket_id}\n"
            f"👤 User ID: `{user_id}`\n"
            f"🕒 {updated}\n\n"
        )

    text += (
        "Reply with a ticket number to open it."
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
    )


support_inbox_handler = MessageHandler(
    filters.Regex("^📩 Support Inbox$"),
    support_inbox,
)
