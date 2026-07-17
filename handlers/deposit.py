from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

AMOUNT = 0

submit_keyboard = ReplyKeyboardMarkup(
    [
        ["📤 Submit Transaction Hash"],
        ["🏠 Main Menu"],
    ],
    resize_keyboard=True,
)


# ---------------- BTC ----------------

async def select_btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["network"] = "BTC"

    await update.message.reply_text(
        "💰 Enter the amount of BTC you want to deposit:"
    )

    return AMOUNT


# ---------------- ETH ----------------

async def select_eth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["network"] = "ETH"

    await update.message.reply_text(
        "💰 Enter the amount of ETH you want to deposit:"
    )

    return AMOUNT


# ---------------- USDT TRC20 ----------------

async def select_usdt_trc20(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["network"] = "USDT TRC20"

    await update.message.reply_text(
        "💰 Enter the amount of USDT (TRC20) you want to deposit:"
    )

    return AMOUNT


# ---------------- USDT ERC20 ----------------

async def select_usdt_erc20(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["network"] = "USDT ERC20"

    await update.message.reply_text(
        "💰 Enter the amount of USDT (ERC20) you want to deposit:"
    )

    return AMOUNT


# ---------------- USDC ERC20 ----------------

async def select_usdc_erc20(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["network"] = "USDC ERC20"

    await update.message.reply_text(
        "💰 Enter the amount of USDC (ERC20) you want to deposit:"
    )

    return AMOUNT


# ---------------- Receive Amount ----------------

async def get_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):

    amount = update.message.text

    try:
        amount = float(amount)
    except ValueError:
        await update.message.reply_text(
            "❌ Please enter a valid amount."
        )
        return AMOUNT

    context.user_data["amount"] = amount

    network = context.user_data["network"]

    addresses = {
        "BTC": "YOUR_BTC_ADDRESS",
        "ETH": "YOUR_ETH_ADDRESS",
        "USDT TRC20": "YOUR_USDT_TRC20_ADDRESS",
        "USDT ERC20": "YOUR_USDT_ERC20_ADDRESS",
        "USDC ERC20": "YOUR_USDC_ERC20_ADDRESS",
    }

    minimums = {
        "BTC": "0.0001 BTC",
        "ETH": "0.005 ETH",
        "USDT TRC20": "10 USDT",
        "USDT ERC20": "10 USDT",
        "USDC ERC20": "10 USDC",
    }

    await update.message.reply_text(
        f"""
💳 *Deposit Details*

🌐 Network:
{network}

💰 Amount:
{amount}

📥 Deposit Address:
`{addresses[network]}`

Minimum Deposit:
{minimums[network]}

━━━━━━━━━━━━━━

After sending payment:

1️⃣ Copy your Transaction Hash (TXID)

2️⃣ Click **📤 Submit Transaction Hash**

3️⃣ Paste your TXID

⚠️ Send funds only through the selected network.
""",
        parse_mode="Markdown",
        reply_markup=submit_keyboard,
    )

    return ConversationHandler.END


deposit_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("^₿ BTC$"), select_btc),
        MessageHandler(filters.Regex("^♦ ETH$"), select_eth),
        MessageHandler(filters.Regex("^💲 USDT \\(TRC20\\)$"), select_usdt_trc20),
        MessageHandler(filters.Regex("^💲 USDT \\(ERC20\\)$"), select_usdt_erc20),
        MessageHandler(filters.Regex("^💲 USDC \\(ERC20\\)$"), select_usdc_erc20),
    ],
    states={
        AMOUNT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                get_amount,
            )
        ]
    },
    fallbacks=[],
    )
