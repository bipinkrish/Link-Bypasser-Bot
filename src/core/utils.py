"""Base downloader functions for freewall sites"""

import requests
import base64
import re
from bs4 import BeautifulSoup

def getSoup(res):
    """Parse HTML response into BeautifulSoup object"""
    return BeautifulSoup(res.text, "html.parser")

def downloaderla(url, site):
    """Common downloader function for downloader.la based sites"""
    try:
        rtoken = RecaptchaV3()
    except:
        rtoken = "dummy_token"
    
    params = {
        "url": url,
        "token": rtoken,
    }
    return requests.get(site, params=params).json()

def getImg(url):
    """Download image content from URL"""
    return requests.get(url).content

def decrypt(res, key):
    """Decrypt base64 encoded result from API response"""
    if res["success"]:
        return base64.b64decode(res["result"].split(key)[-1]).decode("utf-8")
    else:
        raise Exception("API request failed")

def RecaptchaV3():
    """
    RECAPTCHA v3 BYPASS
    Code from https://github.com/xcscxr/Recaptcha-v3-bypass
    """
    try:
        ANCHOR_URL = "https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8ucHJlc3M6NDQz&hl=en&v=pCoGBhjs9s8EhFOHJFe8cqis&size=invisible&cb=ahgyd1gkfkhe"
        url_base = "https://www.google.com/recaptcha/"
        post_data = "v={}&reason=q&c={}&k={}&co={}"
        client = requests.Session()
        client.headers.update({"content-type": "application/x-www-form-urlencoded"})
        matches = re.findall("([api2|enterprise]+)\/anchor\?(.*)", ANCHOR_URL)[0]
        url_base += matches[0] + "/"
        params = matches[1]
        res = client.get(url_base + "anchor", params=params)
        token = re.findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
        params = dict(pair.split("=") for pair in params.split("&"))
        post_data = post_data.format(params["v"], token, params["k"], params["co"])
        res = client.post(url_base + "reload", params=f'k={params["k"]}', data=post_data)
        answer = re.findall(r'"rresp","(.*?)"', res.text)[0]
        return answer
    except:
        return "fallback_token"