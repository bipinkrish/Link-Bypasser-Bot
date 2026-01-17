"""
Linkvertise bypasser
"""

import requests
import re

# Site configuration
SITE_NAME = "Linkvertise"
URL_PATTERNS = [
    r'linkvertise\.com/',
    r'link-to\.net/',
    r'linkvertise\.net/'
]

def linkvertise_bypass(url):
    """
    Bypass Linkvertise short links using bypass.pm service
    """
    try:
        params = {
            "url": url,
        }
        
        response = requests.get("https://bypass.pm/bypass2", params=params).json()
        
        if response["success"]:
            return response["destination"]
        else:
            return response.get("msg", "Error bypassing Linkvertise")

    except Exception as e:
        return f"Error bypassing Linkvertise: {str(e)}"

# Common export function name
process_url = linkvertise_bypass
