from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from database import get_user


async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    if not user:
        await update.message.reply_text(
            "❌ Please register first using 🆕 New User Registration."
        )
        return

    message = f"""
💼 *QUANTRO WALLET*

━━━━━━━━━━━━━━━━━━

💰 Wallet Balance: *${user[7]:.2f}*

💵 Affiliate Balance: *${user[8]:.2f}*

━━━━━━━━━━━━━━━━━━

🏦 *Deposit Addresses*

₿ *BTC*
`YOUR_BTC_ADDRESS`

━━━━━━━━━━━━━━━━━━

♦️ *ETH*
`YOUR_ETH_ADDRESS`

━━━━━━━━━━━━━━━━━━

💲 *USDT (TRC20)*
`YOUR_USDT_TRC20_ADDRESS`

━━━━━━━━━━━━━━━━━━

💲 *USDT (ERC20)*
`YOUR_USDT_ERC20_ADDRESS`

━━━━━━━━━━━━━━━━━━

💲 *USDC (ERC20)*
`YOUR_USDC_ERC20_ADDRESS`

━━━━━━━━━━━━━━━━━━

💵 Minimum Deposit: *$50*

⚠️ Always send the correct cryptocurrency to the correct network.
"""

    await update.message.reply_text(
        message,
        parse_mode="Markdown"
    )


wallet_handler = MessageHandler(
    filters.Regex("^💼 Wallet$"),
    wallet
)
