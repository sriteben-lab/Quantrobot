from telegram import Update
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    CommandHandler,
    filters,
)

from database import add_deposit
from keyboards import main_menu

TXID = 0


async def submit_tx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📤 Please paste your Transaction Hash (TXID).\n\n"
        "After submitting, your transaction will be verified automatically."
    )
    return TXID


async def save_tx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txid = update.message.text.strip()

    network = context.user_data.get("network", "Unknown")
    amount = context.user_data.get("amount", 0)

    add_deposit(
        update.effective_user.id,
        network,
        amount,
        txid
    )

    await update.message.reply_text(
        f"""✅ *Deposit Submitted Successfully*

🌐 Network:
{network}

💰 Amount:
{amount}

📌 Status:
Pending Verification

━━━━━━━━━━━━━━

Your transaction has been received.

The blockchain will be checked automatically.

Once the required confirmations are reached, your wallet balance will be credited automatically.
""",
        parse_mode="Markdown",
        reply_markup=main_menu,
    )

    # Clear temporary deposit data
    context.user_data.pop("network", None)
    context.user_data.pop("amount", None)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Deposit submission cancelled.",
        reply_markup=main_menu,
    )
    return ConversationHandler.END


submit_tx_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex("^📤 Submit Transaction Hash$"),
            submit_tx,
        )
    ],
    states={
        TXID: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                save_tx,
            )
        ]
    },
    fallbacks=[
        CommandHandler("cancel", cancel)
    ],
)
