#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bluemediafiles bypasser
Extracts direct download links from bluemediafiles.com

Site: bluemediafiles.com
Method: Script parsing and key decoding
"""

try:
    import requests
    from bs4 import BeautifulSoup
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False

# Site configuration
SITE_NAME = "bluemediafiles"
URL_PATTERNS = [
    r'bluemediafiles\.com'
]

def decode_key(encoded):
    """Decode the encoded key from bluemediafiles script"""
    key = ""

    i = len(encoded) // 2 - 5
    while i >= 0:
        key += encoded[i]
        i = i - 2

    i = len(encoded) // 2 + 4
    while i < len(encoded):
        key += encoded[i]
        i = i + 2

    return key

def process_url(url: str, torrent=False) -> str:
    """
    Bypass bluemediafiles.com URLs
    
    Args:
        url: bluemediafiles.com URL
        torrent: Whether to use torrent extraction path
        
    Returns:
        Direct download URL or error message
    """
    if not SCRAPER_AVAILABLE:
        return "ERROR: requests and bs4 modules not available"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Alt-Used": "bluemediafiles.com",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
        }

        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        script = str(soup.findAll("script")[3])
        encoded_key = script.split('Create_Button("')[1].split('");')[0]

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": url,
            "Alt-Used": "bluemediafiles.com",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
        }

        params = {"url": decode_key(encoded_key)}

        if torrent:
            res = requests.get(
                "https://dl.pcgamestorrents.org/get-url.php", params=params, headers=headers
            )
            soup = BeautifulSoup(res.text, "html.parser")
            furl = soup.find("a", class_="button").get("href")
        else:
            res = requests.get(
                "https://bluemediafiles.com/get-url.php", params=params, headers=headers
            )
            furl = res.url
            if "mega.nz" in furl:
                furl = furl.replace("mega.nz/%23!", "mega.nz/file/").replace("!", "#")

        return furl
        
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
