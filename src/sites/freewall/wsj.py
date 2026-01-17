"""
Wall Street Journal paywall bypasser
"""

import requests
import urllib.parse

# Site configuration
SITE_NAME = "Wall Street Journal"
URL_PATTERNS = [
    r'wsj\.com/articles/',
    r'wsj\.com/.*'
]

def bypass_wsj_paywall(url):
    """
    Bypass Wall Street Journal paywall using archive services
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Method 1: Try 12ft.io
        twelve_ft_url = f"https://12ft.io/{url}"
        response = requests.head(twelve_ft_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return twelve_ft_url
            
        # Method 2: Try Archive.today 
        encoded_url = urllib.parse.quote(url, safe='')
        archive_url = f"https://archive.today/?run=1&url={encoded_url}"
        
        # Method 3: Try Google Cache
        google_cache = f"https://webcache.googleusercontent.com/search?q=cache:{url}"
        
        return f"WSJ paywall bypass options:\n1. {twelve_ft_url}\n2. {archive_url}\n3. {google_cache}"
        
    except Exception as e:
        return f"Error bypassing WSJ paywall: {str(e)}"

# Common export function name
process_url = bypass_wsj_paywall
