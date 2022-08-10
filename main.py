import telebot
import bypasser
import os

# bot
TOKEN = os.environ.get("TOKEN", "")
bot = telebot.TeleBot(TOKEN)


# start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Available Sites \n /af - Adfly \n /gp - gplinks \n /dl - droplink \n /lv - linkvertise \n /md - mdisk \n /rl - rocklinks \n /pd - pixeldrain \n /wt - wetransfer \n /mu - megaup \n /gd - Drive Look-Alike (/gdlist)")


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
        bot.reply_to(message, "Failed to Bypass")

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
def af(message):
    url = message.text.split("/dl ")[1]
    print("You Have Entered droplink:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.droplink(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)
   

# linkvertise short url
@bot.message_handler(commands=['lv'])
def af(message):
    url = message.text.split("/lv ")[1]
    print("You Have Entered linkvertise:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.linkvertise(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# mdisk link
@bot.message_handler(commands=['md'])
def af(message):
    url = message.text.split("/md ")[1]
    print("You Have Entered mdisk:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.mdisk(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# rocklinks link
@bot.message_handler(commands=['rl'])
def af(message):
    url = message.text.split("/rl ")[1]
    print("You Have Entered rocklinks:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.rocklinks(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# pixeldrain link
@bot.message_handler(commands=['pd'])
def af(message):
    url = message.text.split("/pd ")[1]
    print("You Have Entered pixeldrain:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.pixeldrain(url)
    bot.edit_message_text(link, msg.chat.id, msg.id) 
   

# wetransfer link
@bot.message_handler(commands=['wt'])
def af(message):
    url = message.text.split("/wt ")[1]
    print("You Have Entered wetransfer:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.wetransfer(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)   


# megaup link
@bot.message_handler(commands=['mu'])
def af(message):
    url = message.text.split("/mu ")[1]
    print("You Have Entered megaup:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.megaup(url)
    bot.edit_message_text(link, msg.chat.id, msg.id)


# gd lokk a like
@bot.message_handler(commands=['gd'])
def af(message):
    url = message.text.split("/gd ")[1]
    print("You Have Entered gdrive:",url)
    msg = bot.reply_to(message, "bypassing...")
    link = bypasser.unified(url)
    bot.edit_message_text(link, msg.chat.id, msg.id) 


# gd list
@bot.message_handler(commands=['gdlist'])
def gdlis(message):
    list = """- appdrive.in
    - driveapp.in
    - drivehub.in
    - gdflix.pro
    - drivesharer.in
    - drivebit.in
    - drivelinks.in
    - driveace.in
    - drivepro.in
          """
    bot.reply_to(message, list)       


# server loop
print("server started")
bot.infinity_polling()
