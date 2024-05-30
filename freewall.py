import requests
import base64
import re
from bs4 import BeautifulSoup
from bypasser import RecaptchaV3

RTOKEN = RecaptchaV3()

#######################################################################


def getSoup(res):
    return BeautifulSoup(res.text, "html.parser")


def downloaderla(url, site):
    params = {
        "url": url,
        "token": RTOKEN,
    }
    return requests.get(site, params=params).json()


def getImg(url):
    return requests.get(url).content


def decrypt(res, key):
    if res["success"]:
        return base64.b64decode(res["result"].split(key)[-1]).decode("utf-8")


#######################################################################


def shutterstock(url):
    res = downloaderla(url, "https://ttthreads.net/shutterstock.php")
    if res["success"]:
        return res["result"]


def adobestock(url):
    res = downloaderla(url, "https://new.downloader.la/adobe.php")
    return decrypt(res, "#")


def alamy(url):
    res = downloaderla(url, "https://new.downloader.la/alamy.php")
    return decrypt(res, "#")


def getty(url):
    res = downloaderla(url, "https://getpaidstock.com/api.php")
    return decrypt(res, "#")


def picfair(url):
    res = downloaderla(url, "https://downloader.la/picf.php")
    return decrypt(res, "?newURL=")


def slideshare(url, type="pptx"):
    # enum = {"pdf","pptx","img"}
    # if type not in enum: type = "pdf"
    return requests.get(
        f"https://downloader.at/convert2{type}.php", params={"url": url}
    ).content


def medium(url):
    return requests.post(
        "https://downloader.la/read.php",
        data={
            "mediumlink": url,
        },
    ).content


#######################################################################


def pass_paywall(url, check=False, link=False):
    patterns = [
        (r"https?://(?:www\.)?shutterstock\.com/", shutterstock, True, "png", -1),
        (r"https?://stock\.adobe\.com/", adobestock, True, "png", -2),
        (r"https?://(?:www\.)?alamy\.com/", alamy, True, "png", -1),
        (r"https?://(?:www\.)?gettyimages\.", getty, True, "png", -2),
        (r"https?://(?:www\.)?istockphoto\.com", getty, True, "png", -1),
        (r"https?://(?:www\.)?picfair\.com/", picfair, True, "png", -1),
        (r"https?://(?:www\.)?slideshare\.net/", slideshare, False, "pptx", -1),
        (r"https?://medium\.com/", medium, False, "html", -1),
    ]

    img_link = None
    name = "no-name"
    for pattern, downloader_func, img, ftype, idx in patterns:
        if re.search(pattern, url):
            if check:
                return True
            img_link = downloader_func(url)

            try:
                name = url.split("/")[idx]
            except:
                pass
            if (not img) and img_link:
                fullname = name + "." + ftype
                with open(fullname, "wb") as f:
                    f.write(img_link)
                return fullname
            break

    if check:
        return False
    if link or (not img_link):
        return img_link
    fullname = name + "." + "png"
    with open(fullname, "wb") as f:
        f.write(getImg(img_link))
    return fullname


#######################################################################
