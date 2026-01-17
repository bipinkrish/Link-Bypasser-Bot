"""
Zippyshare direct download link generator
"""

import requests
import re
from lxml import etree

# Site configuration
SITE_NAME = "Zippyshare"
URL_PATTERNS = [
    r'zippyshare\.com/v/',
    r'www\d+\.zippyshare\.com/v/'
]

def zippyshare_bypass(url):
    """
    Generate direct download link for Zippyshare
    """
    try:
        # Use regular requests since cfscraper might not be available
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers)
        
        if not resp.ok:
            return f"Zippyshare file not accessible: {url}"
            
        if re.findall(r">File does not exist on this server<", resp.text):
            return f"Zippyshare file does not exist: {url}"
            
        # Look for the download button JavaScript
        script_match = re.search(r'document\.getElementById\(\'dlbutton\'\)\.href\s*=\s*"([^"]+)"\s*\+\s*\(([^)]+)\)', resp.text)
        if script_match:
            try:
                base_url = script_match.group(1)
                math_expr = script_match.group(2)
                
                # Safely evaluate simple math expressions
                if re.match(r'^[\d\s\+\-\*\/\(\)%]+$', math_expr):
                    result = eval(math_expr)
                    download_url = base_url + str(result)
                    return download_url
            except:
                pass
                    
        return f"Could not extract Zippyshare download link: {url}"
        
    except Exception as e:
        return f"Error processing Zippyshare: {str(e)}"

# Common export function name
process_url = zippyshare_bypass
