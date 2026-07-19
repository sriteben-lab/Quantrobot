# ==========================================
# IMPORTS
# ==========================================

from telegram import (
    Update,
    ReplyKeyboardMarkup,
)

from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import ADMIN_ID
from database import add_refund
from keyboards import main_menu


# ==========================================
# CONVERSATION STATES
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
# KEYBOARDS
# ==========================================

cancel_keyboard = ReplyKeyboardMarkup(
    [["❌ Cancel"]],
    resize_keyboard=True,
    one_time_keyboard=False,
)

done_keyboard = ReplyKeyboardMarkup(
    [["✅ Done", "❌ Cancel"]],
    resize_keyboard=True,
    one_time_keyboard=False,
)


# ==========================================
# CANCEL REFUND
# ==========================================

async def cancel_refund(
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
        reply_markup=cancel_keyboard,
    )

    return DATE

async def investment_date(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "❌ Cancel":
        return await cancel_refund(update, context)

    context.user_data["investment_date"] = update.message.text

    await update.message.reply_text(
        "*Step 2 of 7*\n\n"
        "👤 Enter your Profile ID.",
        parse_mode="Markdown",
        reply_markup=cancel_keyboard,
    )

    return PROFILE

async def profile_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "❌ Cancel":
        return await cancel_refund(update, context)

    context.user_data["profile_id"] = update.message.text

    await update.message.reply_text(
        "*Step 3 of 7*\n\n"
        "💵 Enter the investment amount.",
        parse_mode="Markdown",
        reply_markup=cancel_keyboard,
    )

    return AMOUNT

async def investment_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "❌ Cancel":
        return await cancel_refund(update, context)

    context.user_data["investment_amount"] = update.message.text

    await update.message.reply_text(
        "*Step 4 of 7*\n\n"
        "🪙 Which cryptocurrency did you use?",
        parse_mode="Markdown",
        reply_markup=cancel_keyboard,
    )

    return CRYPTO

async def cryptocurrency(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "❌ Cancel":
        return await cancel_refund(update, context)

    context.user_data["cryptocurrency"] = update.message.text

    await update.message.reply_text(
        "*Step 5 of 7*\n\n"
        "🏦 Which exchange or wallet did you send from?",
        parse_mode="Markdown",
        reply_markup=cancel_keyboard,
    )

    return WALLET

async def exchange_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "❌ Cancel":
        return await cancel_refund(update, context)

    context.user_data["exchange_wallet"] = update.message.text

    await update.message.reply_text(
        "*Step 6 of 7*\n\n"
        "📤 Paste the wallet address you sent the funds from.",
        parse_mode="Markdown",
        reply_markup=cancel_keyboard,
    )

    return ADDRESS

async def sender_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "❌ Cancel":
        return await cancel_refund(update, context)

    context.user_data["sender_wallet"] = update.message.text
    context.user_data["refund_text"] = ""
    context.user_data["refund_photos"] = []

    await update.message.reply_text(
        "*Step 7 of 7*\n\n"
        "📎 Upload your evidence.\n\n"
        "You can send:\n"
        "• TXID\n"
        "• Deposit receipt\n"
        "• Screenshot(s)\n"
        "• Photo(s)\n\n"
        "When finished, press ✅ Done.",
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

    photo = update.message.photo[-1]

    context.user_data["refund_photos"].append(photo.file_id)

    await update.message.reply_text(
        "✅ Photo saved.\n\n"
        "Send another photo, TXID or press ✅ Done.",
        reply_markup=done_keyboard,
    )

    return EVIDENCE


# ==========================================
# RECEIVE IMAGE DOCUMENT
# ==========================================

async def receive_document(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    document = update.message.document

    if (
        document
        and document.mime_type
        and document.mime_type.startswith("image/")
    ):
        context.user_data["refund_photos"].append(document.file_id)

        await update.message.reply_text(
            "✅ Image saved.\n\n"
            "Upload another image or press ✅ Done.",
            reply_markup=done_keyboard,
        )

    return EVIDENCE


# ==========================================
# RECEIVE TEXT EVIDENCE
# ==========================================

async def receive_evidence_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    text = update.message.text

    # Cancel
    if text == "❌ Cancel":
        return await cancel_refund(update, context)

    # Finish
    if text == "✅ Done":
        return await finish_refund(update, context)

    current = context.user_data.get("refund_text", "")

    if current:
        current += "\n\n"

    context.user_data["refund_text"] = current + text

    await update.message.reply_text(
        "✅ Evidence saved.\n\n"
        "Send more screenshots, photos or TXIDs.\n"
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

    data = context.user_data

    add_refund(
        investment_date=data.get("investment_date", ""),
        profile_id=data.get("profile_id", ""),
        investment_amount=data.get("investment_amount", ""),
        cryptocurrency=data.get("cryptocurrency", ""),
        exchange_wallet=data.get("exchange_wallet", ""),
        sender_wallet=data.get("sender_wallet", ""),
        evidence=data.get("refund_text", ""),
        photos=data.get("refund_photos", []),
    )

    await update.message.reply_text(
        "✅ Your refund request has been submitted successfully.\n\n"
        "Our support team will review it and contact you if additional information is required.",
        reply_markup=main_menu,
    )

    context.user_data.clear()

    return ConversationHandler.END

EVIDENCE: [
    MessageHandler(filters.PHOTO, receive_photo),
    MessageHandler(filters.Document.IMAGE, receive_document),
    MessageHandler(filters.TEXT & ~filters.COMMAND, receive_evidence_text),
],
fallbacks=[
    MessageHandler(
        filters.Regex("^❌ Cancel$"),
        cancel_refund,
    ),
],
