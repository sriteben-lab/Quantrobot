from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters


async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "₿ BTC":
        await update.message.reply_text(
            """₿ *BTC Deposit*

Address:
`YOUR_BTC_ADDRESS`

Network: Bitcoin

Minimum Deposit: 0.0001 BTC

⚠️ Send only BTC to this address.
""",
            parse_mode="Markdown"
        )

    elif text == "♦ ETH":
        await update.message.reply_text(
            """♦ *ETH Deposit*

Address:
`YOUR_ETH_ADDRESS`

Network: Ethereum

Minimum Deposit: 0.005 ETH

⚠️ Send only ETH to this address.
""",
            parse_mode="Markdown"
        )

    elif text == "💲 USDT (TRC20)":
        await update.message.reply_text(
            """💲 *USDT (TRC20)*

Address:
`YOUR_USDT_TRC20_ADDRESS`

Network: TRON (TRC20)

Minimum Deposit: 10 USDT

⚠️ Send only USDT via TRC20.
""",
            parse_mode="Markdown"
        )

    elif text == "💲 USDT (ERC20)":
        await update.message.reply_text(
            """💲 *USDT (ERC20)*

Address:
`YOUR_USDT_ERC20_ADDRESS`

Network: Ethereum (ERC20)

Minimum Deposit: 10 USDT

⚠️ Send only USDT via ERC20.
""",
            parse_mode="Markdown"
        )

    elif text == "💲 USDC (ERC20)":
        await update.message.reply_text(
            """💲 *USDC (ERC20)*

Address:
`YOUR_USDC_ERC20_ADDRESS`

Network: Ethereum (ERC20)

Minimum Deposit: 10 USDC

⚠️ Send only USDC via ERC20.
""",
            parse_mode="Markdown"
        )


deposit_handler = MessageHandler(
    filters.TEXT & ~filters.COMMAND,
    deposit,
      )
