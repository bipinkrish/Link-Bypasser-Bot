"""
Gofile direct download link generator
"""

import hashlib
import requests

# Site configuration
SITE_NAME = "Gofile"
URL_PATTERNS = [
    r'gofile\.io/d/',
    r'gofile\.io/c/',
    r'gofile\.io/'
]

def gofile_bypass(url, password=""):
    """
    Generate direct download link for Gofile using official API
    """
    try:
        api_uri = "https://api.gofile.io"
        client = requests.Session()
        
        # Create account
        res = client.get(api_uri + "/createAccount").json()
        
        if "data" not in res or "token" not in res["data"]:
            return "Error: Could not create Gofile account"

        data = {
            "contentId": url.split("/")[-1],
            "token": res["data"]["token"],
            "websiteToken": "12345", 
            "cache": "true",
            "password": hashlib.sha256(password.encode("utf-8")).hexdigest(),
        }
        
        res = client.get(api_uri + "/getContent", params=data).json()
        
        if "data" not in res or "contents" not in res["data"]:
            return "Error: Could not get Gofile content"

        content = []
        for item in res["data"]["contents"].values():
            content.append(item)
            
        if not content:
            return "Error: No files found in Gofile link"

        return content[0]["link"]

    except Exception as e:
        return f"Error processing Gofile: {str(e)}"

# Common export function name
process_url = gofile_bypass