from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters


async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        return

    replied = update.message.reply_to_message.message_id

    if replied not in context.bot_data:
        return

    user_id = context.bot_data[replied]

    await context.bot.send_message(
        chat_id=user_id,
        text=f"💬 *Support Reply*\n\n{update.message.text}",
        parse_mode="Markdown",
    )

    await update.message.reply_text("✅ Reply sent.")


reply_handler = MessageHandler(
    filters.REPLY,
    reply_to_user,
)
