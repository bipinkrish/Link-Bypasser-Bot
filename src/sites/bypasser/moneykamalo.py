"""
MoneyKamalo bypasser
"""

import time
import requests
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "MoneyKamalo"
URL_PATTERNS = [
    r'go\.moneykamalo\.com/',
    r'moneykamalo\.com/'
]

def moneykamalo_bypass(url):
    """
    Bypass MoneyKamalo short links
    """
    try:
        client = requests.session()
        DOMAIN = "https://go.moneykamalo.com"
        url = url[:-1] if url[-1] == "/" else url
        code = url.split("/")[-1]
        final_url = f"{DOMAIN}/{code}"
        ref = "https://bloging.techkeshri.com/"
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
            return "Something went wrong with MoneyKamalo bypass"

    except Exception as e:
        return f"Error bypassing MoneyKamalo: {str(e)}"

# Common export function name
process_url = moneykamalo_bypass
