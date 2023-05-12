import pyrogram
from pyrogram import Client
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
import bypasser
import os
import ddl
import requests
import threading
from texts import HELP_TEXT
from ddl import ddllist
import re


# bot
bot_token = os.environ.get("TOKEN", "")
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "")
OWNER_ID = os.environ.get("OWNER_ID", "")
ADMIN_LIST = [int(ch) for ch in (os.environ.get("ADMIN_LIST", f"{OWNER_ID}")).split()]
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "")
PERMANENT_GROUP = os.environ.get("PERMANENT_GROUP", "-100")
GROUP_ID = [int(ch) for ch in (os.environ.get("GROUP_ID", f"{PERMANENT_GROUP}")).split()]
UPDATES_CHANNEL = str(os.environ.get("UPDATES_CHANNEL", ""))
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)  

# handle ineex
def handleIndex(ele,message,msg):
    result = bypasser.scrapeIndex(ele)
    try: app.delete_messages(message.chat.id, msg.id)
    except: pass
    for page in result: app.send_message(message.chat.id, page, reply_to_message_id=message.id, disable_web_page_preview=True)


# loop thread
def loopthread(message):

    urls = []
    for ele in message.text.split():
        if "http://" in ele or "https://" in ele:
            urls.append(ele)
    if len(urls) == 0: return

    if bypasser.ispresent(ddllist,urls[0]):
        msg = app.send_message(message.chat.id, "⚡ __generating...__", reply_to_message_id=message.id)
    else:
        if urls[0] in "https://olamovies" or urls[0] in "https://psa.pm/":
            msg = app.send_message(message.chat.id, "🔎 __this might take some time...__", reply_to_message_id=message.id)
        else:
            msg = app.send_message(message.chat.id, "🔎 __bypassing...__", reply_to_message_id=message.id)

    link = ""
    for ele in urls:
        if re.search(r"https?:\/\/(?:[\w.-]+)?\.\w+\/\d+:", ele):
            handleIndex(ele,message,msg)
            return
        elif bypasser.ispresent(ddllist,ele):
            try: temp = ddl.direct_link_generator(ele)
            except Exception as e: temp = "**Error**: " + str(e)
        else:    
            try: temp = bypasser.shortners(ele)
            except Exception as e: temp = "**Error**: " + str(e)
        print("bypassed:",temp)
        link = link + temp + "\n\n"
        
    try: app.edit_message_text(message.chat.id, msg.id, f'__{link}__', disable_web_page_preview=True)
    except:
        try: app.edit_message_text(message.chat.id, msg.id, "__Failed to Bypass__")
        except:
            try: app.delete_messages(message.chat.id, msg.id)
            except: pass
            app.send_message(message.chat.id, "__Failed to Bypass__")


# start command
@app.on_message(filters.command(["start"]))
async def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if str(message.chat.id).startswith("-100") and message.chat.id not in GROUP_ID:
        return
    elif message.chat.id not in GROUP_ID:
        if UPDATES_CHANNEL != "None":
            try:
                user = await app.get_chat_member(UPDATES_CHANNEL, message.chat.id)
                if user.status == enums.ChatMemberStatus.BANNED:
                    await app.send_message(
                        chat_id=message.chat.id,
                        text=f"__Sorry, you are banned. Contact My [ Owner ](https://telegram.me/{OWNER_USERNAME})__",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                 await app.send_message(
                    chat_id=message.chat.id,
                    text="<i>🔐 Join Channel To Use Me 🔐</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔓 Join Now 🔓", url=f"https://t.me/{UPDATES_CHANNEL}")
                            ]
                        ]
                    ),

                )
                 return
            except Exception:
                await app.send_message(
                    chat_id=message.chat.id,
                    text=f"<i>Something went wrong</i> <b> <a href='https://telegram.me/{OWNER_USERNAME}'>CLICK HERE FOR SUPPORT </a></b>",

                    disable_web_page_preview=True)
                return
    await app.send_message(message.chat.id, f"__👋 Hi **{message.from_user.mention}**, i am Link Bypasser Bot, just send me any supported links and i will you get you results.\nCheckout /help to Read More__",
                           reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("🌐 Source Code 🌐", url="https://github.com/bipinkrish/Link-Bypasser-Bot")]]), reply_to_message_id=message.id)


# help command
@app.on_message(filters.command(["help"]))
async def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if str(message.chat.id).startswith("-100") and message.chat.id not in GROUP_ID:
        return
    elif message.chat.id not in GROUP_ID:
            try:
                user = await app.get_chat_member(UPDATES_CHANNEL, message.chat.id)
                if user.status == enums.ChatMemberStatus.BANNED:
                    await app.send_message(
                        chat_id=message.chat.id,
                        text=f"__Sorry, you are banned. Contact My [ Owner ](https://telegram.me/{OWNER_USERNAME})__",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                 await app.send_message(
                    chat_id=message.chat.id,
                    text="<i>🔐 Join Channel To Use Me 🔐</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔓 Join Now 🔓", url=f"https://t.me/{UPDATES_CHANNEL}")
                            ]
                        ]
                    ),

                )
                 return
            except Exception:
                await app.send_message(
                    chat_id=message.chat.id,
                    text=f"<i>Something went wrong</i> <b> <a href='https://telegram.me/{OWNER_USERNAME}'>CLICK HERE FOR SUPPORT </a></b>",

                    disable_web_page_preview=True)
                return
    await app.send_message(message.chat.id, HELP_TEXT, reply_to_message_id=message.id, disable_web_page_preview=True)

@app.on_message(filters.command(["authorize"]))
async def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.chat.id in ADMIN_LIST or message.from_user.id in ADMIN_LIST :
        try :
            msg = int(message.text.split()[-1])
        except ValueError:
            await app.send_message(message.chat.id, f"Example\n<code>/authorize -100</code>", reply_to_message_id=message.id, disable_web_page_preview=True)
            return
        if msg in GROUP_ID:
            await app.send_message(message.chat.id, f"Already Added", reply_to_message_id=message.id, disable_web_page_preview=True)
        else :
            GROUP_ID.append(msg)
            await app.send_message(message.chat.id, f"Authorized Temporarily!", reply_to_message_id=message.id, disable_web_page_preview=True)
    else:
        await app.send_message(message.chat.id, f"This Command Is Only For Admins", reply_to_message_id=message.id, disable_web_page_preview=True)

@app.on_message(filters.command(["unauthorize"]))
async def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.chat.id in ADMIN_LIST or message.from_user.id in ADMIN_LIST :
        try :
            msg = int(message.text.split()[-1])
        except ValueError:
            await app.send_message(message.chat.id, f"Example\n<code>/unauthorize -100</code>", reply_to_message_id=message.id, disable_web_page_preview=True)
            return
        if msg not in GROUP_ID:
            await app.send_message(message.chat.id, f"Already Removed", reply_to_message_id=message.id, disable_web_page_preview=True)
        else :
            if msg == int(PERMANENT_GROUP) :
                await app.send_message(message.chat.id, f"Even Owner Can't Remove This {msg} Chat 😂😂", reply_to_message_id=message.id, disable_web_page_preview=True)
                return
            GROUP_ID.remove(msg)
            await app.send_message(message.chat.id, f"Unauthorized!", reply_to_message_id=message.id, disable_web_page_preview=True)
    else:
        await app.send_message(message.chat.id, f"This Command Is Only For Admins", reply_to_message_id=message.id, disable_web_page_preview=True)

@app.on_message(filters.command(["addsudo"]))
async def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.chat.id == int(OWNER_ID) or message.from_user.id == int(OWNER_ID) :
        try :
            msg = int(message.text.split()[-1])
        except ValueError:
            await app.send_message(message.chat.id, f"Example\n<code>/addsudo 123</code>", reply_to_message_id=message.id, disable_web_page_preview=True)
            return
        if msg in ADMIN_LIST:
            await app.send_message(message.chat.id, f"Already Admin", reply_to_message_id=message.id, disable_web_page_preview=True)
        else :
            ADMIN_LIST.append(msg)
            await app.send_message(message.chat.id, f"Promoted As Admin Temporarily", reply_to_message_id=message.id, disable_web_page_preview=True)
    else:
        await app.send_message(message.chat.id, f"This Command Is Only For Owner", reply_to_message_id=message.id, disable_web_page_preview=True)
        
@app.on_message(filters.command(["remsudo"]))
async def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.chat.id == int(OWNER_ID) or message.from_user.id == int(OWNER_ID) :
        try :
            msg = int(message.text.split()[-1])
        except ValueError:
            await app.send_message(message.chat.id, f"Example\n<code>/remsudo 123</code>", reply_to_message_id=message.id, disable_web_page_preview=True)
            return
        if msg not in ADMIN_LIST:
            await app.send_message(message.chat.id, f"Already Demoted!", reply_to_message_id=message.id, disable_web_page_preview=True)
        else :
            if msg == int(message.from_user.id) :
                await app.send_message(message.chat.id, f"You Can't Remove Yourself 😂😂", reply_to_message_id=message.id, disable_web_page_preview=True)
                return
            elif msg == int(OWNER_ID) :
                await app.send_message(message.chat.id, f"Even Owner Can't Remove Himself 😂😂", reply_to_message_id=message.id, disable_web_page_preview=True)
                return
            ADMIN_LIST.remove(msg)
            await app.send_message(message.chat.id, f"Demoted!", reply_to_message_id=message.id, disable_web_page_preview=True)
    else:
        await app.send_message(message.chat.id, f"This Command Is Only For Owner", reply_to_message_id=message.id, disable_web_page_preview=True)
        
@app.on_message(filters.command(["users"]))
async def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.chat.id in ADMIN_LIST or message.from_user.id in ADMIN_LIST :
        lol = "List Of Authorized Chats\n\n"
        for i in GROUP_ID:
            lol += "<code>" + str(i) + "</code>\n"
        lol += "\nList Of Admin ID's\n\n"
        for i in ADMIN_LIST:
            lol += "<code>" + str(i) + "</code>\n"
        await app.send_message(message.chat.id, lol, reply_to_message_id=message.id, disable_web_page_preview=True)
    else :
        await app.send_message(message.chat.id, f"This Command Is Only For Admins", reply_to_message_id=message.id, disable_web_page_preview=True)

# links
@app.on_message(filters.text)
async def receive(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if str(message.chat.id).startswith("-100") and message.chat.id not in GROUP_ID:
        return
    elif message.chat.id not in GROUP_ID:
        if UPDATES_CHANNEL != "None":
            try:
                user = await app.get_chat_member(UPDATES_CHANNEL, message.chat.id)
                if user.status == enums.ChatMemberStatus.BANNED:
                    await app.send_message(
                        chat_id=message.chat.id,
                        text=f"__Sorry, you are banned. Contact My [ Owner ](https://telegram.me/{OWNER_USERNAME})__",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                 await app.send_message(
                    chat_id=message.chat.id,
                    text="<i>🔐 Join Channel To Use Me 🔐</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔓 Join Now 🔓", url=f"https://t.me/{UPDATES_CHANNEL}")
                            ]
                        ]
                    ),

                )
                 return
            except Exception:
                await app.send_message(
                    chat_id=message.chat.id,
                    text=f"<i>Something went wrong</i> <b> <a href='https://telegram.me/{OWNER_USERNAME}'>CLICK HERE FOR SUPPORT </a></b>",

                    disable_web_page_preview=True)
                return
    bypass = threading.Thread(target=lambda:loopthread(message),daemon=True)
    bypass.start()


# doc thread
def docthread(message):
    if message.document.file_name.endswith("dlc"):
        msg = app.send_message(message.chat.id, "🔎 __bypassing...__", reply_to_message_id=message.id)
        print("sent DLC file")
        sess = requests.session()
        file = app.download_media(message)
        dlccont = open(file,"r").read()
        link = bypasser.getlinks(dlccont,sess)
        app.edit_message_text(message.chat.id, msg.id, f'__{link}__')
        os.remove(file)

@app.on_message(filters.document)
async def docfile(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if str(message.chat.id).startswith("-100") and message.chat.id not in GROUP_ID:
        return
    elif message.chat.id not in GROUP_ID:
        if UPDATES_CHANNEL != "None":
            try:
                user = await app.get_chat_member(UPDATES_CHANNEL, message.chat.id)
                if user.status == enums.ChatMemberStatus.BANNED:
                    await app.send_message(
                        chat_id=message.chat.id,
                        text=f"__Sorry, you are banned. Contact My [ Owner ](https://telegram.me/{OWNER_USERNAME})__",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                 await app.send_message(
                    chat_id=message.chat.id,
                    text="<i>🔐 Join Channel To Use Me 🔐</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔓 Join Now 🔓", url=f"https://t.me/{UPDATES_CHANNEL}")
                            ]
                        ]
                    ),

                )
                 return
            except Exception:
                await app.send_message(
                    chat_id=message.chat.id,
                    text=f"<i>Something went wrong</i> <b> <a href='https://telegram.me/{OWNER_USERNAME}'>CLICK HERE FOR SUPPORT </a></b>",

                    disable_web_page_preview=True)
                return
    if message.document.file_name.endswith(".dlc"):
        bypass = threading.Thread(target=lambda:docthread(message),daemon=True)
        bypass.start()

# server loop
print("Bot Starting")
app.run()
