"""
Solidfiles direct download link generator
"""

import re
from json import loads
import requests
from cfscrape import create_scraper

# Site configuration
SITE_NAME = "Solidfiles"
URL_PATTERNS = [
    r'solidfiles\.com/'
]

def solidfiles_bypass(url):
    """
    Generate direct download link for Solidfiles
    Based on https://github.com/Xonshiz/SolidFiles-Downloader
    By https://github.com/Jusidama18
    """
    try:
        try:
            cget = create_scraper().request
        except:
            # Fallback to regular requests
            cget = requests.get
            
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
        }
        
        pageSource = cget(url, headers=headers).text
        
        # Extract viewerOptions from JavaScript
        match = re.search(r"viewerOptions\'\,\ (.*?)\)\;", pageSource)
        if not match:
            return f"ERROR: Could not find viewerOptions in Solidfiles page"
            
        mainOptions = match.group(1)
        options_data = loads(mainOptions)
        
        if "downloadUrl" not in options_data:
            return f"ERROR: No download URL found in Solidfiles data"
            
        return options_data["downloadUrl"]
        
    except Exception as e:
        return f"Error processing Solidfiles: {str(e)}"

# Common export function name
process_url = solidfiles_bypass
