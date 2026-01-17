"""
Mdisk direct download link generator
"""

import requests

# Site configuration
SITE_NAME = "Mdisk"
URL_PATTERNS = [
    r'mdisk\.me/'
]

def mdisk_bypass(url):
    """
    Generate direct download link for Mdisk
    """
    try:
        header = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://mdisk.me/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        }
        
        # Extract file ID from URL
        file_id = url.split("/")[-1]
        API_URL = f"https://diskuploader.entertainvideo.com/v1/file/cdnurl?param={file_id}"
        
        response = requests.get(url=API_URL, headers=header)
        response.raise_for_status()
        
        json_data = response.json()
        
        if "source" in json_data:
            return json_data["source"]
        else:
            return "ERROR: Could not find source URL in Mdisk response"

    except Exception as e:
        return f"Error processing Mdisk: {str(e)}"

# Common export function name
process_url = mdisk_bypass
