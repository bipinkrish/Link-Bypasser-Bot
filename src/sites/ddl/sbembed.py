"""SBEmbed video streaming direct link generator module"""

from re import compile, findall
from requests import session

try:
    from bs4 import BeautifulSoup
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    BeautifulSoup = None

SITE_NAME = "SBEmbed Family"
URL_PATTERNS = [r"sbembed\.", r"tubesb\.", r"watchsb\.", r"streamsb\.", r"sbplay\."]

def process_url(link: str) -> str:
    """Generate direct download link for SBEmbed URLs
    
    Args:
        link: SBEmbed video URL
        
    Returns:
        Direct download link (highest quality) or error message
    """
    if not DEPENDENCIES_AVAILABLE:
        return "ERROR: Required dependencies (beautifulsoup4) not available"
    
    sess = session()
    
    try:
        raw = sess.get(link)
        soup = BeautifulSoup(raw.text, "html.parser")

        result = {}
        for a in soup.findAll("a", onclick=compile(r"^download_video[^>]+")):
            data = dict(
                zip(
                    ["id", "mode", "hash"],
                    findall(r"[\"']([^\"']+)[\"']", a["onclick"]),
                )
            )
            data["op"] = "download_orig"

            raw = sess.get("https://sbembed.com/dl", params=data)
            soup = BeautifulSoup(raw.text, "html.parser")

            if direct := soup.find("a", text=compile("(?i)^direct")):
                result[a.text] = direct["href"]
                
        dl_url = result

        if dl_url:
            # Return the last (usually highest quality) link
            count = len(dl_url)
            lst_link = [dl_url[i] for i in dl_url]
            return lst_link[count - 1]
        else:
            return "ERROR: No download links found"

    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
