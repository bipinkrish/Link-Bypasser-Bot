"""
Terabox direct download link generator
"""

import requests
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "Terabox Family"
URL_PATTERNS = [
    r'terabox\.com/', r'www\.terabox\.com/', r'teraboxapp\.com/',
    r'4funbox\.com/', r'mirrobox\.com/', r'nephobox\.com/', r'momerybox\.com/'
]

def terabox_bypass(url):
    """
    Generate direct download link for Terabox files
    """
    try:
        sess = requests.session()
        
        # Get initial page
        res = sess.get(url)
        url = res.url

        key = url.split("?surl=")[-1]
        url = f"http://www.terabox.com/wap/share/filelist?surl={key}"

        # Note: This would need TERA_COOKIE for full functionality
        # For now, attempt without cookie
        try:
            res = sess.get(url)
        except Exception as e:
            return f"Error accessing Terabox: {str(e)}"

        key = res.url.split("?surl=")[-1]
        soup = BeautifulSoup(res.content, "lxml")
        jsToken = None

        # Extract JS token
        for fs in soup.find_all("script"):
            fstring = fs.string
            if fstring and fstring.startswith("try {eval(decodeURIComponent"):
                jsToken = fstring.split("%22")[1]
                break

        if not jsToken:
            return "Error: Could not find Terabox authentication token"

        # Get file list
        list_url = f"https://www.terabox.com/share/list?app_id=250528&jsToken={jsToken}&shorturl={key}&root=1"
        res = sess.get(list_url)
        result = res.json()

        if result["errno"] != 0:
            return f"ERROR: '{result['errmsg']}' Check Terabox access"
            
        result = result["list"]
        if len(result) > 1:
            return "ERROR: Can't download multiple files from Terabox"
            
        result = result[0]

        if result["isdir"] != "0":
            return "ERROR: Can't download folder from Terabox"
            
        return result.get("dlink", "Error: No download link found")

    except Exception as e:
        return f"Error processing Terabox: {str(e)}"

# Common export function name
process_url = terabox_bypass
