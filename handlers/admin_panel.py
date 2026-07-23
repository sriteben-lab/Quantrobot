from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    filters,
)

from config import ADMIN_ID
from keyboards import main_menu


admin_menu = ReplyKeyboardMarkup(
    [
        ["📥 Pending Deposits"],
        ["🪪 Pending KYC"],
        ["💰 Pending Refunds"],
        ["💬 Support Inbox"],
        ["👥 Users", "📊 Statistics"],
        ["🏠 Main Menu"],
    ],
    resize_keyboard=True,
)


async def admin_panel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "❌ Unauthorized.",
            reply_markup=main_menu,
        )

        return

    await update.message.reply_text(
        "🛠 *Admin Dashboard*\n\n"
        "Select an option below.",
        parse_mode="Markdown",
        reply_markup=admin_menu,
    )


admin_panel_handler = MessageHandler(
    filters.Regex("^🛠 Admin Panel$"),
    admin_panel,
)
