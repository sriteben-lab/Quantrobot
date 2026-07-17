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

    for network, amount, txid, status in deposits:
        message += (
            f"🌐 Network: {network}\n"
            f"💵 Amount: {amount}\n"
            f"🧾 TX Hash:\n"
            f"`{txid}`\n"
            f"📌 Status: {status}\n"
            "━━━━━━━━━━━━━━\n"
        )

    await update.message.reply_text(
        message,
        reply_markup=wallet_menu,
        parse_mode="Markdown"
    )
