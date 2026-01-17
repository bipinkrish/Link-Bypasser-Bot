#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Shorte.st (sh.st) bypasser
Bypasses shorte.st shortened URLs

Site: sh.st (shorte.st)
Method: Session-based bypass with adSessionId extraction
"""

import time
import re
from urllib.parse import urlparse

try:
    import requests
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False

# Site configuration
SITE_NAME = "shorte_st"
URL_PATTERNS = [
    r'sh\.st',
    r'shorte\.st'
]

def process_url(url: str) -> str:
    """
    Bypass sh.st/shorte.st URLs
    
    Args:
        url: sh.st or shorte.st URL
        
    Returns:
        Final destination URL or error message
    """
    if not SCRAPER_AVAILABLE:
        return "ERROR: requests module not available"
    
    try:
        client = requests.Session()
        client.headers.update({"referer": url})
        p = urlparse(url)

        res = client.get(url)

        sess_id = re.findall(r"""sessionId(?:\s+)?:(?:\s+)?['|"](.*?)['|"]""", res.text)[0]

        final_url = f"{p.scheme}://{p.netloc}/shortest-url/end-adsession"
        params = {"adSessionId": sess_id, "callback": "_"}
        
        time.sleep(5)  # Important delay

        res = client.get(final_url, params=params)
        dest_url = re.findall(r'"(.*?)"', res.text)[1].replace(r"\/", "/")

        return dest_url
        
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
