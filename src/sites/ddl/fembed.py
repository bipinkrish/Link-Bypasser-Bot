"""Fembed video streaming direct link generator module"""

from re import search
from requests import session

SITE_NAME = "Fembed Family"
URL_PATTERNS = [
    r"fembed\.", r"layarkacaxxi\.", r"femax20\.", r"fcdn\.", r"feurl\.",
    r"naniplay\.", r"nanime\.", r"mm9842\."
]

def process_url(link: str) -> str:
    """Generate direct download link for Fembed URLs
    
    Args:
        link: Fembed video URL
        
    Returns:
        Direct download link (highest quality) or error message
    """
    sess = session()
    
    try:
        url = link.replace("/v/", "/f/")
        raw = sess.get(url)
        api = search(r"(/api/source/[^\"']+)", raw.text)
        
        if api is not None:
            result = {}
            raw = sess.post("https://layarkacaxxi.icu" + api.group(1)).json()
            
            for d in raw["data"]:
                f = d["file"]
                head = sess.head(f)
                direct = head.headers.get("Location", f)
                result[f"{d['label']}/{d['type']}"] = direct
                
            dl_url = result
            
            if dl_url:
                # Return the last (usually highest quality) link
                count = len(dl_url)
                lst_link = [dl_url[i] for i in dl_url]
                return lst_link[count - 1]
            else:
                return "ERROR: No download links found"
        else:
            return "ERROR: API endpoint not found"
            
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
