"""
Yandex.Disk direct download link generator
"""

import re
import requests
from cfscrape import create_scraper

# Site configuration
SITE_NAME = "Yandex.Disk"
URL_PATTERNS = [
    r'yadi\.sk/',
    r'disk\.yandex\.com/'
]

def yandex_disk_bypass(url):
    """
    Generate direct download link for Yandex.Disk
    Based on https://github.com/wldhx/yadisk-direct
    """
    try:
        # Extract Yandex.Disk link
        try:
            link = re.findall(r"\b(https?://(yadi\.sk|disk\.yandex\.com)\S+)", url)[0][0]
        except IndexError:
            return "No Yandex.Disk links found in URL"
            
        api = "https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}"
        
        try:
            cget = create_scraper().request
            response = cget("get", api.format(link)).json()
        except:
            # Fallback to regular requests
            response = requests.get(api.format(link)).json()
            
        if "href" in response:
            return response["href"]
        else:
            return "ERROR: File not found/Download limit reached"

    except Exception as e:
        return f"Error processing Yandex.Disk: {str(e)}"

# Common export function name
process_url = yandex_disk_bypass
