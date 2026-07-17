from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN
from database import create_tables
from keyboards import main_menu
from handlers.registration import registration_handler
from handlers.profile import profile_handler
from handlers.wallet import wallet_handler
from handlers.fund_wallet import fund_wallet_handler
from handlers.deposit import deposit_handler
from handlers.submit_tx import submit_tx_handler
from handlers.navigation import navigation_handler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 Welcome to Quantro Network!\n\n"
        "Please choose an option from the menu below.",
        reply_markup=main_menu
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Quantro Network Bot\n\n"
        "Use the menu buttons to access the available features."
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📈 Investment Plans":
        await update.message.reply_text(
            "📈 Investment module is under development."
        )

    elif text == "👥 Referrals":
        await update.message.reply_text(
            "👥 Referral module is under development."
        )

    elif text == "🪪 KYC":
        await update.message.reply_text(
            "🪪 KYC module is under development."
        )

    elif text == "💰 Refund":
        await update.message.reply_text(
            "💰 Refund module is under development."
        )

    elif text == "💬 Support":
        await update.message.reply_text(
            "💬 Support module is under development."
        )

    else:
        await update.message.reply_text(
            "Please choose an option from the menu."
        )


def main():
    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(registration_handler)
    app.add_handler(profile_handler)
    app.add_handler(wallet_handler)
    app.add_handler(fund_wallet_handler)
    app.add_handler(deposit_handler)
    app.add_handler(submit_tx_handler)
    app.add_handler(navigation_handler)

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, buttons)
    )

    print("✅ Quantro Network Bot Started")

    app.run_polling()


if __name__ == "__main__":
    main()
