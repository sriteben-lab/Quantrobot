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
    get_deposit,
    add_wallet_balance,
    get_pending_refunds,
    update_refund_status,
    get_refund,
)
    
admin_menu = ReplyKeyboardMarkup(
    [
        ["📥 Pending Deposits"],
        ["🪪 Pending KYC"],
        ["💰 Pending Refunds"],
        ["📩 Support Inbox"],
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

async def pending_refunds(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    refunds = get_pending_refunds()

    if not refunds:
        await update.message.reply_text("No pending refunds.")
        return

    for refund in refunds:

        refund_id = refund[0]
        user_id = refund[1]
        full_name = refund[2]
        investment_amount = refund[5]
        cryptocurrency = refund[6]

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "✅ Approve",
                    callback_data=f"approve_refund:{refund_id}",
                ),
                InlineKeyboardButton(
                    "❌ Reject",
                    callback_data=f"reject_refund:{refund_id}",
                ),
            ]
        ])

        await update.message.reply_text(
            f"💰 *Pending Refund*\n\n"
            f"👤 {full_name}\n"
            f"🆔 User ID: `{user_id}`\n"
            f"💵 Amount: {investment_amount}\n"
            f"🪙 Crypto: {cryptocurrency}",
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

pending_refunds_handler = MessageHandler(
    filters.Regex("^💰 Pending Refunds$"),
    pending_refunds,
)

async def deposit_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, deposit_id = query.data.split(":")
    deposit_id = int(deposit_id)

    if action == "approve_deposit":

        update_deposit_status(deposit_id, "Approved")

        user_id, amount = get_deposit(deposit_id)

        add_wallet_balance(user_id, amount)

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"✅ Your deposit of ${amount:,.2f} has been approved.\n\n"
                "The funds have been added to your wallet."
            ),
        )

        await query.edit_message_text(
            "✅ Deposit Approved"
        )

    elif action == "reject_deposit":

        update_deposit_status(deposit_id, "Rejected")

        user_id, amount = get_deposit(deposit_id)

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"❌ Your deposit of ${amount:,.2f} has been rejected."
            ),
        )

        await query.edit_message_text(
            "❌ Deposit Rejected"
        )

deposit_callback_handler = CallbackQueryHandler(
    deposit_callback,
    pattern="^(approve_deposit|reject_deposit):",
        )

async def refund_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    action, refund_id = query.data.split(":")
    refund_id = int(refund_id)

    user_id, amount = get_refund(refund_id)

    amount = float(
        str(amount).replace("$", "").replace(",", "").strip()
    )

    if action == "approve_refund":

        update_refund_status(refund_id, "Approved")

        add_wallet_balance(user_id, amount)

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"✅ Your refund request has been approved.\n\n"
                f"${amount:,.2f} has been added to your wallet."
            ),
        )

        await query.edit_message_text(
            "✅ Refund Approved"
        )

    elif action == "reject_refund":

        update_refund_status(refund_id, "Rejected")

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "❌ Your refund request has been rejected."
            ),
        )

        await query.edit_message_text(
            "❌ Refund Rejected"
        )

refund_callback_handler = CallbackQueryHandler(
    refund_callback,
    pattern="^(approve_refund|reject_refund):",
)

