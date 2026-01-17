#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Anonfile bypasser (simplified)
Direct link extraction from anonfiles.com using text parsing

Site: anonfiles.com
Method: Text parsing to find CDN links
"""

try:
    import requests
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False

# Site configuration
SITE_NAME = "anonfile"
URL_PATTERNS = [
    r'anonfiles\.com/[a-zA-Z0-9]+/'
]

def process_url(url: str) -> str:
    """
    Extract direct download link from anonfiles.com
    
    Args:
        url: anonfiles.com URL
        
    Returns:
        Direct download link or error message
    """
    if not SCRAPER_AVAILABLE:
        return "ERROR: requests module not available"
    
    try:
        headersList = {"Accept": "*/*"}
        payload = ""

        response = requests.request(
            "GET", url, data=payload, headers=headersList
        ).text.split("\n")
        
        for ele in response:
            if (
                "https://cdn" in ele
                and "anonfiles.com" in ele
                and url.split("/")[-2] in ele
            ):
                break
        else:
            return "ERROR: CDN link not found in response"

        return ele.split('href="')[1].split('"')[0]
        
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
