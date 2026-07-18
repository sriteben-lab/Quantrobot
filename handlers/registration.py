from telegram import Update
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

from database import (
    add_user,
    user_exists,
    set_referrer,
    get_referrer,
)
from keyboards import main_menu

NAME, EMAIL, PHONE, COUNTRY = range(4)


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if user_exists(update.effective_user.id):
        await update.message.reply_text(
            "✅ You are already registered.",
            reply_markup=main_menu
        )
        return ConversationHandler.END

    await update.message.reply_text("Enter your Full Name:")
    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Enter your Email:")
    return EMAIL


async def email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["email"] = update.message.text
    await update.message.reply_text("Enter your Phone Number:")
    return PHONE


async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("Enter your Country:")
    return COUNTRY


async def country(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    add_user(
        user_id,
        context.user_data["name"],
        context.user_data["email"],
        context.user_data["phone"],
        update.message.text,
    )

    # Save referral if user joined through a referral link
    referrer_id = context.user_data.get("referrer_id")

    if (
        referrer_id
        and referrer_id != user_id
        and get_referrer(user_id) is None
    ):
        set_referrer(user_id, referrer_id)

    await update.message.reply_text(
        "🎉 Registration completed successfully!",
        reply_markup=main_menu,
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Registration cancelled.",
        reply_markup=main_menu
    )
    return ConversationHandler.END


registration_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex("^🆕 New User Registration$"),
            register,
        )
    ],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone)],
        COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, country)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel)
    ],
)
