from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

fund_keyboard = ReplyKeyboardMarkup(
    [
        ["₿ BTC", "♦ ETH"],
        ["💲 USDT (TRC20)", "💲 USDT (ERC20)"],
        ["💲 USDC (ERC20)"],
        ["🔙 Back"],
    ],
    resize_keyboard=True,
)

async def fund_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💳 *Fund Wallet*\n\n"
        "Select the cryptocurrency you want to deposit:",
        reply_markup=fund_keyboard,
        parse_mode="Markdown"
    )

fund_wallet_handler = MessageHandler(
    filters.Regex("^💳 Fund Wallet$"),
    fund_wallet
)
