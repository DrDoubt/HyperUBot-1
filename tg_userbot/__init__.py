# tguserbot stuff
from tg_userbot.include.colors import LogColorFormatter

# Telethon Stuff
from telethon import TelegramClient
from telethon.sessions import StringSession

# Misc
from dotenv import load_dotenv
from logging import StreamHandler, basicConfig, INFO, getLogger
from os import path, environ, mkdir
from platform import system
from sys import version_info  # check python version

# Terminal logging
log = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(LogColorFormatter())
basicConfig(handlers=[handler], level=INFO)

CURR_PATH = path.dirname(__file__)
OS = system()  # Current Operating System

if version_info[0] < 3 or version_info[1] < 8:
    log.error("Required Python 3.8!")
    quit(1)

if OS and OS.lower().startswith("win"):
    CURR_PATH += "\\"  # Windows backslash path
else:
    CURR_PATH += "/"  # Other Linux systems or macOS

if path.exists(CURR_PATH + "config.env"):
    load_dotenv(CURR_PATH + "config.env")
    SAMPLE_CONFIG = environ.get("SAMPLE_CONFIG", None)
    if SAMPLE_CONFIG:
        log.error("Please remove SAMPLE_CONFIG from config.env!")
        quit(1)
    API_KEY = environ.get("API_KEY", None)
    API_HASH = environ.get("API_HASH", None)
    LOGGING = environ.get("LOGGING", False)
    LOGGING_CHATID = int(environ.get("LOGGING_CHATID", "0"))
    STRING_SESSION = environ.get("STRING_SESSION", None)
    TEMP_DL_DIR = environ.get("TEMP_DL_DIR", "./downloads")
    UBOT_LANG = environ.get("UBOT_LANG", "en")
    NOT_LOAD_MODULES = environ.get("NOT_LOAD_MODULES", [])
elif path.exists(CURR_PATH + "config.py"):
    try:
        from tg_userbot.config import ConfigClass  # Import here, otherwise error
    except ImportError as ie:
        log.error(f"Couldn't import ConfigClass: {ie}")
        quit(1)
    API_KEY = ConfigClass.API_KEY if hasattr(ConfigClass, "API_KEY") else None
    API_HASH = ConfigClass.API_HASH if hasattr(ConfigClass, "API_HASH") else None
    LOGGING = ConfigClass.LOGGING if hasattr(ConfigClass, "LOGGING") else False
    LOGGING_CHATID = ConfigClass.LOGGING_CHATID if hasattr(ConfigClass, "LOGGING_CHATID") else 0
    STRING_SESSION = ConfigClass.STRING_SESSION if hasattr(ConfigClass, "STRING_SESSION") else None
    TEMP_DL_DIR = ConfigClass.TEMP_DL_DIR if hasattr(ConfigClass, "TEMP_DL_DIR") else "./downloads"
    UBOT_LANG = ConfigClass.UBOT_LANG if hasattr(ConfigClass, "UBOT_LANG") else "en"
    NOT_LOAD_MODULES = ConfigClass.NOT_LOAD_MODULES if hasattr(ConfigClass, "NOT_LOAD_MODULES") else []
else:
    log.error("No Config file found! Make sure it's located in ./tg_userbot/config.* or setup your config file first if you didn't. " +
    "Environment and py scripts are supported.")
    quit(1)

if OS and OS.lower().startswith("win"):
    TEMP_DL_DIR += "\\"
else:
    TEMP_DL_DIR += "/"

try:
    if not path.exists(TEMP_DL_DIR):
        mkdir(TEMP_DL_DIR)
except OSError:
    log.error("Failed to initialize download directory.")

if not API_KEY:
    log.error("API KEY is empty! Obtain your API KEY from https://my.telegram.org if you don't have one.")
    quit(1)

if not API_HASH:
    log.error("API HASH is empty! Obtain your API HASH from https://my.telegram.org if you don't have one.")
    quit(1)

try:
    if STRING_SESSION:
        tgclient = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
    else:
        log.warning("STRING SESSION is empty! Please enter your API KEY and HASH to create a new string session.")
        tgclient = TelegramClient("tguserbot", API_KEY, API_HASH)
except Exception as e:
    log.critical(f"Failed to create Telegram Client: {e}")
    quit(1)

# SYSVARS
PROJECT = "tguserbot-X"
VERSION = "0.0.1-DEV_PREV"
ALL_MODULES = []
MODULE_DESC = {}
MODULE_DICT = {}

