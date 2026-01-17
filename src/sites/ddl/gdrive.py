"""
Google Drive direct download link generator
"""

import requests
import re

# Site configuration
SITE_NAME = "Google Drive"
URL_PATTERNS = [
    r'drive\.google\.com/file/d/',
    r'drive\.google\.com/open\?id=',
    r'docs\.google\.com/.*export'
]

def generate_gdrive_link(url):
    """
    Generate direct download link for Google Drive
    """
    try:
        # Extract file ID from various Google Drive URL formats
        file_id = None
        
        patterns = [
            r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
            r'drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)',
            r'id=([a-zA-Z0-9_-]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                file_id = match.group(1)
                break
                
        if not file_id:
            return f"Could not extract Google Drive file ID from URL: {url}"
            
        # Generate direct download URL
        direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        
        # For large files, Google Drive requires confirmation
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(direct_url, headers=headers, timeout=10)
        
        # Check if it's a large file that needs confirmation
        if 'download_warning' in response.text:
            # Extract the confirmation token
            confirm_match = re.search(r'confirm=([^&]+)', response.text)
            if confirm_match:
                confirm_token = confirm_match.group(1)
                confirmed_url = f"https://drive.google.com/uc?export=download&confirm={confirm_token}&id={file_id}"
                return confirmed_url
                
        return direct_url
        
    except Exception as e:
        return f"Error generating Google Drive link: {str(e)}"

# Common export function name
process_url = generate_gdrive_link
