#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Letsupload DDL bypasser
Extracts direct download links from letsupload.io

Site: letsupload.io
Method: POST request to get direct link from response text
"""

import re
try:
    from cloudscraper import create_scraper
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False

# Site configuration
SITE_NAME = "letsupload"
URL_PATTERNS = [
    r'letsupload\.io'
]

def process_url(url: str) -> str:
    """
    Extract direct download link from letsupload.io
    
    Args:
        url: letsupload.io URL
        
    Returns:
        Direct download link or error message
    """
    if not SCRAPER_AVAILABLE:
        return "ERROR: cloudscraper module not available"
    
    cget = create_scraper().request
    try:
        res = cget("POST", url)
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
    
    direct_link = re.findall(r"(https?://letsupload\.io\/.+?)\'", res.text)
    if direct_link:
        return direct_link[0]
    else:
        return "ERROR: Direct Link not found"
