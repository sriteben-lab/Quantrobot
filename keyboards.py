from telegram import ReplyKeyboardMarkup

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

cancel_menu = ReplyKeyboardMarkup(
    [
        ["🏠 Main Menu"],
        ["❌ Cancel"]
    ],
    resize_keyboard=True
)