import logging
import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode, ChatType
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler,
    filters, ContextTypes
)
from tg_bot.modules import ALL_MODULES
from tg_bot.modules.helper_funcs.misc import paginate_modules

# Load your config securely (don’t hardcode secrets)
from tg_bot.config import TOKEN, OWNER_ID, DONATION_LINK, WEBHOOK, CERT_PATH, PORT, URL, ALLOW_EXCL, START_MESSAGE, START_BUTTONS

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

HELPABLE = {}
CHAT_SETTINGS = {}
USER_SETTINGS = {}

# Dynamically import modules and register their help/settings hooks
for module_name in ALL_MODULES:
    imported_module = __import__(f"tg_bot.modules.{module_name}", fromlist=["*"])
    name = getattr(imported_module, "__mod_name__", module_name)
    if getattr(imported_module, "__help__", None):
        HELPABLE[name.lower()] = imported_module
    if getattr(imported_module, "__chat_settings__", None):
        CHAT_SETTINGS[name.lower()] = imported_module
    if getattr(imported_module, "__user_settings__", None):
        USER_SETTINGS[name.lower()] = imported_module

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = None
    if START_BUTTONS:
        keyb = []
        # Assume button_markdown_parser is async and returns proper buttons
        _, buttons = await button_markdown_parser(START_BUTTONS)
        for b_name, url, same_line in buttons:
            ik = InlineKeyboardButton(b_name, url=url)
            if same_line and keyb:
                keyb[-1].append(ik)
            else:
                keyb.append([ik])
        keyboard = InlineKeyboardMarkup(keyb)
    await update.message.reply_text(
        START_MESSAGE,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type != ChatType.PRIVATE:
        await update.message.reply_text(
            "Contact me in PM for the list of possible commands.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Help", url=f"t.me/{context.bot.username}?start=help")]
            ])
        )
        return
    await update.message.reply_text("Help text here...")  # Expand as needed

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling update:", exc_info=context.error)
    # Optionally, notify owner/admins

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    # Add more handlers for settings, donate, etc.

    # Error handling
    application.add_error_handler(error_handler)

    if WEBHOOK:
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=URL + TOKEN,
            cert=CERT_PATH if CERT_PATH else None
        )
    else:
        application.run_polling()

if __name__ == "__main__":
    main()
