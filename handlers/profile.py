from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from database import get_user


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    if not user:
        await update.message.reply_text(
            "❌ You are not registered.\n\n"
            "Please register first using 🆕 New User Registration."
        )
        return

    message = f"""
👤 *My Profile*

🆔 User ID: {user[0]}

👤 Full Name: {user[1]}
📧 Email: {user[2]}
📱 Phone: {user[3]}
🌍 Country: {user[4]}

💼 Wallet Balance: ${user[7]:.2f}
💵 Affiliate Balance: ${user[8]:.2f}

🪪 KYC Status: {user[6]}
👥 Referrals: {user[9]}
"""

    await update.message.reply_text(
        message,
        parse_mode="Markdown"
    )


profile_handler = MessageHandler(
    filters.Regex("^📋 My Profile$"),
    profile
)
