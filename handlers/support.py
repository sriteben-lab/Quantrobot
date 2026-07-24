from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    CommandHandler,
    filters,
)

from config import ADMIN_ID
from keyboards import main_menu

from database import (
    save_support_message,
    get_open_ticket,
    create_support_ticket,
    save_ticket_message,
)

MESSAGE = 0

cancel_menu = ReplyKeyboardMarkup(
    [
        ["🏠 Main Menu"]
    ],
    resize_keyboard=True,
)


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💬 *Chat with Support*\n\n"
        "Send your message or photo.\n\n"
        "Our support team will reply as soon as possible.",
        parse_mode="Markdown",
        reply_markup=cancel_menu,
    )

    return MESSAGE


async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if update.effective_user.id == ADMIN_ID:
    return

    # ---------- TEXT ----------
    if update.message.text:

        sent = await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                "📩 *New Support Message*\n\n"
                f"👤 {user.full_name}\n"
                f"🆔 `{user.id}`\n\n"
                f"{update.message.text}"
            ),
            parse_mode="Markdown",
        )
        save_support_message(
            sent.message_id,
            user.id,
        )

        ticket_id = get_open_ticket(user.id)

        if not ticket_id:
            ticket_id = create_support_ticket(user.id)

        save_ticket_message(
            ticket_id=ticket_id,
            sender="user",
            sender_id=user.id,
            message=update.message.text,
        )
        

    # ---------- PHOTO ----------
    elif update.message.photo:

        caption = update.message.caption or "No caption"

        photo = update.message.photo[-1].file_id

        sent = await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo,
            caption=(
                "📩 New Support Photo\n\n"
                f"👤 {user.full_name}\n"
                f"🆔 {user.id}\n\n"
                f"{caption}"
            ),
        )
        save_support_message(
            sent.message_id,
            user.id,
        )
        ticket_id = get_open_ticket(user.id)

        if not ticket_id:
            ticket_id = create_support_ticket(user.id)

        save_ticket_message(
            ticket_id=ticket_id,
            sender="user",
            sender_id=user.id,
            media_type="photo",
            file_id=photo,
            caption=caption,
         )

    else:

        await update.message.reply_text(
            "❌ Only text messages and photos are supported."
        )

        return MESSAGE

    # Save admin message_id -> user_id
    context.bot_data[sent.message_id] = user.id

    await update.message.reply_text(
        "✅ Your message has been sent to support.\n\n"
        "We'll get back to you shortly.",
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
        MESSAGE: [
            MessageHandler(
                (filters.TEXT | filters.PHOTO)
                & ~filters.COMMAND,
                receive_message,
            )
        ]
    },
    fallbacks=[
        CommandHandler("cancel", cancel)
    ],
)
