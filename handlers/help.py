from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from keyboards import main_menu

HELP = 0

help_keyboard = ReplyKeyboardMarkup(
    [
        ["💰 Funding Wallet", "📈 Investments"],
        ["🪪 KYC", "💵 Withdrawals"],
        ["👥 Referrals", "💬 Contact Support"],
        ["🏠 Main Menu"],
    ],
    resize_keyboard=True,
)


async def help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "ℹ️ *Quantro Network Help Center*\n\n"
        "Choose a topic below.",
        parse_mode="Markdown",
        reply_markup=help_keyboard,
    )

    return HELP


async def help_answers(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "💰 Funding Wallet":

        await update.message.reply_text(
            """
💰 *Funding Wallet*

• Open Wallet
• Select Fund Wallet
• Choose a cryptocurrency
• Enter the amount in USD
• Send the exact crypto amount shown
• Submit your transaction hash

Your deposit will be verified automatically.
""",
            parse_mode="Markdown",
        )

    elif text == "📈 Investments":

        await update.message.reply_text(
            """
📈 *Investments*

Choose an investment plan.

Your investment starts after your deposit has been verified.

Profits are credited according to the selected plan.
""",
            parse_mode="Markdown",
        )

    elif text == "🪪 KYC":

        await update.message.reply_text(
            """
🪪 *KYC Verification*

Complete KYC to unlock all platform features.

You'll need:

• Government ID
• Selfie
• Proof of Address
"""
        )

    elif text == "💵 Withdrawals":

        await update.message.reply_text(
            """
💵 *Withdrawals*

Withdrawals are processed after verification.

Ensure your wallet address is correct before submitting.
"""
        )

    elif text == "👥 Referrals":

        await update.message.reply_text(
            """
👥 *Referral Program*

Invite friends.

Earn referral commissions whenever they invest.
"""
        )

    elif text == "💬 Contact Support":

        await update.message.reply_text(
            """
Need additional help?

Go back and press:

💬 Chat with Support
"""
        )

    elif text == "🏠 Main Menu":

        await update.message.reply_text(
            "🏠 Main Menu",
            reply_markup=main_menu,
        )

        return ConversationHandler.END

    return HELP


help_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex("^ℹ️ Help$"),
            help_menu,
        )
    ],
    states={
        HELP: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                help_answers,
            )
        ]
    },
    fallbacks=[],
  )
