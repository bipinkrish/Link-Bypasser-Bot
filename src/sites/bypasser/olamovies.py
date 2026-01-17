"""
OlaMovies bypasser
"""

import requests
import re

# Site configuration
SITE_NAME = "OlaMovies"
URL_PATTERNS = [
    r'olamovies\.',
    r'olamoviesstatus\.'
]

def bypass_olamovies(url):
    """
    Bypass OlaMovies links
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Extract the actual link from OlaMovies page
        # Usually it's in a form or hidden input
        content = response.text
        
        # Look for actual download/bypass link patterns
        link_patterns = [
            r'location\.href\s*=\s*["\']([^"\']+)["\']',
            r'window\.open\s*\(\s*["\']([^"\']+)["\']',
            r'href\s*=\s*["\']([^"\']+)["\'].*?(?:download|bypass|continue)'
        ]
        
        for pattern in link_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                result_url = match.group(1)
                if result_url.startswith('http'):
                    return result_url
        
        return f"Could not extract link from OlaMovies: {url}"
        
    except Exception as e:
        return f"Error bypassing OlaMovies: {str(e)}"

# Common export function name
process_url = bypass_olamovies
