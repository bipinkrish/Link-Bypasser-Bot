"""
Anonfiles-based sites bypasser
"""

import requests
from bs4 import BeautifulSoup
from cfscrape import create_scraper

# Site configuration
SITE_NAME = "Anonfiles Family"
URL_PATTERNS = [
    r'anonfiles\.com/', r'bayfiles\.com/', r'hotfile\.', r'letsupload\.', r'megaupload\.', 
    r'filechan\.', r'myfile\.', r'vshare\.', r'rapidshare\.', r'lolabits\.',
    r'openload\.', r'share-online\.', r'upvid\.'
]

def anonfiles_bypass(url):
    """
    Generate direct download link for Anonfiles and similar sites
    """
    try:
        try:
            cget = create_scraper().request
            content = cget("get", url).content
        except:
            # Fallback to regular requests
            content = requests.get(url).content
            
        soup = BeautifulSoup(content, "lxml")
        download_elem = soup.find(id="download-url")
        
        if not download_elem:
            return "ERROR: File not found or download link unavailable!"
            
        return download_elem["href"]
        
    except Exception as e:
        return f"Error processing Anonfiles-based site: {str(e)}"

# Common export function name
process_url = anonfiles_bypass
