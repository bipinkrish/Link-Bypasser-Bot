"""
Antfiles direct download link generator
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Site configuration
SITE_NAME = "Antfiles"
URL_PATTERNS = [
    r'antfiles\.com/'
]

def antfiles_bypass(url):
    """
    Generate direct download link for Antfiles
    """
    try:
        sess = requests.Session()
        raw = sess.get(url)
        soup = BeautifulSoup(raw.content, "html.parser")

        # Find the main download button
        download_link = soup.find(class_="main-btn", href=True)
        
        if download_link:
            parsed_url = urlparse(url)
            return f"{parsed_url.scheme}://{parsed_url.netloc}/{download_link['href']}"
        else:
            return "ERROR: Could not find download link in Antfiles page"

    except Exception as e:
        return f"Error processing Antfiles: {str(e)}"

# Common export function name
process_url = antfiles_bypass
