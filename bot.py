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
from handlers.help import help_handler
from handlers.referrals import referral_handler
from handlers.refund import refund_handler
from handlers.support_inbox import support_inbox_handler
from handlers.open_ticket import open_ticket_handler
from handlers.admin_reply import admin_reply_handler

from handlers.kyc import (
    kyc_handler,
    kyc_status,
)

from handlers.kyc_admin import (
    approve_kyc_handler,
    reject_kyc_handler,
    kyc_callback_handler,
)

from handlers.support import support
from handlers.support_inbox import support_inbox

from handlers.admin_panel import (
    admin_panel,
    pending_kyc,
    pending_deposits,
    pending_refunds,
    admin_panel_handler,
    pending_kyc_handler,
    pending_deposits_handler,
    pending_refunds_handler,
    deposit_callback_handler,
    refund_callback_handler,
)

from handlers.check_status import (
    check_status,
    check_status_handler,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.args:
        try:
            context.user_data["referrer_id"] = int(context.args[0])
        except ValueError:
            pass

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

    print(f"BUTTON PRESSED: {text}")

    if text == "🏠 Main Menu":
        await update.message.reply_text(
            "🏠 Main Menu",
            reply_markup=main_menu,
        )
        return

    elif text == "📈 Investment Plans":
        await update.message.reply_text(
            "📈 Investment module is under development."
        )
        return

    elif text == "👥 Referrals":
        await update.message.reply_text(
            "👥 Referral module is under development."
        )
        return

    elif text == "🪪 KYC Status":
        await kyc_status(update, context)
        return

    elif text == "📊 Check Status":
        await check_status(update, context)
        return

    elif text == "💬 Chat with Support":
        await support(update, context)
        return

    elif text == "🛠 Admin Panel":
        await admin_panel(update, context)
        return

    elif text == "📥 Pending Deposits":
        await pending_deposits(update, context)
        return

    elif text == "🪪 Pending KYC":
        await pending_kyc(update, context)
        return

    elif text == "💰 Pending Refunds":
        await pending_refunds(update, context)
        return

    elif text == "📩 Support Inbox":
        await support_inbox(update, context)
        return

    elif text == "ℹ️ Help":
        await help_command(update, context)
        return

def main():
    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    menu_filter = filters.Regex(
        r"^(📈 Investment Plans|👥 Referrals|🪪 KYC Status|📊 Check Status|💬 Chat with Support|📩 Support Inbox|📥 Pending Deposits|🪪 Pending KYC|💰 Pending Refunds|🏠 Main Menu|🛠 Admin Panel|ℹ️ Help)$"
    )

    app.add_handler(
        MessageHandler(
            menu_filter,
            buttons,
        )
    )
    
    app.add_handler(registration_handler)
    app.add_handler(profile_handler)
    app.add_handler(wallet_handler)
    app.add_handler(fund_wallet_handler)
    app.add_handler(deposit_handler)
    app.add_handler(submit_tx_handler)
    app.add_handler(history_handler)
    app.add_handler(support_handler)
    app.add_handler(reply_handler)
    app.add_handler(support_inbox_handler)
    app.add_handler(open_ticket_handler)
    app.add_handler(admin_reply_handler)    
    app.add_handler(help_handler)
    app.add_handler(referral_handler)
    app.add_handler(kyc_handler)
    app.add_handler(approve_kyc_handler)
    app.add_handler(reject_kyc_handler)
    app.add_handler(kyc_callback_handler)
    app.add_handler(refund_handler)
    app.add_handler(check_status_handler)
    app.add_handler(admin_panel_handler)
    app.add_handler(pending_kyc_handler)
    app.add_handler(pending_deposits_handler)
    app.add_handler(deposit_callback_handler)
    app.add_handler(pending_refunds_handler)
    app.add_handler(refund_callback_handler)
    
    print("✅ Quantro Network Bot Started")

    app.run_polling()


if __name__ == "__main__":
    main()
   

