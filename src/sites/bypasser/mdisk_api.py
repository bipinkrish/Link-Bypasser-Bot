#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mdisk bypasser
Extracts direct download links from mdisk.me URLs

Site: mdisk.me
Method: API-based download link extraction
"""

try:
    import requests
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False

# Site configuration
SITE_NAME = "mdisk"
URL_PATTERNS = [
    r'mdisk\.me'
]

def process_url(url: str) -> str:
    """
    Extract download links from mdisk.me URLs
    
    Args:
        url: mdisk.me URL
        
    Returns:
        Download and source links or error message
    """
    if not SCRAPER_AVAILABLE:
        return "ERROR: requests module not available"
    
    try:
        header = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://mdisk.me/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        }

        inp = url
        fxl = inp.split("/")
        cid = fxl[-1]

        URL = f"https://diskuploader.entertainvideo.com/v1/file/cdnurl?param={cid}"
        res = requests.get(url=URL, headers=header).json()
        return res["download"] + "\n\n" + res["source"]
        
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
