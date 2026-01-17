"""
Slideshare presentation downloader
"""

import requests

# Site configuration
SITE_NAME = "Slideshare"
URL_PATTERNS = [
    r'slideshare\.net/'
]

def slideshare_bypass(url, file_type="pptx"):
    """
    Download Slideshare presentations
    """
    try:
        # enum = {"pdf","pptx","img"}
        if file_type not in ["pdf", "pptx", "img"]:
            file_type = "pptx"
            
        response = requests.get(
            f"https://downloader.at/convert2{file_type}.php", 
            params={"url": url}
        )
        
        if response.status_code == 200:
            return f"Slideshare content downloaded as {file_type}"
        else:
            return "Error: Could not download Slideshare presentation"

    except Exception as e:
        return f"Error downloading Slideshare: {str(e)}"

# Common export function name
process_url = slideshare_bypass
