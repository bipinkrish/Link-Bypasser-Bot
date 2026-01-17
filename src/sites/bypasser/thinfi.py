"""
Thinfi bypasser
"""

import requests
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "Thinfi"
URL_PATTERNS = [
    r'thinfi\.com/'
]

def thinfi_bypass(url):
    """
    Bypass Thinfi short links
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the first paragraph's link
        p_tag = soup.find("p")
        if p_tag and p_tag.find("a"):
            direct_url = p_tag.find("a").get("href")
            return direct_url if direct_url else "Could not extract link from Thinfi"
        else:
            return "Could not find link in Thinfi page structure"

    except Exception as e:
        return f"Error bypassing Thinfi: {str(e)}"

# Common export function name
process_url = thinfi_bypass
