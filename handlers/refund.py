from telegram import (
    Update,
    ReplyKeyboardMarkup,
)

from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

from config import ADMIN_ID
from database import add_refund
from keyboards import main_menu


# ==========================================
# Conversation States
# ==========================================

(
    DATE,
    PROFILE,
    AMOUNT,
    CRYPTO,
    WALLET,
    ADDRESS,
    EVIDENCE,
) = range(7)


# ==========================================
# Keyboards
# ==========================================

done_keyboard = ReplyKeyboardMarkup(
    [
        ["✅ Done"],
        ["❌ Cancel"],
    ],
    resize_keyboard=True,
)


# ==========================================
# STEP 1 OF 7
# ==========================================

async def refund_request(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data.clear()

    context.user_data["refund_photos"] = []

    context.user_data["refund_text"] = ""

    await update.message.reply_text(
        "💰 *Refund Request Form*\n\n"

        "*Step 1 of 7*\n\n"

        "📅 When did you make the investment?\n\n"

        "Example:\n"

        "15 June 2025",

        parse_mode="Markdown",
    )

    return DATE


# ==========================================
# STEP 2 OF 7
# ==========================================

async def investment_date(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data["investment_date"] = update.message.text

    await update.message.reply_text(
        "*Step 2 of 7*\n\n"

        "👤 What is your account Username or User ID associated with your profile?\n\n"

        "Example:\n"

        "Username: JohnDoe\n\n"

        "or\n\n"

        "User ID: 123456789",

        parse_mode="Markdown",
    )

    return PROFILE


# ==========================================
# STEP 3 OF 7
# ==========================================

async def profile_id(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data["profile_id"] = update.message.text

    await update.message.reply_text(
        "*Step 3 of 7*\n\n"

        "💵 What amount did you invest?\n\n"

        "Example:\n"

        "$250",

        parse_mode="Markdown",
    )

    return AMOUNT


# ==========================================
# STEP 4 OF 7
# ==========================================

async def investment_amount(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data["investment_amount"] = update.message.text

    await update.message.reply_text(
        "*Step 4 of 7*\n\n"

        "🪙 Which cryptocurrency/network was used for the deposit?\n\n"

        "Examples:\n\n"

        "• BTC\n"
        "• ETH\n"
        "• USDT (TRC20)\n"
        "• USDT (ERC20)\n"
        "• USDC (ERC20)",

        parse_mode="Markdown",
    )

    return CRYPTO
    
# ==========================================
# STEP 5 OF 7
# ==========================================

async def cryptocurrency(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data["cryptocurrency"] = update.message.text

    await update.message.reply_text(
        "*Step 5 of 7*\n\n"

        "🏦 Which exchange or wallet did you use to send the funds?\n\n"

        "Examples:\n\n"

        "• Binance\n"
        "• Trust Wallet\n"
        "• Coinbase\n"
        "• Bybit\n"
        "• OKX\n"
        "• MetaMask\n"
        "• Klever Wallet",

        parse_mode="Markdown",
    )

    return WALLET


# ==========================================
# STEP 6 OF 7
# ==========================================

async def exchange_wallet(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data["exchange_wallet"] = update.message.text

    await update.message.reply_text(
        "*Step 6 of 7*\n\n"

        "📤 What wallet address did you send the funds from?\n\n"

        "Please paste the complete sending wallet address.",

        parse_mode="Markdown",
    )

    return ADDRESS


# ==========================================
# STEP 7 OF 7
# ==========================================

async def sender_wallet(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data["sender_wallet"] = update.message.text

    context.user_data["refund_text"] = ""

    context.user_data["refund_photos"] = []

    await update.message.reply_text(
        "*Step 7 of 7*\n\n"

        "📎 Provide your transaction evidence.\n\n"

        "Please upload:\n\n"

        "• Transaction Hash (TXID)\n"
        "• Deposit Receipt\n"
        "• Screenshot(s)\n"
        "• Photo(s)\n\n"

        "If you have multiple transactions, label them clearly.\n\n"

        "Example:\n\n"

        "Transaction 1\n\n"

        "TXID:\n"

        "xxxxxxxxxxxxxxxxxxxxxxxx\n\n"

        "Transaction 2\n\n"

        "TXID:\n"

        "yyyyyyyyyyyyyyyyyyyyyyyy\n\n"

        "📷 You may upload multiple screenshots or photos.\n\n"

        "When you have finished uploading everything, press ✅ Done.",

        parse_mode="Markdown",
        reply_markup=done_keyboard,
    )

    return EVIDENCE


# ==========================================
# RECEIVE PHOTO
# ==========================================

async def receive_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    file_id = update.message.photo[-1].file_id

    context.user_data["refund_photos"].append(file_id)

    await update.message.reply_text(
        "✅ Screenshot received.\n\n"
        "You can upload another screenshot or press ✅ Done.",
        reply_markup=done_keyboard,
    )

    return EVIDENCE


# ==========================================
# RECEIVE IMAGE AS DOCUMENT
# ==========================================

async def receive_document(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if (
        update.message.document
        and update.message.document.mime_type
        and update.message.document.mime_type.startswith("image/")
    ):

        context.user_data["refund_photos"].append(
            update.message.document.file_id
        )

        await update.message.reply_text(
            "✅ Image received.\n\n"
            "Upload another image or press ✅ Done.",
            reply_markup=done_keyboard,
        )

    return EVIDENCE


# ==========================================
# RECEIVE TXID / EVIDENCE TEXT
# ==========================================

async def evidence(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if update.message.text == "✅ Done":
        return await finish_refund(update, context)

    previous = context.user_data.get("refund_text", "")

    context.user_data["refund_text"] = (
        previous
        + "\n\n"
        + update.message.text
    )

    await update.message.reply_text(
        "✅ Evidence saved.\n\n"
        "You may upload more screenshots, photos or TXIDs.\n\n"
        "Press ✅ Done when finished.",
        reply_markup=done_keyboard,
    )

    return EVIDENCE
    
# ==========================================
# FINISH REFUND
# ==========================================

async def finish_refund(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    add_refund(
    user_id=update.effective_user.id,
    full_name=update.effective_user.full_name,
    investment_date=context.user_data.get("investment_date", ""),
    profile_id=context.user_data.get("profile_id", ""),
    investment_amount=context.user_data.get("investment_amount", ""),
    cryptocurrency=context.user_data.get("cryptocurrency", ""),
    exchange_wallet=context.user_data.get("exchange_wallet", ""),
    sender_wallet=context.user_data.get("sender_wallet", ""),
    evidence_text=context.user_data.get("refund_text", ""),
    evidence_file_ids=",".join(context.user_data.get("refund_photos", [])),
)

    admin_message = (
        "💰 *NEW REFUND REQUEST*\n\n"

        f"👤 User ID: {update.effective_user.id}\n\n"

        f"📅 Investment Date:\n"
        f"{context.user_data.get('investment_date', '')}\n\n"

        f"🆔 Username / User ID:\n"
        f"{context.user_data.get('profile_id', '')}\n\n"

        f"💵 Investment Amount:\n"
        f"{context.user_data.get('investment_amount', '')}\n\n"

        f"🪙 Cryptocurrency:\n"
        f"{context.user_data.get('cryptocurrency', '')}\n\n"

        f"🏦 Exchange / Wallet:\n"
        f"{context.user_data.get('exchange_wallet', '')}\n\n"

        f"📤 Sender Wallet Address:\n"
        f"{context.user_data.get('sender_wallet', '')}\n\n"

        f"📎 Evidence / TXIDs:\n"
        f"{context.user_data.get('refund_text', '')}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_message,
        parse_mode="Markdown",
    )

    for photo in context.user_data.get("refund_photos", []):
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo,
        )

    await update.message.reply_text(
        "✅ *Your refund request has been submitted successfully.*\n\n"

        "Your request has been forwarded to our Refund Review Team.\n\n"

        "To help speed up the investigation and any eligible refund or balance credit, "
        "please complete your *Know Your Customer (KYC)* verification if you have not already done so.\n\n"

        "Completing KYC helps us verify account ownership, protect your funds, "
        "and process approved refund requests more efficiently.\n\n"

        "You will be notified once the review has been completed.",

        parse_mode="Markdown",
        reply_markup=main_menu,
    )

    context.user_data.clear()

    return ConversationHandler.END


# ==========================================
# CANCEL
# ==========================================

async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data.clear()

    await update.message.reply_text(
        "❌ Refund request cancelled.",
        reply_markup=main_menu,
    )

    return ConversationHandler.END


# ==========================================
# CONVERSATION HANDLER
# ==========================================

refund_handler = ConversationHandler(

    entry_points=[
        MessageHandler(
            filters.Regex("^💰 Submit Refund Request$"),
            refund_request,
        )
    ],

    states = {
    DATE: [
        MessageHandler(filters.TEXT & ~filters.COMMAND, investment_date)
    ],

    PROFILE: [
        MessageHandler(filters.TEXT & ~filters.COMMAND, profile_id)
    ],

    AMOUNT: [
        MessageHandler(filters.TEXT & ~filters.COMMAND, investment_amount)
    ],

    CRYPTO: [
        MessageHandler(filters.TEXT & ~filters.COMMAND, cryptocurrency)
    ],

    WALLET: [
        MessageHandler(filters.TEXT & ~filters.COMMAND, exchange_wallet)
    ],

    ADDRESS: [
        MessageHandler(filters.TEXT & ~filters.COMMAND, sender_wallet)
    ],

    EVIDENCE: [
        MessageHandler(filters.PHOTO, receive_photo),
        MessageHandler(filters.TEXT & ~filters.COMMAND, finish_refund),
    ],
}

            MessageHandler(
                filters.Document.IMAGE,
                receive_document,
            ),

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                evidence,
            ),
        ],
    },

    fallbacks=[
        CommandHandler(
            "cancel",
            cancel,
        )
    ],
)
