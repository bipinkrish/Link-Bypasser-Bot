"""
Upload.ee direct download link generator
"""

import requests
from bs4 import BeautifulSoup
from cfscrape import create_scraper

# Site configuration
SITE_NAME = "Upload.ee"
URL_PATTERNS = [
    r'upload\.ee/',
    r'uploadee\.com/'
]

def uploadee_bypass(url):
    """
    Generate direct download link for Upload.ee
    By https://github.com/iron-heart-x
    """
    try:
        try:
            cget = create_scraper().request
            content = cget("get", url).content
        except:
            # Fallback to regular requests
            content = requests.get(url).content
            
        soup = BeautifulSoup(content, "lxml")
        download_link = soup.find("a", attrs={"id": "d_l"})
        
        if not download_link:
            return f"ERROR: Could not find download link in Upload.ee page"
            
        return download_link["href"]
        
    except Exception as e:
        return f"Error processing Upload.ee: {str(e)}"

# Common export function name
process_url = uploadee_bypass
