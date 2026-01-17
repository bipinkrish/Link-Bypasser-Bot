"""1Fichier direct link generator module"""

from re import match

try:
    from cloudscraper import create_scraper
    from bs4 import BeautifulSoup
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    # Fallback imports to prevent import errors
    create_scraper = None
    BeautifulSoup = None

SITE_NAME = "1Fichier"
URL_PATTERNS = [r"1fichier\.com"]

def process_url(link: str) -> str:
    """Generate direct download link for 1Fichier URLs
    
    Based on https://github.com/Maujar
    Supports password-protected links with :: separator
    
    Args:
        link: 1Fichier URL (optionally with password: url::password)
        
    Returns:
        Direct download link or error message
    """
    if not DEPENDENCIES_AVAILABLE:
        return "ERROR: Required dependencies (cloudscraper, beautifulsoup4) not available"
    
    regex = r"^([http:\/\/|https:\/\/]+)?.*1fichier\.com\/\?.+"
    gan = match(regex, link)
    if not gan:
        return "ERROR: The link you entered is wrong!"
    
    # Parse password from link if present
    if "::" in link:
        pswd = link.split("::")[-1]
        url = link.split("::")[-2]
    else:
        pswd = None
        url = link
        
    cget = create_scraper().request
    
    try:
        if pswd is None:
            req = cget("post", url)
        else:
            pw = {"pass": pswd}
            req = cget("post", url, data=pw)
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
        
    if req.status_code == 404:
        return "ERROR: File not found/The link you entered is wrong!"
        
    soup = BeautifulSoup(req.content, "lxml")
    
    # Check for direct download button
    if soup.find("a", {"class": "ok btn-general btn-orange"}):
        dl_url = soup.find("a", {"class": "ok btn-general btn-orange"})["href"]
        if dl_url:
            return dl_url
        return "ERROR: Unable to generate Direct Link 1fichier!"
        
    # Handle warnings and errors
    warnings = soup.find_all("div", {"class": "ct_warn"})
    
    if len(warnings) == 3:
        str_2 = warnings[-1]
        warning_text = str(str_2).lower()
        
        if "you must wait" in warning_text:
            numbers = [int(word) for word in str(str_2).split() if word.isdigit()]
            if numbers:
                return f"ERROR: 1fichier is on a limit. Please wait {numbers[0]} minute."
            else:
                return "ERROR: 1fichier is on a limit. Please wait a few minutes/hour."
        elif "protect access" in warning_text:
            return ("ERROR: This link requires a password!\n\n"
                   "<b>This link requires a password!</b>\n"
                   "- Insert sign <b>::</b> after the link and write the password after the sign.\n\n"
                   "<b>Example:</b> https://1fichier.com/?smmtd8twfpm66awbqz04::love you\n\n"
                   "* No spaces between the signs <b>::</b>\n"
                   "* For the password, you can use a space!")
        else:
            return "ERROR: Failed to generate Direct Link from 1fichier!"
            
    elif len(warnings) == 4:
        str_1 = warnings[-2]
        str_3 = warnings[-1]
        
        if "you must wait" in str(str_1).lower():
            numbers = [int(word) for word in str(str_1).split() if word.isdigit()]
            if numbers:
                return f"ERROR: 1fichier is on a limit. Please wait {numbers[0]} minute."
            else:
                return "ERROR: 1fichier is on a limit. Please wait a few minutes/hour."
        elif "bad password" in str(str_3).lower():
            return "ERROR: The password you entered is wrong!"
        else:
            return "ERROR: Error trying to generate Direct Link from 1fichier!"
    else:
        return "ERROR: Error trying to generate Direct Link from 1fichier!"
