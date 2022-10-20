import pyrogram
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import bypasser
import os
import ddl
import requests
import threading

# bot
bot_token = os.environ.get("TOKEN", "")
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "")
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)  

# ENVs
GDTot_Crypt = os.environ.get("CRYPT","b0lDek5LSCt6ZjVRR2EwZnY4T1EvVndqeDRtbCtTWmMwcGNuKy8wYWpDaz0%3D")
Laravel_Session = os.environ.get("Laravel_Session","")
XSRF_TOKEN = os.environ.get("XSRF_TOKEN","")
KCRYPT = os.environ.get("KOLOP_CRYPT","")
DCRYPT = os.environ.get("DRIVEFIRE_CRYPT","")
HCRYPT = os.environ.get("HUBDRIVE_CRYPT","")
KATCRYPT = os.environ.get("KATDRIVE_CRYPT","")


# main thread
def mainthread(cmd,url,message):

    # igg games
    if cmd == "/ig":
        print("entered igg:",url)
        link = bypasser.igggames(url)

    # ola movies
    if cmd == "/ol":
        print("entered ola movies:",url) 
        link = bypasser.olamovies(url)
        
    # script links
    elif cmd == "/sc":
        print("entered script link:",url)
        try:
            link = bypasser.getfirst(url)
        except:
            sess = requests.session()
            link = bypasser.getfinal(f'https://{url.split("/")[-2]}/',url, sess)
        
    # direct download link
    elif cmd == "/dl":
        print("entered ddl:",url)
        link = ddl.direct_link_generator(url)
        
    # katdrive
    elif cmd == "/kd":
        if KATCRYPT == "":
            app.send_message(message.chat.id, "🚫 __You can't use this because__ **KATDRIVE_CRYPT** __ENV is not set__", reply_to_message_id=message.id)
            return "0"
        
        print("entered katdrive:",url)
        link = bypasser.katdrive_dl(url, KATCRYPT)
        

    # hubdrive
    elif cmd == "/hd":
        if HCRYPT == "":
            app.send_message(message.chat.id, "🚫 __You can't use this because__ **HUBDRIVE_CRYPT** __ENV is not set__", reply_to_message_id=message.id)
            return "0"

        print("entered hubdrive:",url)
        link = bypasser.hubdrive_dl(url, HCRYPT)
        

    # drivefire
    elif cmd == "/df":
        if DCRYPT == "":
            app.send_message(message.chat.id, "🚫 __You can't use this because__ **DRIVEFIRE_CRYPT** __ENV is not set__", reply_to_message_id=message.id)
            return "0"

        print("entered drivefire:",url)
        link = bypasser.drivefire_dl(url, DCRYPT)
        

    # kolop
    elif cmd == "/ko":
        if KCRYPT == "":
            app.send_message(message.chat.id, "🚫 __You can't use this because__ **KOLOP_CRYPT** __ENV is not set__", reply_to_message_id=message.id)
            return "0"

        print("entered kolop:",url)
        link = bypasser.kolop_dl(url, KCRYPT)
        

    # filecrypt
    elif cmd == "/fc":
        print("entered filecrypt:",url)
        link = bypasser.filecrypt(url)
        

    # shareus
    elif cmd == "/su":
        print("entered shareus:",url)
        link = bypasser.shareus(url)
        

    # shortingly
    elif cmd == "/sg":
        print("entered shortingly:",url)
        link = bypasser.shortlingly(url)
        

    # gyanilinks
    elif cmd == "/gy":
        print("entered gyanilinks:",url)
        link = bypasser.gyanilinks(url)
        

    # pixl
    elif cmd == "/pi":
        print("entered pixl:",url)
        link = bypasser.pixl(url)
        

    # shorte
    elif cmd == "/st":
        print("entered shorte:",url)
        link = bypasser.sh_st_bypass(url)
        

    # psa
    elif cmd == "/ps":
        print("entered psa:",url)
        link = bypasser.psa_bypasser(url)
        

    # sharer pw
    elif cmd == "/sh":
        if XSRF_TOKEN == "" or Laravel_Session == "":
            app.send_message(message.chat.id, "🚫 __You can't use this because__ **XSRF_TOKEN** __and__ **Laravel_Session** __ENV is not set__", reply_to_message_id=message.id)
            return "0"

        print("entered sharer:",url)
        link = bypasser.sharer_pw(url, Laravel_Session, XSRF_TOKEN)
        

    # gdtot url
    elif cmd == "/gt":
        print("entered gdtot:",url)
        link = bypasser.gdtot(url,GDTot_Crypt)
        

    # adfly
    elif cmd == "/af":
        print("entered adfly:",url)
        out = bypasser.adfly(url)
        link = out['bypassed_url']
 
    # gplinks
    elif cmd == "/gp":
        print("entered gplink:",url)
        link = bypasser.gplinks(url)
        
    # droplink
    elif cmd == "/dp":
        print("entered droplink:",url)
        link = bypasser.droplink(url)
        
    # linkvertise
    elif cmd == "/lv":
        print("entered linkvertise:",url)
        link = bypasser.linkvertise(url)
        
    # rocklinks
    elif cmd == "/rl":
        print("entered rocklinks:",url)
        link = bypasser.rocklinks(url)
        
    # ouo
    elif cmd == "/ou":
        print("entered ouo:",url)
        link = bypasser.ouo(url)

    # gdrive look alike
    elif cmd == "/gd":
        print("entered gdrive:",url)
        link = bypasser.unified(url)

    # others
    elif cmd == "/ot":
        print("entered others:",url)
        link = bypasser.others(url)

    return link


# loop thread
def loopthread(cmd,message):
    try:
        url = str(message.reply_to_message.text)
    except:
        try:
            url = str(message.text.split(f"{cmd} ")[1])
        except:
            app.send_message(message.chat.id, f"⚠️ __Invalid format, either__ **reply** __to a__ **link** __or use like this ->__ **{cmd} link**", reply_to_message_id=message.id)
            return

    if cmd == "/dl":
        msg = app.send_message(message.chat.id, "⚡ __generating...__", reply_to_message_id=message.id)
    elif cmd in ["/ol","/ps"]:
        msg = app.send_message(message.chat.id, "🔎 __this might take some time...__", reply_to_message_id=message.id)
    else:
        msg = app.send_message(message.chat.id, "🔎 __bypassing...__", reply_to_message_id=message.id)

    link = ""
    for ele in url.split("\n"):
        temp = mainthread(cmd,ele,message)
        if temp != "0":
            print("bypassed:",temp)
            link = link + temp + "\n\n"
        else:
            return

    try:
        app.edit_message_text(message.chat.id, msg.id, f'__{link}__')
    except:
        app.edit_message_text(message.chat.id, msg.id, "__Failed to Bypass__")


# commands
AvailableCommands = ['ol','sc','dl','kd','hd','df','ko','fc','su','sg','gy','pi','st','ps','sh','gt','af','gp','dp','lv','rl','ou','gd','ot','ig']
@app.on_message(filters.command(AvailableCommands))
def receive(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    bypass = threading.Thread(target=lambda:loopthread(message.text.split(" ")[0],message),daemon=True)
    bypass.start()


# doc thread
def docthread(message):
    if message.document.file_name.endswith("dlc"):
        msg = app.send_message(message.chat.id, "🔎 __bypassing...__", reply_to_message_id=message.id)
        print("entered DLC file")
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


# start command
@app.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    app.send_message(message.chat.id, f"__👋 Hi **{message.from_user.mention}**, i am Link Bypasser Bot, just send me any supported links with proper format and i will you give you results. use /help to veiw supported sites list.__",
    reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("🌐 Source Code", url="https://github.com/bipinkrish/Link-Bypasser-Bot")]]), reply_to_message_id=message.id)


# help command
@app.on_message(filters.command(["help"]))
def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    app.send_message(message.chat.id, "🔗 **Available Sites** \n\n  \
 /dl - __direct download link (/ddllist)__ \n  \
 /af - __adfly__ \n  \
 /gp - __gplinks__ \n  \
 /dp - __droplink__ \n  \
 /lv - __linkvertise__ \n  \
 /rl - __rocklinks__ \n  \
 /gd - __gdrive look-alike (/gdlist)__ \n  \
 /ot - __others (/otlist)__ \n  \
 /ou - __ouo__ \n  \
 /gt - __gdtot__ \n  \
 /sh - __sharer__ \n  \
 /ps - __psa__ \n  \
 /st - __shorte__ \n  \
 /pi - __pixl__ \n  \
 /gy - __gyanilinks__ \n  \
 /sg - __shortingly__ \n  \
 /su - __shareus__ \n  \
 /fc - __filecrypt__ \n  \
 /ko - __kolop__ \n  \
 /df - __drivefire__ \n  \
 /hd - __hubdrive__ \n  \
 /kd - __katdrive__ \n  \
 /sc - __script links__ \n  \
 /ol - __olamovies__ \n  \
 /ig - __igg games__ \n\n\
__reply to the link with command or use format /xx link__",
reply_to_message_id=message.id)


# gd list
@app.on_message(filters.command(['gdlist']))
def gdlis(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    list = """__- appdrive.in \n\
- driveapp.in \n\
- drivehub.in \n\
- gdflix.pro \n\
- drivesharer.in \n\
- drivebit.in \n\
- drivelinks.in \n\
- driveace.in \n\
- drivepro.in \n\
          __"""
    app.send_message(message.chat.id, list, reply_to_message_id=message.id)


# others list
@app.on_message(filters.command(['otlist']))
def otlis(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    list="""__- exe.io/exey.io \n\
- sub2unlock.net/sub2unlock.com \n\
- rekonise.com \n\
- letsboost.net \n\
- ph.apps2app.com \n\
- mboost.me	\n\
- sub4unlock.com \n\
- ytsubme.com \n\
- bit.ly \n\
- social-unlock.com	\n\
- boost.ink	\n\
- goo.gl \n\
- shrto.ml \n\
- t.co \n\
- tinyurl.com
    __"""
    app.send_message(message.chat.id, list, reply_to_message_id=message.id)    


# ddl list
@app.on_message(filters.command(['ddllist']))
def ddllis(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    list="""__- disk.yandex.com \n\
- mediafire.com \n\
- uptobox.com \n\
- osdn.net \n\
- github.com \n\
- hxfile.co \n\
- anonfiles.com \n\
- letsupload.io \n\
- 1drv.ms(onedrive) \n\
- pixeldrain.com \n\
- antfiles.com \n\
- streamtape.com \n\
- bayfiles.com \n\
- racaty.net \n\
- 1fichier.com \n\
- solidfiles.com \n\
- krakenfiles.com \n\
- upload.ee \n\
- mdisk.me \n\
- wetransfer.com \n\
- gofile.io \n\
- dropbox.com \n\
- zippyshare.com \n\
- megaup.net \n\
- fembed.net, fembed.com, femax20.com, fcdn.stream, feurl.com, layarkacaxxi.icu, naniplay.nanime.in, naniplay.nanime.biz, naniplay.com, mm9842.com \n\
- sbembed.com, watchsb.com, streamsb.net, sbplay.org
    __"""
    app.send_message(message.chat.id, list, reply_to_message_id=message.id)     


# see help
@app.on_message(filters.text)
def short(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.text[0] == "/":
        app.send_message(message.chat.id, "__⏩ see /help__", reply_to_message_id=message.id)


# server loop
print("bot started")
app.run()
