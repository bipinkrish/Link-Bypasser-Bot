"""
Pixeldrain direct download link generator
"""

import requests
import re
from cfscrape import create_scraper

# Site configuration
SITE_NAME = "Pixeldrain"
URL_PATTERNS = [
    r'pixeldrain\.com/u/',
    r'pixeldrain\.com/api/',
    r'pixeldrain\.com/l/'
]

def pixeldrain_bypass(url):
    """
    Generate direct download link for Pixeldrain files
    """
    try:
        url = url.strip("/ ")
        file_id = url.split("/")[-1]
        
        # Check if it's a list or single file
        if url.split("/")[-2] == "l":
            info_link = f"https://pixeldrain.com/api/list/{file_id}"
            dl_link = f"https://pixeldrain.com/api/list/{file_id}/zip?download"
        else:
            info_link = f"https://pixeldrain.com/api/file/{file_id}/info"
            dl_link = f"https://pixeldrain.com/api/file/{file_id}?download"
            
        try:
            cget = create_scraper().request
            resp = cget("get", info_link).json()
        except Exception as e:
            # Fallback to regular requests if cfscraper not available
            try:
                resp = requests.get(info_link).json()
            except:
                return f"ERROR: Could not access Pixeldrain API - {e.__class__.__name__}"
        
        if resp.get("success", True):  # Some responses don't have success field
            return dl_link
        else:
            return f"ERROR: Can't download due to {resp.get('message', 'unknown error')}"

    except Exception as e:
        return f"Error processing Pixeldrain: {str(e)}"

# Common export function name
process_url = pixeldrain_bypass
