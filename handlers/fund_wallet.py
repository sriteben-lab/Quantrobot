from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

async def fund_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "💳 Fund Wallet":

        await update.message.reply_text(
"""
💳 FUND WALLET

Choose your deposit method:

₿ BTC

♦ ETH

💲 USDT (TRC20)

💲 USDT (ERC20)

💲 USDC (ERC20)
"""
        )

    elif text == "₿ BTC":

        await update.message.reply_text(
"""
₿ BTC Deposit

Address:

YOUR_BTC_ADDRESS

⚠️ Send only BTC.
"""
        )

    elif text == "♦ ETH":

        await update.message.reply_text(
"""
♦ ETH Deposit

Address:

YOUR_ETH_ADDRESS

⚠️ Send only ETH.
"""
        )

    elif text == "💲 USDT (TRC20)":

        await update.message.reply_text(
"""
USDT (TRC20)

Address:

YOUR_USDT_TRC20_ADDRESS

⚠️ Use the TRON network.
"""
        )

    elif text == "💲 USDT (ERC20)":

        await update.message.reply_text(
"""
USDT (ERC20)

Address:

YOUR_USDT_ERC20_ADDRESS

⚠️ Use the Ethereum network.
"""
        )

    elif text == "💲 USDC (ERC20)":

        await update.message.reply_text(
"""
USDC (ERC20)

Address:

YOUR_USDC_ERC20_ADDRESS

⚠️ Use the Ethereum network.
"""
        )


fund_wallet_handler = MessageHandler(
    filters.TEXT & ~filters.COMMAND,
    fund_wallet,
)
