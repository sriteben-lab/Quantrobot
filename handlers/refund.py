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


# ==========================
# Conversation States
# ==========================

(
    DATE,
    PROFILE,
    AMOUNT,
    CRYPTO,
    WALLET,
    ADDRESS,
    EVIDENCE,
) = range(7)


# ==========================
# Keyboards
# ==========================

done_keyboard = ReplyKeyboardMarkup(
    [
        ["✅ Done"],
        ["❌ Cancel"],
    ],
    resize_keyboard=True,
)


# ==========================
# Step 1
# ==========================

async def refund_request(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["refund_photos"] = []

    await update.message.reply_text(
        "💰 *Refund Request Form*\n\n"
        "*Step 1 of 7*\n\n"
        "📅 When did you make the investment?\n\n"
        "Example:\n"
        "15 June 2025",
        parse_mode="Markdown",
    )

    return DATE


# ==========================
# Step 2
# ==========================

async def investment_date(update: Update, context: ContextTypes.DEFAULT_TYPE):

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


# ==========================
# Step 3
# ==========================

async def profile_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["profile_id"] = update.message.text

    await update.message.reply_text(
        "*Step 3 of 7*\n\n"
        "💵 What amount did you invest?\n\n"
        "Example:\n"
        "$250",
        parse_mode="Markdown",
    )

    return AMOUNT


# ==========================
# Step 4
# ==========================

async def investment_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):

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
    # ==========================
# Step 5
# ==========================

async def cryptocurrency(update: Update, context: ContextTypes.DEFAULT_TYPE):

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


# ==========================
# Step 6
# ==========================

async def exchange_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["exchange_wallet"] = update.message.text

    await update.message.reply_text(
        "*Step 6 of 7*\n\n"
        "📤 What wallet address did you send the funds from?\n\n"
        "Paste the complete sending wallet address.",
        parse_mode="Markdown",
    )

    return ADDRESS


# ==========================
# Step 7
# ==========================

async def sender_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):

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

        "Transaction 1\n"
        "TXID:\n"
        "xxxxxxxxxxxxxxxx\n\n"

        "Transaction 2\n"
        "TXID:\n"
        "yyyyyyyyyyyyyyyy\n\n"

        "📷 You may upload multiple screenshots or photos.\n\n"

        "When finished, press ✅ Done.",
        parse_mode="Markdown",
        reply_markup=done_keyboard,
    )

    return EVIDENCE


# ==========================
# Collect Text Evidence
# ==========================

async def collect_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "✅ Done":
        return await finish_refund(update, context)

    if update.message.text == "❌ Cancel":
        return await cancel(update, context)

    previous = context.user_data.get("refund_text", "")

    context.user_data["refund_text"] = (
        previous
        + "\n\n"
        + update.message.text
    )

    await update.message.reply_text(
        "✅ Information received.\n\n"
        "Upload more TXIDs/photos or press ✅ Done."
    )

    return EVIDENCE


# ==========================
# Collect Photos
# ==========================

async def collect_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    photo = update.message.photo[-1].file_id

    context.user_data["refund_photos"].append(photo)

    await update.message.reply_text(
        "📷 Screenshot received.\n\n"
        "Upload another one or press ✅ Done."
    )

    return EVIDENCE
# ==========================
# Finish Refund
# ==========================

async def finish_refund(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    full_name = user.full_name

    investment_date = context.user_data["investment_date"]
    profile_id = context.user_data["profile_id"]
    investment_amount = context.user_data["investment_amount"]
    cryptocurrency = context.user_data["cryptocurrency"]
    exchange_wallet = context.user_data["exchange_wallet"]
    sender_wallet = context.user_data["sender_wallet"]

    evidence_text = context.user_data.get(
        "refund_text",
        ""
    )

    photos = context.user_data.get(
        "refund_photos",
        []
    )

    evidence_file_ids = ",".join(photos)

    # Save into database
    add_refund(
        user.id,
        full_name,
        investment_date,
        profile_id,
        investment_amount,
        cryptocurrency,
        exchange_wallet,
        sender_wallet,
        evidence_text,
        evidence_file_ids,
    )

    # ==========================
    # Send to Admin
    # ==========================

    admin_message = f"""
💰 NEW REFUND REQUEST

━━━━━━━━━━━━━━

👤 Name:
{full_name}

🆔 User ID:
{user.id}

📅 Investment Date:
{investment_date}

👤 Profile:
{profile_id}

💵 Amount:
{investment_amount}

🪙 Cryptocurrency:
{cryptocurrency}

🏦 Exchange/Wallet:
{exchange_wallet}

📤 Sender Wallet:
{sender_wallet}

━━━━━━━━━━━━━━

📄 Evidence

{evidence_text}
"""

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_message,
    )

    # Forward uploaded photos
    for photo in photos:
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo,
        )

    # ==========================
    # Confirmation to User
    # ==========================

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


# ==========================
# Cancel
# ==========================

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "❌ Refund request cancelled.",
        reply_markup=main_menu,
    )

    return ConversationHandler.END


# ==========================
# Conversation Handler
# ==========================

refund_handler = ConversationHandler(

    entry_points=[
        MessageHandler(
            filters.Regex("^💰 Submit Refund Request$"),
            refund_request,
        )
    ],

    states={

        DATE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                investment_date,
            )
        ],

        PROFILE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                profile_id,
            )
        ],

        AMOUNT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                investment_amount,
            )
        ],

        CRYPTO: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                cryptocurrency,
            )
        ],

        WALLET: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                exchange_wallet,
            )
        ],

        ADDRESS: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                sender_wallet,
            )
        ],

        EVIDENCE: [

            MessageHandler(
                filters.PHOTO,
                collect_photo,
            ),

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                collect_text,
            ),
        ],
    },

    fallbacks=[
        CommandHandler(
            "cancel",
            cancel,
        )
    ],
),
        
    
