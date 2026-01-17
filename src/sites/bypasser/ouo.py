"""
Ouo bypasser
"""

import re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from core.utils import RecaptchaV3

# Site configuration
SITE_NAME = "Ouo"
URL_PATTERNS = [
    r'ouo\.press/',
    r'ouo\.io/'
]

def ouo_bypass(url):
    """
    Bypass Ouo short links
    Code from https://github.com/xcscxr/ouo-bypass/
    """
    try:
        tempurl = url.replace("ouo.press", "ouo.io")
        p = urlparse(tempurl)
        id = tempurl.split("/")[-1]
        
        headers = {
            "authority": "ouo.io",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "referer": "http://www.google.com/ig/adde?moduleurl=",
            "upgrade-insecure-requests": "1",
        }
        
        client = requests.Session()
        client.headers.update(headers)
        
        res = client.get(tempurl)
        next_url = f"{p.scheme}://{p.hostname}/go/{id}"

        for _ in range(2):
            if res.headers.get("Location"):
                break
                
            bs4 = BeautifulSoup(res.content, "lxml")
            
            # Find the form inputs
            form = bs4.find("form")
            if not form:
                return "Error: No form found in Ouo page"
                
            inputs = form.findAll("input", {"name": re.compile(r"token$")})
            data = {input.get("name"): input.get("value") for input in inputs}
            data["x-token"] = RecaptchaV3()
            
            header = {"content-type": "application/x-www-form-urlencoded"}
            res = client.post(
                next_url,
                data=data,
                headers=header,
                allow_redirects=False,
            )
            next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}"

        return res.headers.get("Location", "Error: No redirect location found")

    except Exception as e:
        return f"Error bypassing Ouo: {str(e)}"

# Common export function name
process_url = ouo_bypass
