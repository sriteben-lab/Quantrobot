from telegram import ReplyKeyboardMarkup

# Main Menu
main_menu = ReplyKeyboardMarkup(
    [
        ["🆕 New User Registration"],
        ["💼 Wallet", "📈 Investment Plans"],
        ["👥 Referrals", "🪪 KYC Status"],
        ["📤 Submit KYC", "💰 Submit Refund Request"],
        ["📊 Check Status", "💬 Chat with Support"],
        ["📋 My Profile"],
        ["ℹ️ Help"]
    ],
    resize_keyboard=True
)

# Wallet Menu
wallet_menu = ReplyKeyboardMarkup(
    [
        ["💳 Fund Wallet"],
        ["📜 Transaction History"],
        ["⬅ Back"]
    ],
    resize_keyboard=True
)

# Cancel Menu
cancel_menu = ReplyKeyboardMarkup(
    [
        ["🏠 Main Menu"],
        ["❌ Cancel"]
    ],
    resize_keyboard=True
)
