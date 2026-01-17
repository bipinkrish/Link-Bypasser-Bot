"""
MediaFire direct download link generator
"""

import requests
import re
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Warning: BeautifulSoup not available for MediaFire module")
    BeautifulSoup = None

# Site configuration
SITE_NAME = "MediaFire"
URL_PATTERNS = [
    r'mediafire\.com/file/',
    r'mediafire\.com/\?',
    r'mediafire\.com/download/'
]

def generate_mediafire_link(url):
    """
    Generate direct download link for MediaFire
    """
    try:
        if BeautifulSoup is None:
            return f"BeautifulSoup required for MediaFire: {url}"
            
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find the download button/link
        download_button = soup.find('a', {'aria-label': 'Download file'})
        if download_button and download_button.get('href'):
            return download_button['href']
            
        # Fallback: look for direct download link in scripts
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'downloadUrl' in script.string:
                match = re.search(r'"downloadUrl":"([^"]+)"', script.string)
                if match:
                    return match.group(1).replace('\\', '')
        
        return f"Could not extract direct link from MediaFire: {url}"
        
    except Exception as e:
        return f"Error generating MediaFire link: {str(e)}"

# Common export function name  
process_url = generate_mediafire_link
