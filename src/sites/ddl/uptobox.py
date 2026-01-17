"""
Uptobox direct download link generator
"""

import re
from time import sleep
import requests
from cfscrape import create_scraper

# Site configuration
SITE_NAME = "Uptobox"
URL_PATTERNS = [
    r'uptobox\.com/'
]

def uptobox_bypass(url):
    """
    Generate direct download link for Uptobox
    Based on https://github.com/jovanzers/WinTenCermin and https://github.com/sinoobie/noobie-mirror
    """
    try:
        # Validate Uptobox URL
        try:
            link = re.findall(r"\bhttps?://.*uptobox\.com\S+", url)[0]
        except IndexError:
            return "No Uptobox links found in URL"
            
        # Check if already a direct link
        dl_link = re.findall(r"\bhttps?://.*\.uptobox\.com/dl\S+", url)
        if dl_link:
            return dl_link[0]
            
        try:
            cget = create_scraper().request
        except:
            # Fallback to regular requests
            cget = requests.get
            
        try:
            file_id = re.findall(r"\bhttps?://.*uptobox\.com/(\w+)", url)[0]
            # Using API without token (limited functionality)
            file_link = f"https://uptobox.com/api/link?file_code={file_id}"
            res = cget(file_link).json()
        except Exception as e:
            return f"ERROR: {e.__class__.__name__}"
            
        if res["statusCode"] == 0:
            return res["data"]["dlLink"]
        elif res["statusCode"] == 16:
            # Wait required
            sleep(1)
            waiting_token = res["data"]["waitingToken"]
            sleep(res["data"]["waiting"])
            try:
                res = cget(f"{file_link}&waitingToken={waiting_token}").json()
                return res["data"]["dlLink"]
            except Exception as e:
                return f"ERROR: {e.__class__.__name__}"
        elif res["statusCode"] == 39:
            return f"ERROR: Uptobox is being limited, please wait"
        else:
            return f"ERROR: {res.get('message', 'Unknown Uptobox API error')}"

    except Exception as e:
        return f"Error processing Uptobox: {str(e)}"

# Common export function name
process_url = uptobox_bypass
