"""
WeTransfer direct download link generator
"""

import requests
from cfscrape import create_scraper

# Site configuration
SITE_NAME = "WeTransfer"
URL_PATTERNS = [
    r'wetransfer\.com/',
    r'we\.tl/'
]

def wetransfer_bypass(url):
    """
    Generate direct download link for WeTransfer
    """
    try:
        try:
            cget = create_scraper().request
        except:
            # Fallback to regular requests
            def cget(method, url, **kwargs):
                return requests.request(method, url, **kwargs)
                
        # Get the actual transfer URL  
        try:
            response = cget("GET", url)
            url = response.url
        except:
            pass  # Use original URL if redirect fails
            
        # Extract transfer ID and security hash
        url_parts = url.split("/")
        if len(url_parts) < 2:
            return "ERROR: Invalid WeTransfer URL format"
            
        transfer_id = url_parts[-2]
        security_hash = url_parts[-1]
        
        json_data = {
            "security_hash": security_hash, 
            "intent": "entire_transfer"
        }
        
        api_url = f'https://wetransfer.com/api/v4/transfers/{transfer_id}/download'
        res = cget("POST", api_url, json=json_data).json()
        
        if "direct_link" in res:
            return res["direct_link"]
        elif "message" in res:
            return f"ERROR: {res['message']}"
        elif "error" in res:
            return f"ERROR: {res['error']}"
        else:
            return "ERROR: Cannot find direct link for WeTransfer"

    except Exception as e:
        return f"Error processing WeTransfer: {str(e)}"

# Common export function name
process_url = wetransfer_bypass
