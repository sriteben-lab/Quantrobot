import re

from telegram import Update
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    filters,
)

from config import ADMIN_ID
from database import (
    get_ticket_messages,
)


async def open_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    text = update.message.text

    match = re.search(r"\((\d+)\)", text)

    if not match:
        return

    ticket_id = int(match.group(1))

    messages = get_ticket_messages(ticket_id)

    if not messages:
        await update.message.reply_text(
            "This conversation is empty."
        )
        return

    await update.message.reply_text(
        f"📩 Conversation #{ticket_id}\n"
    )

    for msg in messages:

        sender = msg[0]
        message = msg[2]
        media_type = msg[3]
        file_id = msg[4]
        caption = msg[5]

        if media_type == "photo":

            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=file_id,
                caption=f"{sender.upper()}:\n{caption or ''}",
            )

        else:

            await update.message.reply_text(
                f"{sender.upper()}:\n\n{message}"
            )


open_ticket_handler = MessageHandler(
    filters.Regex(r"^💬 .* \(\d+\)$"),
    open_ticket,
)
