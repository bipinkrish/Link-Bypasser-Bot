"""Filepress direct link generator module"""

from urllib.parse import urlparse

try:
    from cloudscraper import create_scraper
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    # Fallback imports to prevent import errors
    create_scraper = None

SITE_NAME = "Filepress"
URL_PATTERNS = [r"filepress\."]

def process_url(url: str) -> str:
    """Generate direct download link for Filepress URLs
    
    Provides both Google Drive and Telegram download options
    
    Args:
        url: Filepress URL
        
    Returns:
        Direct download links or error message
    """
    if not DEPENDENCIES_AVAILABLE:
        return "ERROR: Required dependencies (cloudscraper) not available"
    
    cget = create_scraper().request
    
    try:
        url = cget("GET", url).url
        raw = urlparse(url)

        gd_data = {
            "id": raw.path.split("/")[-1],
            "method": "publicDownlaod",
        }
        tg_data = {
            "id": raw.path.split("/")[-1],
            "method": "telegramDownload",
        }

        api = f"{raw.scheme}://{raw.hostname}/api/file/downlaod/"

        gd_res = cget(
            "POST",
            api,
            headers={"Referer": f"{raw.scheme}://{raw.hostname}"},
            json=gd_data,
        ).json()
        tg_res = cget(
            "POST",
            api,
            headers={"Referer": f"{raw.scheme}://{raw.hostname}"},
            json=tg_data,
        ).json()

    except Exception as e:
        return f"Google Drive: ERROR: {e.__class__.__name__} \nTelegram: ERROR: {e.__class__.__name__}"

    gd_result = (
        f'https://drive.google.com/uc?id={gd_res["data"]}'
        if "data" in gd_res
        else f'ERROR: {gd_res["statusText"]}'
    )
    tg_result = (
        f'https://tghub.xyz/?start={tg_res["data"]}'
        if "data" in tg_res
        else "No Telegram file available "
    )

    return f"Google Drive: {gd_result} \nTelegram: {tg_result}"
