"""
Pdisk bypasser
"""

import requests
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "Pdisk"
URL_PATTERNS = [
    r'pdisk\.pro/',
    r'pdisk\.me/',
    r'pdisk\.net/'
]

def pdisk_bypass(url):
    """
    Bypass Pdisk links to get direct video URLs
    """
    try:
        response = requests.get(url)
        content = response.text
        
        # Try to extract from HTML comment
        try:
            direct_url = content.split("<!-- ")[-1].split(" -->")[0]
            if direct_url and direct_url.startswith("http"):
                return direct_url
        except:
            pass
            
        # Try to extract from video source tag
        try:
            soup = BeautifulSoup(content, "html.parser")
            video_elem = soup.find("video")
            if video_elem:
                source_elem = video_elem.find("source")
                if source_elem and source_elem.get("src"):
                    return source_elem.get("src")
        except:
            pass
            
        return "Could not extract direct URL from Pdisk link"

    except Exception as e:
        return f"Error bypassing Pdisk: {str(e)}"

# Common export function name
process_url = pdisk_bypass
