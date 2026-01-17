"""
OSDN direct download link generator
"""

import re
from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup
from cfscrape import create_scraper

# Site configuration
SITE_NAME = "OSDN"
URL_PATTERNS = [
    r'osdn\.net/'
]

def osdn_bypass(url):
    """
    Generate direct download link for OSDN
    """
    try:
        osdn_link = "https://osdn.net"
        
        # Extract OSDN link if provided in a mixed URL
        try:
            link = re.findall(r"\bhttps?://.*osdn\.net\S+", url)[0]
        except IndexError:
            link = url  # Use original URL if it's already an OSDN link
            
        try:
            cget = create_scraper().request
            response = cget("get", link, allow_redirects=True)
            page = BeautifulSoup(response.content, "lxml")
        except:
            # Fallback to regular requests
            response = requests.get(link, allow_redirects=True)
            page = BeautifulSoup(response.content, "lxml")
        
        info = page.find("a", {"class": "mirror_link"})
        if not info:
            return "ERROR: Could not find mirror link in OSDN page"
            
        link = unquote(osdn_link + info["href"])
        
        mirrors_form = page.find("form", {"id": "mirror-select-form"})
        if not mirrors_form:
            return link  # Return direct link if no mirrors found
            
        mirrors = mirrors_form.findAll("tr")
        if len(mirrors) > 1:
            # Use first available mirror
            mirror_input = mirrors[1].find("input")
            if mirror_input:
                mirror = mirror_input["value"]
                link = re.sub(r"m=(.*)&f", f"m={mirror}&f", link)
                
        return link

    except Exception as e:
        return f"Error processing OSDN: {str(e)}"

# Common export function name
process_url = osdn_bypass
