import re
import requests
from base64 import b64decode
from urllib.parse import unquote
import time
import requests
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import time
import json
import base64
import requests
import telebot

bot = telebot.TeleBot(
    "YOUR BOT TOKEN", parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Available Sites \n /af - Adfly \n /gp - gplinks \n /dl - droplink \n /lv - linkvertise ")


# adfly short url
@bot.message_handler(commands=['af'])
def af(message):

    def adfly_bypass(url):
        res = requests.get(url).text

        out = {'error': False, 'src_url': url}

        try:
            ysmm = re.findall("ysmm\s+=\s+['|\"](.*?)['|\"]", res)[0]
        except:
            out['error'] = True
            return out

        url = decrypt_url(ysmm)

        if re.search(r'go\.php\?u\=', url):
            url = b64decode(re.sub(r'(.*?)u=', '', url)).decode()
        elif '&dest=' in url:
            url = unquote(re.sub(r'(.*?)dest=', '', url))

        out['bypassed_url'] = url

        return out

    def decrypt_url(code):
        a, b = '', ''
        for i in range(0, len(code)):
            if i % 2 == 0:
                a += code[i]
            else:
                b = code[i] + b

        key = list(a + b)
        i = 0

        while i < len(key):
            if key[i].isdigit():
                for j in range(i+1, len(key)):
                    if key[j].isdigit():
                        u = int(key[i]) ^ int(key[j])
                        if u < 10:
                            key[i] = str(u)
                        i = j
                        break
            i += 1

        key = ''.join(key)
        decrypted = b64decode(key)[16:-16]

        return decrypted.decode('utf-8')

    URL = message.text.split("/af ")[1]

    print("You Have Entered:")
    print(URL)

    print("Checking Link...")

    print("Bypassing Link...")

    out = adfly_bypass(URL)
    print(out['bypassed_url'])
    bot.reply_to(message, out['bypassed_url'])

# gplinks short url
@bot.message_handler(commands=['gp'])
def gp(message):

    url = message.text.split("/gp ")[1]
    print("Entered Link:")
    print(url)
    print("Checking Link...")
    print("Checking Done!")

    print("Bypassing the Link...")

    def gplinks_bypass(url):
        scraper = cloudscraper.create_scraper(allow_brotli=False)
        res = scraper.get(url)

        h = {"referer": res.url}
        res = scraper.get(url, headers=h)

        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.find_all('input')
        data = {input.get('name'): input.get('value') for input in inputs}

        h = {
            'content-type': 'application/x-www-form-urlencoded',
            'x-requested-with': 'XMLHttpRequest'
        }

        time.sleep(10)  # !important

        p = urlparse(url)
        final_url = f'{p.scheme}://{p.netloc}/links/go'
        res = scraper.post(final_url, data=data, headers=h).json()

        return res
    bot.reply_to(message, gplinks_bypass(url)["url"])

# droplink url
@bot.message_handler(commands=['dl'])
def af(message):
    url = message.text.split("/dl ")[1]
    print("You Have Entered:")
    print(url)
    print("Checking Link!")
    
    print("Bypassing Link...")
    def droplink_bypass(url):
        client = requests.Session()
        res = client.get(url)

        ref = re.findall("action[ ]{0,}=[ ]{0,}['|\"](.*?)['|\"]", res.text)[0]

        h = {'referer': ref}
        res = client.get(url, headers=h)

        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.find_all('input')
        data = { input.get('name'): input.get('value') for input in inputs }

        h = {
            'content-type': 'application/x-www-form-urlencoded',
            'x-requested-with': 'XMLHttpRequest'
        }
        p = urlparse(url)
        final_url = f'{p.scheme}://{p.netloc}/links/go'

        time.sleep(3.1)
        res = client.post(final_url, data=data, headers=h).json()

        return res
    bot.reply_to(message, droplink_bypass(url)["url"])

# linkvertise short url
@bot.message_handler(commands=['lv'])
def af(message):
    def lv_bypass(url):
        client = requests.Session()
        
        headers = {
            "User-Agent": "AppleTV6,2/11.1",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        client.headers.update(headers)
        
        url = url.replace("%3D", " ").replace("&o=sharing", "").replace("?o=sharing", "").replace("dynamic?r=", "dynamic/?r=")
        
        id_name = re.search(r"\/\d+\/[^\/]+", url)
        
        if not id_name: return None
        
        paths = [
            "/captcha", 
            "/countdown_impression?trafficOrigin=network", 
            "/todo_impression?mobile=true&trafficOrigin=network"
        ]
        
        for path in paths:
            url = f"https://publisher.linkvertise.com/api/v1/redirect/link{id_name[0]}{path}"
            response = client.get(url).json()
            if response["success"]: break
        
        data = client.get(f"https://publisher.linkvertise.com/api/v1/redirect/link/static{id_name[0]}").json()

        out = {
            'timestamp':int(str(time.time_ns())[0:13]),
            'random':"6548307", 
            'link_id':data["data"]["link"]["id"]
        }
        
        options = {
            'serial': base64.b64encode(json.dumps(out).encode()).decode()
        }
        
        data = client.get("https://publisher.linkvertise.com/api/v1/account").json()
        user_token = data["user_token"] if "user_token" in data.keys() else None
        
        url_submit = f"https://publisher.linkvertise.com/api/v1/redirect/link{id_name[0]}/target?X-Linkvertise-UT={user_token}"
        
        data = client.post(url_submit, json=options).json()
        
        return data["data"]["target"]

    
    url = message.text.split("/lv ")[1]
    bot.reply_to(message, lv_bypass(url))


print("server started")
bot.infinity_polling()
