"""GDrive look-alike sites unified bypasser module"""

import re
from urllib.parse import urlparse

try:
    import cloudscraper
    from lxml import etree
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    cloudscraper = None
    etree = None

SITE_NAME = "GDrive Family"
URL_PATTERNS = [
    r"appdrive\.", r"driveapp\.", r"drivehub\.", r"gdflix\.", r"drivesharer\.",
    r"drivebit\.", r"drivelinks\.", r"driveace\.", r"drivepro\.", r"driveseed\."
]

def process_url(url: str) -> str:
    """Bypass GDrive look-alike sites to get direct Google Drive links
    
    Unified function that handles multiple GDrive clone sites with login
    
    Args:
        url: GDrive look-alike URL (appdrive, driveapp, etc.)
        
    Returns:
        Direct Google Drive link or error message
    """
    if not DEPENDENCIES_AVAILABLE:
        return "ERROR: Required dependencies (cloudscraper, lxml) not available"
    
    try:
        # Default account credentials  
        Email = "chzeesha4@gmail.com"
        Password = "zeeshi#789"
        
        account = {"email": Email, "passwd": Password}
        client = cloudscraper.create_scraper(allow_brotli=False)
        client.headers.update({
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        })
        
        # Login to the site
        data = {"email": account["email"], "password": account["passwd"]}
        client.post(f"https://{urlparse(url).netloc}/login", data=data)
        
        # Get the main page
        res = client.get(url)
        key = re.findall('"key",\\s+"(.*?)"', res.text)[0]
        ddl_btn = etree.HTML(res.content).xpath("//button[@id='drc']")
        
        # Parse file info
        info = re.findall(">(.*?)<\\/li>", res.text)
        info_parsed = {}
        for item in info:
            kv = [s.strip() for s in item.split(": ", maxsplit=1)]
            if len(kv) == 2:
                info_parsed[kv[0].lower()] = kv[1]
                
        info_parsed["error"] = False
        info_parsed["link_type"] = "login"
        
        # Prepare request data
        headers = {
            "Content-Type": f"multipart/form-data; boundary={'-'*4}_",
        }
        data = {"type": 1, "key": key, "action": "original"}
        
        if len(ddl_btn):
            info_parsed["link_type"] = "direct"
            data["action"] = "direct"
            
        # Try to get the download link
        while data["type"] <= 3:
            boundary = f'{"-"*6}_'
            data_string = ""
            for item in data:
                data_string += f"{boundary}\\r\\n"
                data_string += f'Content-Disposition: form-data; name="{item}"\\r\\n\\r\\n{data[item]}\\r\\n'
            data_string += f"{boundary}--\\r\\n"
            gen_payload = data_string
            
            try:
                response = client.post(url, data=gen_payload, headers=headers).json()
                break
            except Exception:
                data["type"] += 1
                
        if "url" in response:
            info_parsed["gdrive_link"] = response["url"]
        elif "error" in response and response["error"]:
            info_parsed["error"] = True
            info_parsed["error_message"] = response["message"]
        else:
            info_parsed["error"] = True
            info_parsed["error_message"] = "Something went wrong :("
            
        if info_parsed["error"]:
            return f"ERROR: {info_parsed.get('error_message', 'Unknown error')}"
            
        # Site-specific post-processing
        netloc = urlparse(url).netloc.lower()
        
        if any(site in netloc for site in ["driveapp", "drivehub", "gdflix", "drivesharer", "drivebit", "drivelinks", "driveace", "drivepro"]):
            res = client.get(info_parsed["gdrive_link"])
            try:
                drive_link = etree.HTML(res.content).xpath("//a[contains(@class,'btn')]/@href")[0]
                info_parsed["gdrive_link"] = drive_link
            except (IndexError, TypeError):
                pass  # Keep original link if parsing fails
                
        return info_parsed["gdrive_link"]
        
    except Exception as e:
        return f"ERROR: Unable to Extract GDrive Link - {e.__class__.__name__}"
