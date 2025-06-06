"""
Sample configuration file for PSonOfLars_BHMarie Telegram Bot.

IMPORTANT:
- DO NOT rename and directly use this file as your own config!
- Instead, create a new 'config.py' in the same directory, import this class, and extend it as needed.
- Never commit your personal API keys, tokens, or passwords to public repositories.
"""

import os
import sys

if not __name__.endswith("sample_config"):
    print(
        "Please extend this sample config to your own config.py file. "
        "Never edit or use this sample directly. Exiting for safety.",
        file=sys.stderr
    )
    quit(1)


class Config(object):
    # LOGGER settings
    LOGGER = True

    # REQUIRED - Must be set in your own config.py for the bot to run!
    API_KEY = os.environ.get("BOT_API_KEY", "YOUR KEY HERE")
    OWNER_ID = int(os.environ.get("BOT_OWNER_ID", 0))  # Integer: Your Telegram user ID
    OWNER_USERNAME = os.environ.get("BOT_OWNER_USERNAME", "YOUR USERNAME HERE")

    # RECOMMENDED
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqldbtype://username:pw@hostname:port/db_name"
    )
    MESSAGE_DUMP = os.environ.get("MESSAGE_DUMP_CHAT_ID", None)
    LOAD = os.environ.get("LOAD_MODULES", "").split(",") if os.environ.get("LOAD_MODULES") else []
    NO_LOAD = os.environ.get("NO_LOAD_MODULES", "char_limit_exceed,translation,rss,sid").split(",")

    WEBHOOK = bool(os.environ.get("BOT_USE_WEBHOOK", False))
    URL = os.environ.get("BOT_WEBHOOK_URL", None)

    # OPTIONAL
    SUDO_USERS = [
        int(x) for x in os.environ.get("SUDO_USERS", "").split(",") if x
    ]  # List of Telegram user IDs
    SUPPORT_USERS = [
        int(x) for x in os.environ.get("SUPPORT_USERS", "").split(",") if x
    ]
    WHITELIST_USERS = [
        int(x) for x in os.environ.get("WHITELIST_USERS", "").split(",") if x
    ]
    DONATION_LINK = os.environ.get("DONATION_LINK", None)
    CERT_PATH = os.environ.get("CERT_PATH", None)
    PORT = int(os.environ.get("PORT", 5000))
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False))
    WORKERS = int(os.environ.get("WORKERS", 8))
    BAN_STICKER = os.environ.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg")
    ALLOW_EXCL = bool(os.environ.get("ALLOW_EXCL", False))
    BMERNU_SCUT_SRELFTI = os.environ.get("BMERNU_SCUT_SRELFTI", None)

    START_MESSAGE = os.environ.get(
        "START_MESSAGE", "https://t.me/c/1235155926/33801"
    )
    START_BUTTONS = os.environ.get("START_BUTTONS", None)

    # SECURITY IMPROVEMENTS:
    # - Sensitive values are loaded from environment variables
    # - OWNER_ID, SUDO_USERS, etc., are ensured to be integers
    # - Never expose real API keys or secrets in source code

    # NEW FEATURES:
    # - Support for loading configuration from environment variables for easy deployment and CI/CD
    # - Dynamic module loading/exclusion via environment variables
    # - Clearer documentation and safer defaults

class Production(Config):
    LOGGER = False

class Development(Config):
    LOGGER = True
