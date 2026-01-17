"""
Pixl.is bypasser
"""

import time
import cloudscraper
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "Pixl"
URL_PATTERNS = [
    r'pixl\.is/'
]

def pixl_bypass(url):
    """
    Bypass Pixl.is image/album links
    """
    try:
        client = cloudscraper.create_scraper(allow_brotli=False)
        resp = client.get(url)
        
        if resp.status_code == 404:
            return "File not found/The link you entered is wrong!"
            
        soup = BeautifulSoup(resp.content, "html.parser")
        
        # Handle album links
        if "album" in url:
            dl_msg = ""
            count = 1
            
            totalimages_elem = soup.find("span", {"data-text": "image-count"})
            if totalimages_elem:
                totalimages = totalimages_elem.text
                dl_msg += f"Album contains {totalimages} images:\n\n"
                
            thmbnailanch = soup.findAll(attrs={"class": "--media"})
            
            for ref in thmbnailanch:
                if count > 10:  # Limit to avoid excessive processing
                    dl_msg += f"... and {len(thmbnailanch) - 10} more images"
                    break
                    
                try:
                    imgdata = client.get(ref.attrs["href"])
                    if not imgdata.status_code == 200:
                        time.sleep(2)
                        continue
                        
                    imghtml = BeautifulSoup(imgdata.text, "html.parser")
                    downloadanch = imghtml.find(attrs={"class": "btn-download"})
                    
                    if downloadanch and downloadanch.attrs.get("href"):
                        currentimg = downloadanch.attrs["href"].replace(" ", "%20")
                        dl_msg += f"{count}. {currentimg}\n"
                        count += 1
                except:
                    continue
                    
            return dl_msg if dl_msg else "No images found in Pixl album"
        else:
            # Handle single image
            downloadanch = soup.find(attrs={"class": "btn-download"})
            if downloadanch and downloadanch.attrs.get("href"):
                return downloadanch.attrs["href"].replace(" ", "%20")
            else:
                return "Could not find download link for Pixl image"

    except Exception as e:
        return f"Error bypassing Pixl: {str(e)}"

# Common export function name
process_url = pixl_bypass
