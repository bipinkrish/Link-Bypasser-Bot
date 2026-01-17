"""
Lolshort bypasser
"""

import time
import requests
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "Lolshort"
URL_PATTERNS = [
    r'get\.lolshort\.tech/',
    r'lolshort\.tech/'
]

def lolshort_bypass(url):
    """
    Bypass Lolshort short links
    """
    try:
        client = requests.session()
        DOMAIN = "https://get.lolshort.tech/"
        url = url[:-1] if url[-1] == "/" else url
        code = url.split("/")[-1]
        final_url = f"{DOMAIN}/{code}"
        ref = "https://tech.animezia.com/"
        h = {"referer": ref}
        resp = client.get(final_url, headers=h)
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs}
        h = {"x-requested-with": "XMLHttpRequest"}
        time.sleep(5)
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
        
        try:
            return r.json()["url"]
        except:
            return "Something went wrong with Lolshort bypass"

    except Exception as e:
        return f"Error bypassing Lolshort: {str(e)}"

# Common export function name
process_url = lolshort_bypass
