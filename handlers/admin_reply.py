from telegram import Update
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    filters,
)

from config import ADMIN_ID

from database import (
    get_ticket_user,
    save_ticket_message,
)


async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    ticket_id = context.user_data.get("active_ticket")

    if not ticket_id:
        return

    user_id = get_ticket_user(ticket_id)

    if not user_id:
        await update.message.reply_text("Ticket not found.")
        return

    text = update.message.text

    # Save to database
    save_ticket_message(
        ticket_id=ticket_id,
        sender="support",
        sender_id=ADMIN_ID,
        message=text,
    )

    # Send to the user
    await context.bot.send_message(
        chat_id=user_id,
        text=f"💬 Support\n\n{text}",
    )

    await update.message.reply_text("✅ Reply sent.")
    

admin_reply_handler = MessageHandler(
    filters.TEXT & ~filters.COMMAND,
    admin_reply,
)
