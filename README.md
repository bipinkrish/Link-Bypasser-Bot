# Link-Bypasser-Bot

a Telegram Bot (with Site) that can Bypass Ad Links, Generate Direct Links and Jump Paywalls. see the Bot in Action [@BypassLinkBot](https://t.me/BypassLinkBot) or try it on [Replit](https://replit.com/@bipinkrish/Link-Bypasser#app.py)

---

## Required Variables

- `TOKEN` Bot Token from @BotFather
- `HASH` API Hash from my.telegram.org
- `ID` API ID from my.telegram.org

## Optional Variables 
you can also set these in `config.json` file

- `CRYPT` GDTot Crypt If you don't know how to get Crypt then [Learn Here](https://www.youtube.com/watch?v=EfZ29CotRSU)
- `XSRF_TOKEN` and `Laravel_Session` XSRF Token and Laravel Session cookies! If you don't know how to get then then watch [this Video](https://www.youtube.com/watch?v=EfZ29CotRSU) (for GDTOT) and do the same for sharer.pw
- `DRIVEFIRE_CRYPT` Drivefire Crypt
- `KOLOP_CRYPT`  Kolop Crypt!
- `HUBDRIVE_CRYPT` Hubdrive Crypt
- `KATDRIVE_CRYPT` Katdrive Crypt
- `UPTOBOX_TOKEN` Uptobox Token
- `TERA_COOKIE` Terabox Cookie (only `ndus` value) (see [Help](#help))
- `CLOUDFLARE` Use `cf_clearance` cookie from and Cloudflare protected sites
- `PORT` Port to run the Bot Site on (default is 5000)
---
## Deploy on Heroku
**BEFORE YOU DEPLOY ON HEROKU, YOU SHOULD FORK THE REPO AND CHANGE ITS NAME TO ANYTHING ELSE**<br>

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/bipinkrish/Link-Bypasser-Bot)</br>

## Commands

```
/start - Welcome Message
/help - List of All Supported Sites

```

---
## Supported Sites
To see the list of supported sites see [texts.py](https://github.com/bipinkrish/Link-Bypasser-Bot/blob/main/texts.py) file
---
## Help
* If you are deploying on VPS, watch videos on how to set/export Environment Variables. OR you can set these in `config.json` file
* Terabox Cookie

    1. Open any Browser
    2. Make sure you are logged in with a Terbox account
    3. Press `f12` to open DEV tools and click Network tab
    4. Open any Terbox video link and open Cookies tab
    5. Copy value of `ndus`
   
   <br>

   ![](https://i.ibb.co/hHBZM5m/Screenshot-113.png)
