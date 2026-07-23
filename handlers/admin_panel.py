from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from config import ADMIN_ID
from keyboards import main_menu

from database import (
    get_pending_kyc,
    get_pending_deposits,
    update_deposit_status,
)

admin_menu = ReplyKeyboardMarkup(
    [
        ["📥 Pending Deposits"],
        ["🪪 Pending KYC"],
        ["💰 Pending Refunds"],
        ["💬 Support Inbox"],
        ["👥 Users", "📊 Statistics"],
        ["🏠 Main Menu"],
    ],
    resize_keyboard=True,
)


async def admin_panel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "❌ Unauthorized.",
            reply_markup=main_menu,
        )

        return

    await update.message.reply_text(
        "🛠 *Admin Dashboard*\n\n"
        "Select an option below.",
        parse_mode="Markdown",
        reply_markup=admin_menu,
    )
    
async def pending_kyc(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if update.effective_user.id != ADMIN_ID:

        return

    kycs = get_pending_kyc()

    if not kycs:

        await update.message.reply_text(
            "✅ There are no pending KYC submissions."
        )

        return

    for kyc in kycs:

        user_id = kyc[0]
        full_name = kyc[1]
        id_document = kyc[2]
        selfie = kyc[3]

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Approve",
                        callback_data=f"approve_kyc:{user_id}",
                    ),
                    InlineKeyboardButton(
                        "❌ Reject",
                        callback_data=f"reject_kyc:{user_id}",
                    ),
                ]
            ]
        )

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=id_document,
            caption=(
                f"🪪 Pending KYC\n\n"
                f"👤 {full_name}\n"
                f"🆔 {user_id}\n\n"
                "📄 Identity Document"
            ),
            reply_markup=keyboard,
        )

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selfie,
            caption="🤳 Selfie Holding Identity Document",
        )

async def pending_deposits(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    deposits = get_pending_deposits()

    if not deposits:
        await update.message.reply_text("No pending deposits.")
        return

    for deposit in deposits:

        deposit_id = deposit[0]
        user_id = deposit[1]
        network = deposit[2]
        amount = deposit[3]
        crypto_amount = deposit[4]
        txid = deposit[5]

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "✅ Approve",
                    callback_data=f"approve_deposit:{deposit_id}",
                ),
                InlineKeyboardButton(
                    "❌ Reject",
                    callback_data=f"reject_deposit:{deposit_id}",
                ),
            ]
        ])

        await update.message.reply_text(
            f"📥 *Pending Deposit*\n\n"
            f"👤 User ID: `{user_id}`\n"
            f"🌐 Network: {network}\n"
            f"💵 USD: ${amount:,.2f}\n"
            f"🪙 Crypto: {crypto_amount}\n\n"
            f"🔗 TXID:\n`{txid}`",
            parse_mode="Markdown",
            reply_markup=keyboard,
        )

admin_panel_handler = MessageHandler(
    filters.Regex("^🛠 Admin Panel$"),
    admin_panel,
)

pending_kyc_handler = MessageHandler(
    filters.Regex("^🪪 Pending KYC$"),
    pending_kyc,
)

pending_deposits_handler = MessageHandler(
    filters.Regex("^📥 Pending Deposits$"),
    pending_deposits,
        )

async def deposit_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, deposit_id = query.data.split(":")
    deposit_id = int(deposit_id)

    if action == "approve_deposit":
        update_deposit_status(deposit_id, "Approved")
        await query.edit_message_text("✅ Deposit approved.")

    elif action == "reject_deposit":
        update_deposit_status(deposit_id, "Rejected")
        await query.edit_message_text("❌ Deposit rejected.")

deposit_callback_handler = CallbackQueryHandler(
    deposit_callback,
    pattern="^(approve_deposit|reject_deposit):",
        )
