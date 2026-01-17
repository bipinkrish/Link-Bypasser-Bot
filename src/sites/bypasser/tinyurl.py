"""
TinyURL bypasser - Simple URL shortener bypass
"""

import requests

# Site configuration
SITE_NAME = "TinyURL"
URL_PATTERNS = [
    r'tinyurl\.com/',
    r'tinyurl\.com/[a-zA-Z0-9]+'
]

def bypass_tinyurl(url):
    """
    Bypass TinyURL shortened URLs
    """
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        return response.url
    except Exception as e:
        return f"Error bypassing TinyURL: {str(e)}"

# Common export function name
process_url = bypass_tinyurl
