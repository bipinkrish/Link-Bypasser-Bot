"""
Filecrypt bypasser
"""

import requests
import cloudscraper
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "Filecrypt"
URL_PATTERNS = [
    r'filecrypt\.co/',
    r'filecrypt\.cc/'
]

def getlinks(dlc):
    """
    Extract links from DLC content using dcrypt.it
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
            "Accept": "application/json, text/javascript, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "http://dcrypt.it",
            "Connection": "keep-alive",
            "Referer": "http://dcrypt.it/",
        }

        data = {
            "content": dlc,
        }

        response = requests.post(
            "http://dcrypt.it/decrypt/paste", headers=headers, data=data
        ).json()["success"]["links"]
        
        links = ""
        for link in response:
            links = links + link + "\n\n"
        return links[:-1] if links else "No links found"
    except:
        return "Error extracting links from DLC"

def filecrypt_bypass(url):
    """
    Bypass Filecrypt links and extract DLC content
    """
    try:
        client = cloudscraper.create_scraper(allow_brotli=False)
        headers = {
            "authority": "filecrypt.co",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://filecrypt.co",
            "referer": url,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        }

        resp = client.get(url, headers=headers)
        soup = BeautifulSoup(resp.content, "html.parser")

        # Find the DLC download button
        buttons = soup.find_all("button")
        dlclink = None
        
        for ele in buttons:
            onclick = ele.get("onclick")
            if onclick and "DownloadDLC" in onclick:
                dlc_id = onclick.split("DownloadDLC('")[1].split("'")[0]
                dlclink = f"https://filecrypt.co/DLC/{dlc_id}.html"
                break

        if not dlclink:
            return "Error: Could not find DLC download link"

        resp = client.get(dlclink, headers=headers)
        return getlinks(resp.text)

    except Exception as e:
        return f"Error bypassing Filecrypt: {str(e)}"

# Common export function name
process_url = filecrypt_bypass
