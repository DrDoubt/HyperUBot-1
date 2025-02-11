# Copyright 2020-2021 nunopenim @github
# Copyright 2020-2021 prototype74 @github
#
# Licensed under the PEL (Penim Enterprises License), v1.0
#
# You may not use this file or any of the content within it, unless in
# compliance with the PE License

from userbot import log
from os.path import basename

if basename(__file__).startswith("config") or \
   basename(__file__).startswith("sample_config"):
    log.error("Please do not just use this sample config as "
              "your main config. Create a new config.py in the same "
              "directory with a proper ConfigClass.")
    quit(1)


class ConfigClass(object):
    # Optional configurations
    #
    # Userbot display language. Default is english ('en')
    #
    UBOT_LANG = "en"  # must match language code

    #
    # Logs any bot event to the specific chat
    #
    LOGGING = False  # Enable or disable logging
    LOGGING_CHATID = None  # Chat ID. Must be an integer

    #
    # To store downloaded file(s) (temporary)
    #
    TEMP_DL_DIR = "./downloads"  # Default

    #
    # Skips load specific module(s) e.g. ["admin"]
    #
    NOT_LOAD_MODULES = []  # must be a list or config will not work

    #
    # Community extra repos, leave as list of strings (or not)
    # The format of the repo should be "<github_username>/<github_repo>"
    # Example: "nunopenim/modules-universe", although this is not a
    #          community repo :)
    #
    COMMUNITY_REPOS = []

    #
    # Allow the bot to sideload modules from Telegram chats.
    # By enabling this config you accept the risk of
    # sideloading modules
    #
    ALLOW_SIDELOAD = False

    #
    # Automactially update the list of repository data when
    # listing packages if the last update was about an hour ago
    #
    PKG_ENABLE_AUTO_UPDATE = False

    #
    # Don't reboot automatically if new user modules are installed
    # or uninstalled
    #
    PKG_DISABLE_AUTO_REBOOT = False
