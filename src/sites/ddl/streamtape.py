"""
Streamtape direct download link generator
"""

import re
import requests

# Site configuration
SITE_NAME = "Streamtape"
URL_PATTERNS = [
    r'streamtape\.com/',
    r'streamtape\.co/'
]

def streamtape_bypass(url):
    """
    Generate direct download link for Streamtape
    """
    try:
        response = requests.get(url)
        
        # Find video link from page
        videolink = re.findall(r"document.*((?=id\=)[^\"']+)", response.text)
        
        if videolink:
            nexturl = "https://streamtape.com/get_video?" + videolink[-1]
            return nexturl
        else:
            return "ERROR: Could not find video link in Streamtape page"

    except Exception as e:
        return f"Error processing Streamtape: {str(e)}"

# Common export function name
process_url = streamtape_bypass
