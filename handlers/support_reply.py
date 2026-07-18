import re

from telegram import Update
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    filters,
)


async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        return

    original_text = update.message.reply_to_message.text or ""

    # Look for: User ID: `123456789`
    match = re.search(r"User ID:\s*`?(\d+)`?", original_text)

    if not match:
        await update.message.reply_text(
            "❌ Could not determine the user's ID.\n"
            "Please reply directly to a support message sent by the bot."
        )
        return

    user_id = int(match.group(1))

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "💬 *Support Reply*\n\n"
                f"{update.message.text}"
            ),
            parse_mode="Markdown",
        )

        await update.message.reply_text("✅ Reply sent successfully.")

    except Exception as e:
        await update.message.reply_text(
            f"❌ Failed to send reply.\n\n{e}"
        )


reply_handler = MessageHandler(
    filters.REPLY & filters.TEXT,
    reply_to_user,
)
