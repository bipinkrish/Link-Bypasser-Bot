"""
TNLink bypasser
"""

import requests
import time
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "TNLink"
URL_PATTERNS = [
    r'tnlink\.in/',
    r'page\.tnlink\.in/'
]

def tnlink_bypass(url):
    """
    Bypass TNLink URLs
    """
    try:
        client = requests.session()
        DOMAIN = "https://page.tnlink.in/"
        url = url[:-1] if url[-1] == "/" else url
        code = url.split("/")[-1]
        final_url = f"{DOMAIN}/{code}"
        ref = "https://usanewstoday.club/"
        h = {"referer": ref}
        
        while len(client.cookies) == 0:
            resp = client.get(final_url, headers=h)
            
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs}
        h = {"x-requested-with": "XMLHttpRequest"}
        time.sleep(8)
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
        
        try:
            return r.json()["url"]
        except:
            return f"Could not extract TNLink URL: {url}"
            
    except Exception as e:
        return f"Error bypassing TNLink: {str(e)}"

# Common export function name
process_url = tnlink_bypass
