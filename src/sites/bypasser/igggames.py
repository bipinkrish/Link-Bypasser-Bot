"""IGG-Games URL bypasser module"""

import requests

try:
    from bs4 import BeautifulSoup
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    BeautifulSoup = None

SITE_NAME = "IGG-Games"
URL_PATTERNS = [r"igg-games\.com"]

def bypassBluemediafiles(url, torrent=False):
    """Helper function to bypass bluemediafiles"""
    try:
        if torrent:
            # Handle torrent links differently if needed
            return url
        return url  # Simplified for now
    except Exception:
        return url

def process_url(url: str) -> str:
    """Extract download links from IGG-Games pages
    
    Args:
        url: IGG-Games URL
        
    Returns:
        Formatted download links or error message
    """
    if not DEPENDENCIES_AVAILABLE:
        return "ERROR: Required dependencies (beautifulsoup4) not available"
    
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        soup = soup.find("div", class_="uk-margin-medium-top").findAll("a")

        bluelist = []
        for ele in soup:
            bluelist.append(ele.get("href"))
        bluelist = bluelist[3:-1]

        links = ""
        last = None
        fix = True
        
        for ele in bluelist:
            if ele == "https://igg-games.com/how-to-install-a-pc-game-and-update.html":
                fix = False
                links += "\\n"
            if "bluemediafile" in ele:
                tmp = bypassBluemediafiles(ele)
                if fix:
                    tt = tmp.split("/")[2]
                    if last is not None and tt != last:
                        links += "\\n"
                    last = tt
                links = links + "○ " + tmp + "\\n"
            elif "pcgamestorrents.com" in ele:
                res = requests.get(ele)
                soup = BeautifulSoup(res.text, "html.parser")
                turl = (
                    soup.find(
                        "p", class_="uk-card uk-card-body uk-card-default uk-card-hover"
                    )
                    .find("a")
                    .get("href")
                )
                links = links + "🧲 `" + bypassBluemediafiles(turl, True) + "`\\n\\n"
            elif ele != "https://igg-games.com/how-to-install-a-pc-game-and-update.html":
                if fix:
                    tt = ele.split("/")[2]
                    if last is not None and tt != last:
                        links += "\\n"
                    last = tt
                links = links + "○ " + ele + "\\n"

        return links[:-1] if links else "ERROR: No download links found"
        
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
