import telebot
import bypasser
import os


# bot
TOKEN = os.environ.get("TOKEN", "")
if TOKEN == "":
    print("TOKEN is Required to start the Bot")
    exit()
bot = telebot.TeleBot(TOKEN)    
GDTot_Crypt = os.environ.get("CRYPT","b0lDek5LSCt6ZjVRR2EwZnY4T1EvVndqeDRtbCtTWmMwcGNuKy8wYWpDaz0%3D")
Laravel_Session = os.environ.get("Laravel_Session","")
XSRF_TOKEN = os.environ.get("XSRF_TOKEN","")
KCRYPT = os.environ.get("KOLOP_CRYPT","")
DCRYPT = os.environ.get("DRIVEFIRE_CRYPT","")
HCRYPT = os.environ.get("HUBDRIVE_CRYPT","")
KATCRYPT = os.environ.get("KATDRIVE_CRYPT","")


# start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🔗 *Available Sites* \n\n  \
 `/af` - _adfly_ \n  \
 `/gp` - _gplinks_ \n  \
 `/dl` - _droplink_ \n  \
 `/lv` - _linkvertise_ \n  \
 `/md` - _mdisk_ \n  \
 `/rl` - _rocklinks_ \n  \
 `/pd` - _pixeldrain_ \n  \
 `/wt` - _wetransfer_ \n  \
 `/mu` - _megaup_ \n  \
 `/gd` - _gdrive look-alike (/gdlist)_ \n  \
 `/ot` - _others (/otlist)_ \n  \
 `/ou` - _ouo_ \n  \
 `/gt` - _gdtot_ \n  \
 `/sh` - _sharer_ \n  \
 `/ps` - _psa_ \n  \
 `/go` - _gofile_ \n  \
 `/st` - _shorte_ \n  \
 `/pi` - _pixl_ \n  \
 `/an` - _anonfiles_ \n  \
 `/gy` - _gyanilinks_ \n  \
 `/sg` - _shortingly_ \n  \
 `/su` - _shareus_ \n  \
 `/db` - _dropbox_ \n  \
 `/fc` - _filecrypt_ \n  \
 `/zs` - _zippyshare_ \n  \
 `/mf` - _mediafire_ \n  \
 `/ko` - _kolop_ \n  \
 `/df` - _drivefire_ \n  \
 `/hd` - _hubdrive_ \n  \
 `/kd` - _katdrive_ \n\n\
_reply to the link with command or use format /xx link_",
parse_mode="Markdown")


# katdrive
@bot.message_handler(commands=['kd'])
def kd(message):
    if KATCRYPT == "":
        bot.reply_to(message, "🚫 _You can't use this because_ *KATDRIVE_CRYPT* _ENV is not set_", parse_mode="Markdown")
        return

    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/kd ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("Entered Link katdrive:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.katdrive_dl(url, KATCRYPT)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# hubdrive
@bot.message_handler(commands=['hd'])
def hd(message):
    if HCRYPT == "":
        bot.reply_to(message, "🚫 _You can't use this because_ *HUBDRIVE_CRYPT* _ENV is not set_", parse_mode="Markdown")
        return

    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/hd ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("Entered Link hubdrive:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.hubdrive_dl(url, HCRYPT)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# drivefire
@bot.message_handler(commands=['df'])
def df(message):
    if DCRYPT == "":
        bot.reply_to(message, "🚫 _You can't use this because_ *DRIVEFIRE_CRYPT* _ENV is not set_", parse_mode="Markdown")
        return

    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/df ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("Entered Link drivefire:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.drivefire_dl(url, DCRYPT)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# kolop
@bot.message_handler(commands=['ko'])
def ko(message):
    if KCRYPT == "":
        bot.reply_to(message, "🚫 _You can't use this because_ *KOLOP_CRYPT* _ENV is not set_", parse_mode="Markdown")
        return

    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/ko ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("Entered Link kolop:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.kolop_dl(url, KCRYPT)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# mediafire
@bot.message_handler(commands=['mf'])
def mf(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/mf ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered mediafire:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.mediafire(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# zippyshare
@bot.message_handler(commands=['zs'])
def zs(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/zs ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered zippyshare:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.zippyshare(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# filecrypt
@bot.message_handler(commands=['fc'])
def fc(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/fc ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered filecrypt:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.filecrypt(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# dropbox
@bot.message_handler(commands=['db'])
def db(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/db ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered dropbox:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.dropbox(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# shareus
@bot.message_handler(commands=['su'])
def su(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/su ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered shareus:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.shareus(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# shortingly
@bot.message_handler(commands=['sg'])
def sg(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/sg ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered shortingly:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.shortlingly(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# gyanilinks
@bot.message_handler(commands=['gy'])
def gy(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/gy ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered gyanilinks:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.gyanilinks(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# anonfiles
@bot.message_handler(commands=['an'])
def an(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/an ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered anonfiles:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.anonfile(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# pixl
@bot.message_handler(commands=['pi'])
def pi(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/pi ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered pixl:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.pixl(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# shorte
@bot.message_handler(commands=['st'])
def st(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/st ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered shorte:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.sh_st_bypass(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# go file
@bot.message_handler(commands=['go'])
def go(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/go ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered gofile:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.gofile_dl(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# psa
@bot.message_handler(commands=['ps'])
def ps(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/ps ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered psa:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    links = bypasser.psa_bypasser(url)
    bot.edit_message_text(f'_{links}_', msg.chat.id, msg.id, parse_mode="Markdown")


# sharer pw
@bot.message_handler(commands=['sh'])
def sh(message):
    if XSRF_TOKEN == "" or Laravel_Session == "":
        bot.reply_to(message, "🚫 _You can't use this because_ *XSRF_TOKEN* _and_ *Laravel_Session* _ENV are not set_", parse_mode="Markdown")
        return

    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/sh ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("Entered Link sharer:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.sharer_pw(url, Laravel_Session, XSRF_TOKEN)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# gdtot url
@bot.message_handler(commands=['gt'])
def gt(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/gt ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("Entered Link gdtot:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.gdtot(url,GDTot_Crypt)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# adfly short url
@bot.message_handler(commands=['af'])
def af(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/af ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered adfly:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    out = bypasser.adfly(url)
    link = out['bypassed_url']
    try:    
        bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")
    except:
        bot.edit_message_text("_Failed to Bypass_", msg.chat.id, msg.id, parse_mode="Markdown")


# gplinks short url
@bot.message_handler(commands=['gp'])
def gp(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/gp ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("Entered Link gplink:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.gplinks(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# droplink url
@bot.message_handler(commands=['dl'])
def dp(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/dl ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered droplink:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.droplink(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")
   

# linkvertise short url
@bot.message_handler(commands=['lv'])
def lv(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/lv ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered linkvertise:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.linkvertise(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# mdisk link
@bot.message_handler(commands=['md'])
def md(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/md ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered mdisk:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.mdisk(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# rocklinks link
@bot.message_handler(commands=['rl'])
def rl(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/rl ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered rocklinks:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.rocklinks(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# pixeldrain link
@bot.message_handler(commands=['pd'])
def pd(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/pd ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered pixeldrain:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.pixeldrain(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown") 
   

# wetransfer link
@bot.message_handler(commands=['wt'])
def wt(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/wt ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered wetransfer:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.wetransfer(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")   


# megaup link
@bot.message_handler(commands=['mu'])
def mu(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/mu ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered megaup:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.megaup(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown")


# ouo
@bot.message_handler(commands=['ou'])
def ou(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/ou ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered ouo:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.ouo(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown") 


# gd lokk a like
@bot.message_handler(commands=['gd'])
def gd(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/gd ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered gdrive:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.unified(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown") 


# gd list
@bot.message_handler(commands=['gdlist'])
def gdlis(message):
    list = """_
- appdrive.in \n\
- driveapp.in \n\
- drivehub.in \n\
- gdflix.pro \n\
- drivesharer.in \n\
- drivebit.in \n\
- drivelinks.in \n\
- driveace.in \n\
- drivepro.in \n\
          _"""
    bot.reply_to(message, list, parse_mode="Markdown")       


# others
@bot.message_handler(commands=['ot'])
def ot(message):
    try:
        url = message.reply_to_message.text
    except:
        try:
            url = message.text.split("/ot ")[1]
        except:
            bot.reply_to(message, "⚠️ _Invalid format, either_ *reply* _to a_ *link* _or use_ */xx link*", parse_mode="Markdown")
            return
    print("You Have Entered others:",url)
    msg = bot.reply_to(message, "🔎 _bypassing..._", parse_mode="Markdown")
    link = bypasser.others(url)
    bot.edit_message_text(f'_{link}_', msg.chat.id, msg.id, parse_mode="Markdown") 


# others list
@bot.message_handler(commands=['otlist'])
def otlis(message):
    list="""_
- exe.io/exey.io \n\
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
    _"""
    bot.reply_to(message, list, parse_mode="Markdown")       


# server loop
print("bot started")
bot.infinity_polling()
