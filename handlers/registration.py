from telegram import Update
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

from config import ADMIN_ID

from database import (
    add_user,
    user_exists,
    set_referrer,
    get_referrer,
)

from keyboards import main_menu


NAME, EMAIL, PHONE, COUNTRY = range(4)


# =====================================
# START REGISTRATION
# =====================================

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if user_exists(update.effective_user.id):
        await update.message.reply_text(
            "✅ You are already registered.",
            reply_markup=main_menu,
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "Enter your Full Name:"
    )

    return NAME


# =====================================
# NAME
# =====================================

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "Enter your Email:"
    )

    return EMAIL


# =====================================
# EMAIL
# =====================================

async def email(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["email"] = update.message.text

    await update.message.reply_text(
        "Enter your Phone Number:"
    )

    return PHONE


# =====================================
# PHONE
# =====================================

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["phone"] = update.message.text

    await update.message.reply_text(
        "Enter your Country:"
    )

    return COUNTRY


# =====================================
# COUNTRY / FINISH REGISTRATION
# =====================================

async def country(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    full_name = context.user_data["name"]
    email = context.user_data["email"]
    phone = context.user_data["phone"]
    country = update.message.text

    # Save user
    add_user(
        user_id,
        full_name,
        email,
        phone,
        country,
    )

    # Save referral
    referrer_id = context.user_data.get("referrer_id")

    if (
        referrer_id
        and referrer_id != user_id
        and get_referrer(user_id) is None
    ):
        set_referrer(user_id, referrer_id)

    # Notify admin
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                "🆕 *NEW USER REGISTRATION*\n\n"
                f"👤 *Full Name:* {full_name}\n"
                f"🆔 *Telegram ID:* `{user_id}`\n"
                f"📧 *Email:* {email}\n"
                f"📱 *Phone:* {phone}\n"
                f"🌍 *Country:* {country}"
            ),
            parse_mode="Markdown",
        )
    except Exception as e:
        print(f"Failed to notify admin: {e}")

    # Notify user
    await update.message.reply_text(
        "🎉 Registration completed successfully!",
        reply_markup=main_menu,
    )

    context.user_data.clear()

    return ConversationHandler.END


# =====================================
# CANCEL
# =====================================

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "❌ Registration cancelled.",
        reply_markup=main_menu,
    )

    return ConversationHandler.END


# =====================================
# CONVERSATION HANDLER
# =====================================

registration_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex("^🆕 New User Registration$"),
            register,
        )
    ],
    states={
        NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                name,
            )
        ],
        EMAIL: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                email,
            )
        ],
        PHONE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                phone,
            )
        ],
        COUNTRY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                country,
            )
        ],
    },
    fallbacks=[
        CommandHandler(
            "cancel",
            cancel,
        )
    ],
)
