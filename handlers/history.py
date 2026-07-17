from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from database import get_user_deposits
from keyboards import wallet_menu


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):

    deposits = get_user_deposits(update.effective_user.id)

    if not deposits:
        await update.message.reply_text(
            "📜 No transactions found.",
            reply_markup=wallet_menu
        )
        return

    message = "📜 *Transaction History*\n\n"

    for network, usd_amount, crypto_amount, txid, status in deposits:

        crypto_text = (
            f"{crypto_amount:.8f}"
            if crypto_amount is not None
            else "Pending Calculation"
        )

        message += (
            f"🌐 Network: {network}\n"
            f"💵 Deposit Value: ${usd_amount:.2f}\n"
            f"🪙 Crypto Amount: {crypto_text}\n"
            f"🧾 TX Hash:\n"
            f"`{txid}`\n"
            f"📌 Status: {status}\n"
            "━━━━━━━━━━━━━━\n"
        )

    await update.message.reply_text(
        message,
        parse_mode="Markdown",
        reply_markup=wallet_menu
    )


history_handler = MessageHandler(
    filters.Regex("^📜 Transaction History$"),
    history,
)
