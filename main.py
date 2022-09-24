import telebot
import bypasser
import os

# bot
TOKEN = os.environ.get("TOKEN", "")
bot = telebot.TeleBot(TOKEN)
GDTot_Crypt = os.environ.get("CRYPT","b0lDek5LSCt6ZjVRR2EwZnY4T1EvVndqeDRtbCtTWmMwcGNuKy8wYWpDaz0%3D")
Laravel_Session = os.environ.get("Laravel_Session","")
XSRF_TOKEN = os.environ.get("XSRF_TOKEN","")


# start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Available Sites \n /af - Adfly \n /gp - gplinks \n /dl - droplink \n /lv - linkvertise \n \
/md - mdisk \n /rl - rocklinks \n /pd - pixeldrain \n /wt - wetransfer \n /mu - megaup \n /gd - Drive Look-Alike (/gdlist) \n \
/ot - others (/otlist) \n /ou - ouo \n /gt - gdtot \n /sh -  sharer \n /ps - psa \n /go - gofile \n /st - shorte \n \
/pi - pixl \n /an - anonfiles \n /gy - gyanilinks \n /sg - shortingly \n /su - shareus \n /db - dropbox \n /fc - filecrypt \n \
/zs - zippyshare \n /mf - mediafire")


# mediafire
@bot.message_handler(commands=['mf'])
def mf(message):
    try:
        url = message.text.split("/mf ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered mediafire:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.mediafire(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# zippyshare
@bot.message_handler(commands=['zs'])
def zs(message):
    try:
        url = message.text.split("/zs ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered zippyshare:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.zippyshare(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# filecrypt
@bot.message_handler(commands=['fc'])
def fc(message):
    try:
        url = message.text.split("/fc ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered filecrypt:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.filecrypt(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# dropbox
@bot.message_handler(commands=['db'])
def db(message):
    try:
        url = message.text.split("/db ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered dropbox:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.dropbox(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# shareus
@bot.message_handler(commands=['su'])
def su(message):
    try:
        url = message.text.split("/su ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered shareus:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.shareus(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# shortingly
@bot.message_handler(commands=['sg'])
def sg(message):
    try:
        url = message.text.split("/sg ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered shortingly:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.shortlingly(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# gyanilinks
@bot.message_handler(commands=['gy'])
def gy(message):
    try:
        url = message.text.split("/gy ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered gyanilinks:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.gyanilinks(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# anonfiles
@bot.message_handler(commands=['an'])
def an(message):
    try:
        url = message.text.split("/an ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered anonfiles:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.anonfile(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# pixl
@bot.message_handler(commands=['pi'])
def pi(message):
    try:
        url = message.text.split("/pi ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered pixl:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.pixl(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# shorte
@bot.message_handler(commands=['st'])
def st(message):
    try:
        url = message.text.split("/st ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered shorte:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.sh_st_bypass(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# go file
@bot.message_handler(commands=['go'])
def go(message):
    try:
        url = message.text.split("/go ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered gofile:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.gofile_dl(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# psa
@bot.message_handler(commands=['ps'])
def ps(message):
    try:
        url = message.text.split("/ps ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered psa:",url)
    msg = bot.reply_to(message, "bypassing...")
    links = bypasser.psa_bypasser(url)
    bot.edit_message_text(links, msg.chat.id, msg.id)


# sharer pw
@bot.message_handler(commands=['sh'])
def sh(message):
    if XSRF_TOKEN == "" or Laravel_Session == "":
        bot.reply_to(message, "You can't use this because XSRF_TOKEN and Laravel_Session ENV are not set")
        return

    try:
        url = message.text.split("/sh ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("Entered Link sharer:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.sharer_pw(url, Laravel_Session, XSRF_TOKEN)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# gdtot url
@bot.message_handler(commands=['gt'])
def gt(message):
    try:
        url = message.text.split("/gt ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("Entered Link gdtot:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.gdtot(url,GDTot_Crypt)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# adfly short url
@bot.message_handler(commands=['af'])
def af(message):
    try:
        url = message.text.split("/af ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered adfly:",url)
    msg = bot.reply_to(message, "bypassing...")
    out = bypasser.adfly(url)
    link = out['bypassed_url']
    try:    
        bot.edit_message_text(link, msg.chat.id, msg.id)
    except:
        bot.edit_message_text("Failed to Bypass", msg.chat.id, msg.id)


# gplinks short url
@bot.message_handler(commands=['gp'])
def gp(message):
    try:
        url = message.text.split("/gp ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("Entered Link gplink:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.gplinks(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# droplink url
@bot.message_handler(commands=['dl'])
def dp(message):
    try:
        url = message.text.split("/dl ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered droplink:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.droplink(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)
   

# linkvertise short url
@bot.message_handler(commands=['lv'])
def lv(message):
    try:
        url = message.text.split("/lv ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered linkvertise:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.linkvertise(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# mdisk link
@bot.message_handler(commands=['md'])
def md(message):
    try:
        url = message.text.split("/md ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered mdisk:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.mdisk(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# rocklinks link
@bot.message_handler(commands=['rl'])
def rl(message):
    try:
        url = message.text.split("/rl ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered rocklinks:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.rocklinks(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# pixeldrain link
@bot.message_handler(commands=['pd'])
def pd(message):
    try:
        url = message.text.split("/pd ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered pixeldrain:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.pixeldrain(url)
    bot.edit_message_text(link, msg.chat.id, msg.id) 
   

# wetransfer link
@bot.message_handler(commands=['wt'])
def wt(message):
    try:
        url = message.text.split("/wt ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered wetransfer:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.wetransfer(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)   


# megaup link
@bot.message_handler(commands=['mu'])
def mu(message):
    try:
        url = message.text.split("/mu ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered megaup:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.megaup(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# ouo
@bot.message_handler(commands=['ou'])
def ou(message):
    try:
        url = message.text.split("/ou ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered ouo:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.ouo(url)
    bot.edit_message_text(link, msg.chat.id, msg.id) 


# gd lokk a like
@bot.message_handler(commands=['gd'])
def gd(message):
    try:
        url = message.text.split("/gd ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered gdrive:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.unified(url)
    bot.edit_message_text(link, msg.chat.id, msg.id) 


# gd list
@bot.message_handler(commands=['gdlist'])
def gdlis(message):
    list = """
- appdrive.in \n\
- driveapp.in \n\
- drivehub.in \n\
- gdflix.pro \n\
- drivesharer.in \n\
- drivebit.in \n\
- drivelinks.in \n\
- driveace.in \n\
- drivepro.in \n\
          """
    bot.reply_to(message, list)       


# others
@bot.message_handler(commands=['ot'])
def ot(message):
    try:
        url = message.text.split("/ot ")[1]
    except:
        bot.reply_to(message, "Invalid format, /xx link")
        return
    print("You Have Entered others:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.others(url)
    bot.edit_message_text(link, msg.chat.id, msg.id) 


# others list
@bot.message_handler(commands=['otlist'])
def otlis(message):
    list="""
- exe.io/exey.io \n\
- sub2unlock.net/sub2unlock.com \n\
- rekonise.com \n\
- letsboost.net \n\
- ph.apps2app.com \n\
- mboost.me	\n\
- shortconnect.comb \n\
- sub4unlock.com \n\
- ytsubme.com \n\
- bit.ly \n\
- social-unlock.com	\n\
- boost.ink	\n\
- goo.gl \n\
- shrto.ml \n\
- t.co \n\
- tinyurl.com
    """
    bot.reply_to(message, list)       


# server loop
print("bot started")
bot.infinity_polling()
