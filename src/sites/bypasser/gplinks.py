"""
GPlinks bypasser
"""

import time
import cloudscraper
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "GPlinks"
URL_PATTERNS = [
    r'gplinks\.co/',
    r'gplinks\.in/',
    r'gplinks\.com/'
]

def gplinks_bypass(url):
    """
    Bypass GPlinks short links
    """
    try:
        client = cloudscraper.create_scraper(allow_brotli=False)
        token = url.split("/")[-1]
        domain = "https://gplinks.co/"
        referer = "https://mynewsmedia.co/"
        
        # Get redirect URL
        location_response = client.get(url, allow_redirects=False)
        if "Location" not in location_response.headers:
            return "Error: No redirect found in GPlinks URL"
            
        vid = location_response.headers["Location"].split("=")[-1]
        url = f"{url}/?{vid}"
        
        response = client.get(url, allow_redirects=False)
        soup = BeautifulSoup(response.content, "html.parser")
        
        go_link_elem = soup.find(id="go-link")
        if not go_link_elem:
            return "Error: Could not find go-link element in GPlinks page"
            
        inputs = go_link_elem.find_all(name="input")
        data = {input.get("name"): input.get("value") for input in inputs}
        
        time.sleep(10)
        headers = {"x-requested-with": "XMLHttpRequest"}
        
        bypassed_response = client.post(domain + "links/go", data=data, headers=headers)
        bypassed_url = bypassed_response.json()["url"]
        
        return bypassed_url

    except Exception as e:
        return f"Error bypassing GPlinks: {str(e)}"

# Common export function name
process_url = gplinks_bypass
