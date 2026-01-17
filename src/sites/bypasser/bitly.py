"""
Bitly bypasser - Simple URL shortener bypass
"""

import requests

# Site configuration
SITE_NAME = "Bitly"
URL_PATTERNS = [
    r'bit\.ly',
    r'bitly\.com'
]

def bypass_bitly(url):
    """
    Bypass bitly shortened URLs
    """
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        return response.url
    except Exception as e:
        return f"Error bypassing bitly: {str(e)}"

# Common export function name
process_url = bypass_bitly
