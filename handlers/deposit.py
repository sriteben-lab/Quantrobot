from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

submit_keyboard = ReplyKeyboardMarkup(
    [
        ["📤 Submit Transaction Hash"],
        ["💳 Fund Wallet"],
        ["🔙 Back"],
    ],
    resize_keyboard=True,
)


async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "₿ BTC":
        context.user_data["network"] = "BTC"

        await update.message.reply_text(
            """₿ *BTC Deposit*

Address:
`YOUR_BTC_ADDRESS`

Network:
Bitcoin

Minimum Deposit:
0.0001 BTC

━━━━━━━━━━━━━━

After sending payment:

1️⃣ Copy your Transaction Hash (TXID)

2️⃣ Click **📤 Submit Transaction Hash**

3️⃣ Paste your TXID

⚠️ Send only BTC to this address.
""",
            parse_mode="Markdown",
            reply_markup=submit_keyboard,
        )

    elif text == "♦ ETH":
        context.user_data["network"] = "ETH"

        await update.message.reply_text(
            """♦ *ETH Deposit*

Address:
`YOUR_ETH_ADDRESS`

Network:
Ethereum

Minimum Deposit:
0.005 ETH

━━━━━━━━━━━━━━

After sending payment:

1️⃣ Copy your Transaction Hash (TXID)

2️⃣ Click **📤 Submit Transaction Hash**

3️⃣ Paste your TXID

⚠️ Send only ETH to this address.
""",
            parse_mode="Markdown",
            reply_markup=submit_keyboard,
        )

    elif text == "💲 USDT (TRC20)":
        context.user_data["network"] = "USDT TRC20"

        await update.message.reply_text(
            """💲 *USDT (TRC20)*

Address:
`YOUR_USDT_TRC20_ADDRESS`

Network:
TRON (TRC20)

Minimum Deposit:
10 USDT

━━━━━━━━━━━━━━

After sending payment:

1️⃣ Copy your Transaction Hash (TXID)

2️⃣ Click **📤 Submit Transaction Hash**

3️⃣ Paste your TXID

⚠️ Send only USDT through the TRC20 network.
""",
            parse_mode="Markdown",
            reply_markup=submit_keyboard,
        )

    elif text == "💲 USDT (ERC20)":
        context.user_data["network"] = "USDT ERC20"

        await update.message.reply_text(
            """💲 *USDT (ERC20)*

Address:
`YOUR_USDT_ERC20_ADDRESS`

Network:
Ethereum (ERC20)

Minimum Deposit:
10 USDT

━━━━━━━━━━━━━━

After sending payment:

1️⃣ Copy your Transaction Hash (TXID)

2️⃣ Click **📤 Submit Transaction Hash**

3️⃣ Paste your TXID

⚠️ Send only USDT through the ERC20 network.
""",
            parse_mode="Markdown",
            reply_markup=submit_keyboard,
        )

    elif text == "💲 USDC (ERC20)":
        context.user_data["network"] = "USDC ERC20"

        await update.message.reply_text(
            """💲 *USDC (ERC20)*

Address:
`YOUR_USDC_ERC20_ADDRESS`

Network:
Ethereum (ERC20)

Minimum Deposit:
10 USDC

━━━━━━━━━━━━━━

After sending payment:

1️⃣ Copy your Transaction Hash (TXID)

2️⃣ Click **📤 Submit Transaction Hash**

3️⃣ Paste your TXID

⚠️ Send only USDC through the ERC20 network.
""",
            parse_mode="Markdown",
            reply_markup=submit_keyboard,
        )


deposit_handler = MessageHandler(
    filters.Regex(
        "^(₿ BTC|♦ ETH|💲 USDT \\(TRC20\\)|💲 USDT \\(ERC20\\)|💲 USDC \\(ERC20\\))$"
    ),
    deposit,
        )
