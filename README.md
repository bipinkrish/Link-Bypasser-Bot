# Link-Bypasser-Bot

a Telegram Bot that can Bypass Ad Links and Generate Direct Links. see the Bot in Action [@BypassLinkBot](https://t.me/BypassLinkBot)

---

## Required Variables

- `TOKEN` Bot Token from @BotFather
- `HASH` API Hash from my.telegram.org
- `ID` API ID from my.telegram.org
- `OWNER_ID` Owner's User ID
- `OWNER_USERNAME` Username of Bot Owner Without "@"
- `PERMANENT_GROUP` Telegram New Or Old Group ID starts with -100, members of this group no need to join updates channel

## Optional Variables

- `CRYPT` GDTot Crypt If you don't know how to get Crypt then [Learn Here](https://www.youtube.com/watch?v=EfZ29CotRSU)
- `XSRF_TOKEN` and `Laravel_Session` XSRF Token and Laravel Session cookies! If you don't know how to get then then watch [this Video](https://www.youtube.com/watch?v=EfZ29CotRSU) (for GDTOT) and do the same for sharer.pw
- `DRIVEFIRE_CRYPT` Drivefire Crypt
- `KOLOP_CRYPT`  Kolop Crypt!
- `HUBDRIVE_CRYPT` Hubdrive Crypt
- `KATDRIVE_CRYPT` Katdrive Crypt
- `UPTOBOX_TOKEN` Uptobox Token
- `TERA_COOKIE` Terabox Cookie (only `ndus` value) (see [Help](#help))
- `UPDATES_CHANNEL` Updates channel username Without "@"
- `ADMIN_LIST` User ID's of Bot Admins seperatend by space
- `GROUP_ID` Telegram New Or Old Group ID's starts with -100 seperated by space, members of this group no need to join updates channel

---

## Commands

```
start - Welcome Message
help - List of All Supported Sites
addsudo - Add admins to Bot [Owner Command]
remsudo - Remove admins from Bot [Owner Command]
authorize - authorize Bot to the Group [Admin Command]
unauthorize - unauthorize Bot in that Group [Admin Command]
users - Authorized Group ID's and Admin ID's [Admin Command]
```

---

## Supported Sites

To see the list of supported sites see [texts.py](https://github.com/bipinkrish/Link-Bypasser-Bot/blob/main/texts.py) file

---

## Help

* If you are deploying on VPS, watch videos on how to set/export Environment Variables.

* Terabox Cookie

    1. Open any Browser
    2. Make sure you are logged in with a Terbox account
    3. Press `f12` to open DEV tools and click Network tab
    4. Open any Terbox video link and open Cookies tab
    5. Copy value of `ndus`
   
   <br>

   ![](https://i.ibb.co/hHBZM5m/Screenshot-113.png)
