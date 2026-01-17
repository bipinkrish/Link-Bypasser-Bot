#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tiny/Tinyfy bypasser
Bypasses tinyfy.in short URLs

Site: tinyfy.in
Method: Form submission with referrer from yotrickslog.tech
"""

try:
    import requests
    from bs4 import BeautifulSoup
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False

# Site configuration
SITE_NAME = "tiny"
URL_PATTERNS = [
    r'tinyfy\.in'
]

def process_url(url: str) -> str:
    """
    Bypass tinyfy.in URLs
    
    Args:
        url: tinyfy.in URL
        
    Returns:
        Bypassed URL or error message
    """
    if not SCRAPER_AVAILABLE:
        return "ERROR: requests and bs4 modules not available"
    
    try:
        client = requests.session()
        DOMAIN = "https://tinyfy.in"
        url = url[:-1] if url[-1] == "/" else url
        code = url.split("/")[-1]
        final_url = f"{DOMAIN}/{code}"
        ref = "https://www.yotrickslog.tech/"
        h = {"referer": ref}
        
        resp = client.get(final_url, headers=h)
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs}
        h = {"x-requested-with": "XMLHttpRequest"}
        
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
        try:
            return r.json()["url"]
        except:
            return "ERROR: Failed to extract URL from JSON response"
            
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
