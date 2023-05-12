import pyrogram
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton,CallbackQuery
import bypasser
import os
import ddl
import requests
import threading
from texts import HELP_TEXT, START_MSG, ABOUT_MSG
from ddl import ddllist
import re


# bot
bot_token = os.environ.get("TOKEN", "")
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "")
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
START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('UPDATE CHANNEL', url='https://telegram.me/technofoxYT'), 
            InlineKeyboardButton('YouTube CHANNEL', url='https://youtube.com/channel/UCngpKD7UkgXICp32m_h-RQQ')
        ], 
        [
            InlineKeyboardButton('💝 Donate Us For Keeping Our Service Free', callback_data='donate')
        ],
        
        [
            InlineKeyboardButton('⚙ HELP', callback_data='help'),
            InlineKeyboardButton('📕 ABOUT', callback_data='about'),
            InlineKeyboardButton('CLOSE ❌', callback_data='close')
        ]
    ]
)

HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('SUPPORT GROUP', url='https://telegram.me/webcoderhub'), 
            InlineKeyboardButton('DEVELOPER', url='https://t.me/OwnersContact_bot')
        ],
        [
            InlineKeyboardButton('🏠HOME', callback_data='home'),
            InlineKeyboardButton('📕 ABOUT', callback_data='about'), 
            InlineKeyboardButton('CLOSE ❌', callback_data='close')
        ]
    ]
)

ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('GITHUB', url='https://github.com/ScripterSaurav'), 
            InlineKeyboardButton('DEVELOPER', url='https://t.me/OwnersContact_bot')
        ],
        [
            InlineKeyboardButton('🏠 HOME', callback_data='home'),
            InlineKeyboardButton('⚙ HELP', callback_data='help'), 
            InlineKeyboardButton('CLOSE ❌', callback_data='close')
        ]
    ]
)

@app.on_callback_query() 
async def cb_handler(bot, update): 
    if update.data == "home": 
        await update.message.edit_text(
            text=START_MSG.format(update.from_user.mention), 
            reply_markup=START_BUTTONS, 
            disable_web_page_preview=True
        ) 
    elif update.data == "help": 
        await update.message.edit_text(
            text=HELP_TEXT, 
            reply_markup=HELP_BUTTONS, 
            disable_web_page_preview=True
        ) 
    elif update.data == "about": 
        await update.message.edit_text(
            text=ABOUT_MSG, 
            reply_markup=ABOUT_BUTTONS, 
            disable_web_page_preview=True
        ) 
    elif update.data == "donate": 
        await update.message.reply_photo("https://cdn.discordapp.com/attachments/772320931749953546/1096420532292964423/20230414_182207.jpg", caption=" ❓Do You Like This Bot & Want To Support It?\n\n You can help with server costs by donating to our wallet 😢 Use Above Qr Code Scanner For Donating Us. \n\n❤️Thank you.\n\n<b>Note:-</b> If You Face Any Problem Related Or While Donating Us Please Contact Us Here\n @OwnersContact_bot")
    else:
        await update.message.delete() 


@app.on_message(filters.private & filters.command(["start"])) 
async def start(bot, update): 
    await update.reply_text(
        text=START_MSG.format(update.from_user.mention),
        disable_web_page_preview=True, 
        reply_markup=START_BUTTONS)

@app.on_message(filters.private & filters.command(["help"])) 
async def help(bot, update): 
    await update.reply_text(
        text=HELP_TEXT, 
        disable_web_page_preview=True, 
        reply_markup=HELP_BUTTONS)

@app.on_message(filters.private & filters.command(["about"])) 
async def about(bot, update): 
    await update.reply_text(
        text=ABOUT_MSG, 
        disable_web_page_preview=True, 
        reply_markup=ABOUT_BUTTONS)

@app.on_message(filters.command(["donate"]) & filters.private) 
async def donate(bot, message): 
    await message.reply_photo("https://cdn.discordapp.com/attachments/772320931749953546/1096420532292964423/20230414_182207.jpg", caption=" ❓Do You Like This Bot & Want To Support It?\n\n You can help with server costs by donating to our wallet 😢 Use Above Qr Code Scanner For Donating Us. \n\n❤️Thank you.\n\n<b>Note:-</b> If You Face Any Problem Related Or While Donating Us Please Contact Us Here\n @OwnersContact_bot")

# links
@app.on_message(filters.text)
def receive(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
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


# doc
@app.on_message(filters.document)
def docfile(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    bypass = threading.Thread(target=lambda:docthread(message),daemon=True)
    bypass.start()


# server loop
print("Bot Starting")
app.run()
