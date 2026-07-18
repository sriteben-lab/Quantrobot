from telegram import Update
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

from config import ADMIN_ID
from database import add_refund, get_user
from keyboards import main_menu

TXID, REASON = range(2)


async def start_refund(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    if not user:
        await update.message.reply_text(
            "❌ Please register first.",
            reply_markup=main_menu,
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "📄 Please paste the Transaction Hash (TXID) of the deposit you want refunded."
    )

    return TXID


async def refund_txid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["refund_txid"] = update.message.text.strip()

    await update.message.reply_text(
        "📝 Please describe the reason for your refund request."
    )

    return REASON


async def refund_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reason = update.message.text.strip()

    user = get_user(update.effective_user.id)

    full_name = user[1]

    txid = context.user_data["refund_txid"]

    add_refund(
        update.effective_user.id,
        full_name,
        txid,
        reason,
    )

    # Notify Admin
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"""
🚨 New Refund Request

👤 Name:
{full_name}

🆔 User ID:
{update.effective_user.id}

TXID:
{txid}

Reason:
{reason}

Status:
Pending Review
""",
    )

    await update.message.reply_text(
        """
✅ Your refund request has been submitted successfully.

Our team will review your request.

You will be notified once a decision has been made.
""",
        reply_markup=main_menu,
    )

    context.user_data.pop("refund_txid", None)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Refund request cancelled.",
        reply_markup=main_menu,
    )

    return ConversationHandler.END


refund_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex("^💰 Submit Refund Request$"),
            start_refund,
        )
    ],
    states={
        TXID: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                refund_txid,
            )
        ],
        REASON: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                refund_reason,
            )
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
    ],
)
