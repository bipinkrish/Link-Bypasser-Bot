"""
Earnl bypasser
"""

import time
import requests
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "Earnl"
URL_PATTERNS = [
    r'earnl\.xyz/',
    r'v\.earnl\.xyz/'
]

def earnl_bypass(url):
    """
    Bypass Earnl short links
    """
    try:
        client = requests.session()
        DOMAIN = "https://v.earnl.xyz"
        url = url[:-1] if url[-1] == "/" else url
        code = url.split("/")[-1]
        final_url = f"{DOMAIN}/{code}"
        ref = "https://link.modmakers.xyz/"
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
            return "Something went wrong with Earnl bypass"

    except Exception as e:
        return f"Error bypassing Earnl: {str(e)}"

# Common export function name
process_url = earnl_bypass
