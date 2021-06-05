# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot initialization. """

import os
import sys
from distutils.util import strtobool as sb
from logging import DEBUG, INFO, basicConfig, getLogger
from pathlib import Path
from platform import python_version
from time import sleep

from dotenv import load_dotenv
from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from requests import get
from telethon import TelegramClient, version
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession

from .storage import Storage

STORAGE = lambda n: Storage(Path("data") / n)

load_dotenv("config.env")

# Bot Logs setup:
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE") or "False")

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO
    )
LOGS = getLogger(__name__)

if sys.version_info[0] < 3 or sys.version_info[1] < 8:
    LOGS.info(
        "Você DEVE ter uma versão python de pelo menos 3.8."
        "Vários recursos dependem disso. Bot finalizando."
    )
    sys.exit(1)

# Check if the config was edited by using the already used variable.
# Basically, its the 'virginity check' for the config file ;)
CONFIG_CHECK = (
    os.environ.get("___________PLOX_______REMOVE_____THIS_____LINE__________") or None
)

if CONFIG_CHECK:
    LOGS.info(
        "Remova a linha mencionada na primeira hashtag do arquivo config.env"
    )
    sys.exit(1)

# Telegram App KEY and HASH
API_KEY = int(os.environ.get("API_KEY") or 0)
API_HASH = str(os.environ.get("API_HASH") or None)

# Userbot Session String
STRING_SESSION = os.environ.get("STRING_SESSION") or None

# Logging channel/group ID configuration.
BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID") or 0)

# Userbot logging feature switch.
BOTLOG = sb(os.environ.get("BOTLOG") or "False")
LOGSPAMMER = sb(os.environ.get("LOGSPAMMER") or "False")

# Bleep Blop, this is a bot ;)
PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN") or "True")

# Heroku Credentials for updater.
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME") or None
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY") or None

# Custom (forked) repo URL and BRANCH for updater.
UPSTREAM_REPO_URL = "https://github.com/thewhiteharlot/PurpleBot.git"
UPSTREAM_REPO_BRANCH = "master"

# Console verbose logging
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE") or "False")

# SQL Database URI
DB_URI = os.environ.get("DATABASE_URL") or None

# OCR API key
OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY") or None

# Default .alive name
ALIVE_NAME = str(os.environ.get("ALIVE_NAME")) or None

# Default .alive logo
ALIVE_LOGO = os.environ.get("ALIVE_LOGO") or None

# remove.bg API key
REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY") or None

# Chrome Driver and Chrome Binaries
CHROME_DRIVER = "/usr/bin/chromedriver"
CHROME_BIN = "/usr/bin/chromium"

# OpenWeatherMap API Key
OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID") or None
WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY") or None

# Anti Spambot Config
ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT") or "False")
ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT") or "False")

# Default .alive name
ALIVE_NAME = os.environ.get("ALIVE_NAME") or None

# Time & Date - Country and Time Zone
COUNTRY = str(os.environ.get("COUNTRY") or "")
TZ_NUMBER = int(os.environ.get("TZ_NUMBER") or 1)

# Zipfile module
ZIP_DOWNLOAD_DIRECTORY = os.environ.get("ZIP_DOWNLOAD_DIRECTORY") or "./zips"

# Clean Welcome
CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME") or "False")

# Last.fm Module
BIO_PREFIX = os.environ.get("BIO_PREFIX") or None
DEFAULT_BIO = os.environ.get("DEFAULT_BIO") or None

LASTFM_API = os.environ.get("LASTFM_API") or None
LASTFM_SECRET = os.environ.get("LASTFM_SECRET") or None
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME") or None
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD") or None
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)

lastfm = None
if LASTFM_API and LASTFM_SECRET and LASTFM_USERNAME and LASTFM_PASS:
    try:
        lastfm = LastFMNetwork(
            api_key=LASTFM_API,
            api_secret=LASTFM_SECRET,
            username=LASTFM_USERNAME,
            password_hash=LASTFM_PASS,
        )
    except Exception:
        pass

# Google Drive Module
G_DRIVE_DATA = os.environ.get("G_DRIVE_DATA") or None
G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID") or None
G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET") or None
G_DRIVE_AUTH_TOKEN_DATA = os.environ.get("G_DRIVE_AUTH_TOKEN_DATA") or None
G_DRIVE_FOLDER_ID = os.environ.get("G_DRIVE_FOLDER_ID") or None
G_DRIVE_INDEX_URL = os.environ.get("G_DRIVE_INDEX_URL") or None

TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY") or "./downloads/"

# Terminal Alias
TERM_ALIAS = os.environ.get("TERM_ALIAS") or None

# Deezloader
DEEZER_ARL_TOKEN = os.environ.get("DEEZER_ARL_TOKEN") or None

# Genius Lyrics API
GENIUS = os.environ.get("GENIUS_ACCESS_TOKEN") or None

# Uptobox
USR_TOKEN = os.environ.get("USR_TOKEN_UPTOBOX") or None

# PurpleBot version
PURPLEBOT_VERSION = "5.0.2"


def migration_workaround():
    try:
        from userbot.modules.sql_helper.globals import addgvar, delgvar, gvarstatus
    except:
        return None

    old_ip = gvarstatus("public_ip")
    new_ip = get("https://api.ipify.org").text

    if old_ip is None:
        delgvar("public_ip")
        addgvar("public_ip", new_ip)
        return None

    if old_ip == new_ip:
        return None

    sleep_time = 180
    LOGS.info(
        f"Uma mudança no endereço IP foi detectada, esperando por {sleep_time / 60} minutos antes de iniciar o bot."
    )
    sleep(sleep_time)
    LOGS.info("Inicializando o bot...")

    delgvar("public_ip")
    addgvar("public_ip", new_ip)
    return None


if HEROKU_APP_NAME is not None and HEROKU_API_KEY is not None:
    migration_workaround()


# 'bot' variable
if STRING_SESSION:
    # pylint: disable=invalid-name
    bot = TelegramClient(
        session=StringSession(STRING_SESSION),
        api_id=API_KEY,
        api_hash=API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
    )
else:
    # pylint: disable=invalid-name
    bot = TelegramClient("userbot", API_KEY, API_HASH)


async def check_botlog_chatid():
    if not BOTLOG_CHATID and LOGSPAMMER:
        LOGS.info(
            "Você deve configurar a variável BOTLOG_CHATID nas variáveis config.env, para que o registro dos logs de erro funcione."
        )
        sys.exit(1)

    elif not BOTLOG_CHATID and BOTLOG:
        LOGS.info(
            "Você deve configurar a variável BOTLOG_CHATID nas variáveis config.env, para que o recurso de registro do userbot funcione."
        )
        sys.exit(1)

    elif not (BOTLOG and LOGSPAMMER):
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info(
            "Sua conta não tem permissão para enviar mensagens para BOTLOG_CHATID. "
            " Verifique se você digitou o ID do bate-papo corretamente."
        )
        sys.exit(1)


with bot:
    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except BaseException:
        LOGS.info(
            "BOTLOG_CHATID não é uma variável válida "
            " Verifique suas VARS ou arquivo config.env."
        )
        sys.exit(1)


async def update_restart_msg(chat_id, msg_id):
    DEFAULTUSER = ALIVE_NAME or "Defina a ConfigVar `ALIVE_NAME`!"
    message = (
            f"👾 **PurpleBot**   ➡️  `{PURPLEBOT_VERSION}` \n"
            f"⚙️ **Telethon**     ➡️  `{version.__version__}` \n"
            f"🐍 **Python**        ➡️  `{python_version()}` \n"
            f"👤 **Usuário**       ➡️   `{DEFAULTUSER}` "
            "\n\n__Userbot iniciado__ ☑️"
        )
    await bot.edit_message(chat_id, msg_id, message)
    return True


try:
    from userbot.modules.sql_helper.globals import delgvar, gvarstatus

    chat_id, msg_id = gvarstatus("restartstatus").split("\n")
    with bot:
        try:
            bot.loop.run_until_complete(update_restart_msg(int(chat_id), int(msg_id)))
        except:
            pass
    delgvar("restartstatus")
except AttributeError:
    pass

# Global Variables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
CMD_HELP = {}
ISAFK = False
AFKREASON = None
