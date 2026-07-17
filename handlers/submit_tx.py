from telegram import Update
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from database import add_deposit

TXID = 0


async def submit_tx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📤 Paste your Transaction Hash (TXID):"
    )
    return TXID


async def save_tx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txid = update.message.text

    network = context.user_data.get("network", "Unknown")

    add_deposit(
        update.effective_user.id,
        network,
        0,
        txid
    )

    await update.message.reply_text(
        "✅ Transaction submitted successfully.\n\n"
        "Your payment is now waiting for blockchain confirmation."
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
                save_tx
            )
        ]
    },
    fallbacks=[],
)
