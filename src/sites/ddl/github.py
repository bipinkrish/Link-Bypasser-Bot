"""
GitHub releases direct download link generator
"""

import re
import requests
from cfscrape import create_scraper

# Site configuration
SITE_NAME = "GitHub"
URL_PATTERNS = [
    r'github\.com/.*?/releases/'
]

def github_bypass(url):
    """
    Generate direct download link for GitHub releases
    """
    try:
        # Validate it's a GitHub releases URL
        try:
            re.findall(r"\bhttps?://.*github\.com.*releases\S+", url)[0]
        except IndexError:
            return "No GitHub Releases links found in URL"
            
        try:
            cget = create_scraper().request
            download = cget("get", url, stream=True, allow_redirects=False)
        except:
            # Fallback to regular requests
            download = requests.get(url, stream=True, allow_redirects=False)
            
        # GitHub releases redirect to direct download links
        if "location" in download.headers:
            return download.headers["location"]
        elif "Location" in download.headers:
            return download.headers["Location"]
        else:
            return "ERROR: Can't extract the direct download link from GitHub"

    except Exception as e:
        return f"Error processing GitHub: {str(e)}"

# Common export function name
process_url = github_bypass
