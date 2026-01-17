#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mdiskshortners bypasser
Bypasses mdiskshortners.in short URLs

Site: mdiskshortners.in
Method: Form submission with 2-second delay
"""

import time
try:
    from cloudscraper import create_scraper
    from bs4 import BeautifulSoup
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False

# Site configuration
SITE_NAME = "mdiskshortners"
URL_PATTERNS = [
    r'mdiskshortners\.in'
]

def process_url(url: str) -> str:
    """
    Bypass mdiskshortners.in URLs
    
    Args:
        url: mdiskshortners.in URL
        
    Returns:
        Bypassed URL or error message
    """
    if not SCRAPER_AVAILABLE:
        return "ERROR: cloudscraper and bs4 modules not available"
    
    try:
        client = create_scraper(allow_brotli=False)
        DOMAIN = "https://mdiskshortners.in/"
        url = url[:-1] if url[-1] == "/" else url
        code = url.split("/")[-1]
        final_url = f"{DOMAIN}/{code}"
        ref = "https://www.adzz.in/"
        h = {"referer": ref}
        
        resp = client.get(final_url, headers=h)
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs}
        h = {"x-requested-with": "XMLHttpRequest"}
        
        time.sleep(2)
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
        try:
            return r.json()["url"]
        except:
            return "ERROR: Failed to extract URL from JSON response"
            
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
