import telebot
import bypasser
import os

# bot
TOKEN = os.environ.get("TOKEN", "")
bot = telebot.TeleBot(TOKEN)


# start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Available Sites \n /af - Adfly \n /gp - gplinks \n /dl - droplink \n /lv - linkvertise \n /md - mdisk \n /rl - rocklinks \n /pd - pixeldrain \n /wt - wetransfer \n /mu - megaup \n /gd - Drive Look-Alike (/gdlist) \n /ot - others (/otlist) \n /ou - ouo")


# adfly short url
@bot.message_handler(commands=['af'])
def af(message):
    url = message.text.split("/af ")[1]
    print("You Have Entered adfly:",url)
    msg = bot.reply_to(message, "bypassing...")
    try:
        out = bypasser.adfly(url)
        link = out['bypassed_url']
        bot.edit_message_text(link, msg.chat.id, msg.id)
    except:
        bot.edit_message_text("Failed to Bypass", msg.chat.id, msg.id)

# gplinks short url
@bot.message_handler(commands=['gp'])
def gp(message):
    url = message.text.split("/gp ")[1]
    print("Entered Link gplink:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.gplinks(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# droplink url
@bot.message_handler(commands=['dl'])
def dp(message):
    url = message.text.split("/dl ")[1]
    print("You Have Entered droplink:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.droplink(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)
   

# linkvertise short url
@bot.message_handler(commands=['lv'])
def lv(message):
    url = message.text.split("/lv ")[1]
    print("You Have Entered linkvertise:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.linkvertise(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# mdisk link
@bot.message_handler(commands=['md'])
def md(message):
    url = message.text.split("/md ")[1]
    print("You Have Entered mdisk:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.mdisk(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# rocklinks link
@bot.message_handler(commands=['rl'])
def rl(message):
    url = message.text.split("/rl ")[1]
    print("You Have Entered rocklinks:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.rocklinks(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# pixeldrain link
@bot.message_handler(commands=['pd'])
def pd(message):
    url = message.text.split("/pd ")[1]
    print("You Have Entered pixeldrain:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.pixeldrain(url)
    bot.edit_message_text(link, msg.chat.id, msg.id) 
   

# wetransfer link
@bot.message_handler(commands=['wt'])
def wt(message):
    url = message.text.split("/wt ")[1]
    print("You Have Entered wetransfer:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.wetransfer(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)   


# megaup link
@bot.message_handler(commands=['mu'])
def mu(message):
    url = message.text.split("/mu ")[1]
    print("You Have Entered megaup:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.megaup(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# ouo
@bot.message_handler(commands=['ou'])
def ou(message):
    url = message.text.split("/ou ")[1]
    print("You Have Entered ouo:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.ouo(url)
    bot.edit_message_text(link, msg.chat.id, msg.id) 


# gd lokk a like
@bot.message_handler(commands=['gd'])
def gd(message):
    url = message.text.split("/gd ")[1]
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
    url = message.text.split("/ot ")[1]
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
