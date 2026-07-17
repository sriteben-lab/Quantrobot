from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

from database import get_user

fund_keyboard = ReplyKeyboardMarkup(
    [
        ["₿ BTC", "♦ ETH"],
        ["💲 USDT (TRC20)", "💲 USDT (ERC20)"],
        ["💲 USDC (ERC20)"],
        ["🔙 Back"],
    ],
    resize_keyboard=True,
)


wallet_keyboard = ReplyKeyboardMarkup(
    [
        ["💳 Fund Wallet"],
        ["📜 Transaction History"],
        ["🏠 Main Menu"],
    ],
    resize_keyboard=True,
)


async def fund_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Back button
    if update.message.text == "🔙 Back":

        user = get_user(update.effective_user.id)

        if not user:
            await update.message.reply_text(
                "❌ Please register first."
            )
            return

        await update.message.reply_text(
            f"""💼 *QUANTRO WALLET*

━━━━━━━━━━━━━━

💰 Wallet Balance: ${user[7]:.2f}

💵 Affiliate Balance: ${user[8]:.2f}

━━━━━━━━━━━━━━

Choose an option below.
""",
            parse_mode="Markdown",
            reply_markup=wallet_keyboard,
        )

        return

    await update.message.reply_text(
        "💳 *Fund Wallet*\n\n"
        "Select the cryptocurrency you want to deposit:",
        reply_markup=fund_keyboard,
        parse_mode="Markdown",
    )


fund_wallet_handler = MessageHandler(
    filters.Regex("^(💳 Fund Wallet|🔙 Back)$"),
    fund_wallet,
)
