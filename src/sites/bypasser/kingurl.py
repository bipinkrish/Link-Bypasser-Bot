#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kingurl bypasser
Supports both kingurl.in variants

Sites: go.kingurl.in, earn.bankshiksha.in
Methods: Form submission for go.kingurl.in, direct redirect for bankshiksha
"""

import time
try:
    from cloudscraper import create_scraper
    from bs4 import BeautifulSoup
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False

# Site configuration
SITE_NAME = "kingurl"
URL_PATTERNS = [
    r'kingurl\.in',
    r'bankshiksha\.in'
]

def process_url(url: str) -> str:
    """
    Bypass kingurl.in links
    
    Args:
        url: kingurl.in URL
        
    Returns:
        Bypassed URL or error message
    """
    if not SCRAPER_AVAILABLE:
        return "ERROR: cloudscraper and bs4 modules not available"
    
    try:
        if "go.kingurl.in" in url:
            return kingurl1_bypass(url)
        else:
            return kingurl_bypass(url)
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"

def kingurl1_bypass(url: str) -> str:
    """Bypass go.kingurl.in links with form submission"""
    client = create_scraper(allow_brotli=False)
    DOMAIN = "https://go.kingurl.in/"
    url = url[:-1] if url[-1] == "/" else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://earnbox.bankshiksha.in/"
    h = {"referer": ref}
    
    resp = client.get(final_url, headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = {input.get("name"): input.get("value") for input in inputs}
    h = {"x-requested-with": "XMLHttpRequest"}
    
    time.sleep(7)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return str(r.json()["url"])
    except:
        return "ERROR: Failed to extract URL from JSON response"

def kingurl_bypass(url: str) -> str:
    """Bypass earn.bankshiksha.in links with direct redirect"""
    DOMAIN = "https://earn.bankshiksha.in/click.php?LinkShortUrlID"
    url = url[:-1] if url[-1] == "/" else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}={code}"
    return final_url
