"""
GDTot bypasser
"""

import re
from urllib.parse import urlparse
from cfscrape import create_scraper
from lxml import etree

# Site configuration
SITE_NAME = "GDTot"
URL_PATTERNS = [
    r'gdtot\.cloud/',
    r'gdtot\.eu/',
    r'gdtot\.me/'
]

def gdtot_bypass(url):
    """
    Bypass GDTot short links
    """
    try:
        cget = create_scraper().request
        
        try:
            res = cget("GET", f'https://gdbot.xyz/file/{url.split("/")[-1]}')
        except Exception as e:
            return f"ERROR: {e.__class__.__name__}"
            
        token_url = etree.HTML(res.content).xpath(
            "//a[contains(@class,'inline-flex items-center justify-center')]/@href"
        )
        
        if not token_url:
            try:
                url = cget("GET", url).url
                p_url = urlparse(url)
                res = cget(
                    "GET", f"{p_url.scheme}://{p_url.hostname}/ddl/{url.split('/')[-1]}"
                )
            except Exception as e:
                return f"ERROR: {e.__class__.__name__}"
                
            if (
                drive_link := re.findall(r"myDl\('(.*?)'\)", res.text)
            ) and "drive.google.com" in drive_link[0]:
                return drive_link[0]
            else:
                return "ERROR: Drive Link not found, Try in your browser"
                
        token_url = token_url[0]
        
        try:
            token_page = cget("GET", token_url)
        except Exception as e:
            return f"ERROR: {e.__class__.__name__} with {token_url}"
            
        path = re.findall('\("(.*?)"\)', token_page.text)
        if not path:
            return "ERROR: Cannot bypass this GDTot link"
            
        path = path[0]
        raw = urlparse(token_url)
        final_url = f"{raw.scheme}://{raw.hostname}{path}"
        
        # Note: This references ddl module which would need to be imported
        # For now returning the direct URL
        return final_url

    except Exception as e:
        return f"Error bypassing GDTot: {str(e)}"

# Common export function name
process_url = gdtot_bypass
