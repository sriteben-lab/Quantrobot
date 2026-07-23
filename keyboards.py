from telegram import ReplyKeyboardMarkup

# ==========================
# Main Menu
# ==========================
main_menu = ReplyKeyboardMarkup(
    [
        ["🆕 New User Registration"],
        ["💼 Wallet", "📈 Investment Plans"],
        ["👥 Referrals", "🪪 KYC Status"],
        ["📤 Submit KYC", "💰 Submit Refund Request"],
        ["📊 Check Status", "💬 Chat with Support"],
        ["📋 My Profile"],
        ["🛠 Admin Panel"],
        ["ℹ️ Help"],
]
    ],
    resize_keyboard=True
)

# ==========================
# Wallet Menu
# ==========================
wallet_menu = ReplyKeyboardMarkup(
    [
        ["💳 Fund Wallet"],
        ["📜 Transaction History"],
        ["🏠 Main Menu"],
    ],
    resize_keyboard=True
)

# ==========================
# Fund Wallet Menu
# ==========================
fund_keyboard = ReplyKeyboardMarkup(
    [
        ["₿ BTC", "♦ ETH"],
        ["💲 USDT (TRC20)", "💲 USDT (ERC20)"],
        ["💲 USDC (ERC20)"],
        ["🏠 Main Menu"],
    ],
    resize_keyboard=True
)

# ==========================
# Cancel Menu
# ==========================
cancel_menu = ReplyKeyboardMarkup(
    [
        ["🏠 Main Menu"],
        ["❌ Cancel"],
    ],
    resize_keyboard=True
)
