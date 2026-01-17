"""
Medium paywall bypasser
"""

import requests
import urllib.parse

# Site configuration
SITE_NAME = "Medium"
URL_PATTERNS = [
    r'medium\.com/@',
    r'medium\.com/p/',
    r'[^/]+\.medium\.com'
]

def bypass_medium_paywall(url):
    """
    Bypass Medium paywall using archive services
    """
    try:
        # Method 1: Try Freedium
        freedium_url = f"https://freedium.cfd/{url}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.head(freedium_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return freedium_url
            
        # Method 2: Try 12ft.io
        twelve_ft_url = f"https://12ft.io/{url}"
        response = requests.head(twelve_ft_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return twelve_ft_url
            
        # Method 3: Try Archive.today
        encoded_url = urllib.parse.quote(url, safe='')
        archive_url = f"https://archive.today/?run=1&url={encoded_url}"
        
        return archive_url
        
    except Exception as e:
        return f"Error bypassing Medium paywall: {str(e)}"

# Common export function name
process_url = bypass_medium_paywall
