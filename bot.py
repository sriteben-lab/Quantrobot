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
from handlers.history import history_handler
from handlers.support import support_handler
from handlers.support_reply import reply_handler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 Welcome to Quantro Network!\n\n"
        "Please choose an option from the menu below.",
        reply_markup=main_menu,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Quantro Network Bot\n\n"
        "Use the menu buttons to access the available features."
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🏠 Main Menu":
        await update.message.reply_text(
            "🏠 Main Menu",
            reply_markup=main_menu,
        )
        return

    if text == "📈 Investment Plans":
        await update.message.reply_text(
            "📈 Investment module is under development."
        )

    elif text == "👥 Referrals":
        await update.message.reply_text(
            "👥 Referral module is under development."
        )

    elif text == "🪪 KYC Status":
        await update.message.reply_text(
            "🪪 KYC Status module is under development."
        )

    elif text == "📤 Submit KYC":
        await update.message.reply_text(
            "📤 KYC submission module is under development."
        )

    elif text == "💰 Submit Refund Request":
        await update.message.reply_text(
            "💰 Refund request module is under development."
        )

    elif text == "📊 Check Status":
        await update.message.reply_text(
            "📊 Status checker is under development."
        )

    elif text == "💬 Chat with Support":
        await update.message.reply_text(
            "💬 Support module is under development."
        )

    elif text == "ℹ️ Help":
        await help_command(update, context)


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
    app.add_handler(history_handler)
    app.add_handler(support_handler)
    app.add_handler(reply_handler)
    

     
    menu_filter = filters.Regex(
        r"^(📈 Investment Plans|👥 Referrals|🪪 KYC Status|📤 Submit KYC|💰 Submit Refund Request|📊 Check Status|💬 Chat with Support|ℹ️ Help|🏠 Main Menu)$"
    )

    app.add_handler(
        MessageHandler(
            menu_filter,
            buttons,
        )
    )

    print("✅ Quantro Network Bot Started")

    app.run_polling()


if __name__ == "__main__":
    main()
   
