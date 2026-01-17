"""VNShortener URL bypasser module"""

import time
import requests

try:
    from bs4 import BeautifulSoup
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    BeautifulSoup = None

SITE_NAME = "VNShortener"
URL_PATTERNS = [r"vnshortener\."]

def process_url(url: str) -> str:
    """Bypass VNShortener shortened URLs
    
    Args:
        url: VNShortener shortened URL
        
    Returns:
        Original URL or error message
    """
    if not DEPENDENCIES_AVAILABLE:
        return "ERROR: Required dependencies (beautifulsoup4) not available"
    
    try:
        sess = requests.session()
        DOMAIN = "https://vnshortener.com/"
        org = "https://nishankhatri.xyz"
        PhpAcc = DOMAIN + "link/new.php"
        ref = "https://nishankhatri.com.np/"
        go = DOMAIN + "links/go"

        code = url.split("/")[3]
        final_url = f"{DOMAIN}/{code}/"
        headers = {"authority": DOMAIN, "origin": org}

        data = {
            "step_1": code,
        }
        response = sess.post(PhpAcc, headers=headers, data=data).json()
        id = response["inserted_data"]["id"]
        
        data = {
            "step_2": code,
            "id": id,
        }
        response = sess.post(PhpAcc, headers=headers, data=data).json()

        headers["referer"] = ref
        params = {"sid": str(id)}
        resp = sess.get(final_url, params=params, headers=headers)
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs}

        time.sleep(1)
        headers["x-requested-with"] = "XMLHttpRequest"
        
        r = sess.post(go, data=data, headers=headers).json()
        if r["status"] == "success":
            return r["url"]
        else:
            return "ERROR: Failed to bypass"
            
    except Exception:
        return "Something went wrong :("
