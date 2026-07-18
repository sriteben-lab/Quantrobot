from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from database import get_user
from keyboards import main_menu

# Replace with your bot username (without @)
BOT_USERNAME = "QuantroNetworkProBot"


async def referrals(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = get_user(update.effective_user.id)

    if not user:
        await update.message.reply_text(
            "❌ Please register first.",
            reply_markup=main_menu,
        )
        return

    referral_link = (
        f"https://t.me/{BOT_USERNAME}?start={update.effective_user.id}"
    )

    referrals_count = user[9]
    affiliate_balance = user[8]

    await update.message.reply_text(
        f"""
👥 *Referral Program*

🔗 *Your Referral Link*

{referral_link}

━━━━━━━━━━━━━━

👤 *Total Referrals*
{referrals_count}

💰 *Affiliate Earnings*
${affiliate_balance:,.2f}

Invite your friends using your personal referral link.

When a referred user makes their first verified investment, you'll receive a commission automatically.
""",
        parse_mode="Markdown",
        reply_markup=main_menu,
    )


referral_handler = MessageHandler(
    filters.Regex("^👥 Referrals$"),
    referrals,
      )
