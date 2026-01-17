"""
Multi-site scraper bypasser
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

# Site configuration
SITE_NAME = "Scrappers"
URL_PATTERNS = [
    r'sharespark\.',
    r'htpmovies\.',
    r'cinevood\.',
    r'atishmkv\.',
    r'teluguflix\.',
    r'taemovies\.',
    r'toonworld4all\.',
    r'animeremux\.'
]

def scrappers_bypass(link):
    """
    Multi-site scraper for various movie/content sites
    """
    try:
        # Validate link format
        try:
            link = re.match(
                r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*",
                link,
            )[0]
        except (TypeError, AttributeError):
            return "Not a Valid Link."

        if "htpmovies" in link and "/exit.php" in link:
            # Handle direct exit links
            return f"HTMovies exit link: {link}"
            
        elif "teluguflix" in link:
            gd_txt = ""
            r = requests.get(link)
            soup = BeautifulSoup(r.text, "html.parser")
            links = soup.select('a[href*="gdtot"]')
            gd_txt = f"Total Links Found : {len(links)}\n\n"
            
            for no, link_elem in enumerate(links[:10], start=1):  # Limit to 10
                gdlk = link_elem["href"]
                try:
                    t = requests.get(gdlk, timeout=10)
                    soupt = BeautifulSoup(t.text, "html.parser")
                    title = soupt.select('meta[property^="og:description"]')
                    title_text = title[0]['content'].replace('Download ', '') if title else "Unknown"
                    gd_txt += f"{no}. {title_text}\n{gdlk}\n\n"
                except:
                    gd_txt += f"{no}. {gdlk}\n\n"
                    
            return gd_txt
            
        elif "atishmkv" in link:
            prsd = ""
            r = requests.get(link)
            soup = BeautifulSoup(r.text, "html.parser")
            x = soup.select('a[href^="https://gdflix.top/file"]')
            
            for a in x:
                prsd += a["href"] + "\n\n"
            return prsd if prsd else "No GDFlix links found"
            
        else:
            # Generic magnet link extractor
            res = requests.get(link)
            soup = BeautifulSoup(res.text, "html.parser")
            magnet_links = soup.select(r'a[href^="magnet:?xt=urn:btih:"]')
            
            if magnet_links:
                links = [hy["href"] for hy in magnet_links]
                return "\n\n".join(links)
            else:
                return f"No supported content found for: {link}"

    except Exception as e:
        return f"Error scraping site: {str(e)}"

# Common export function name
process_url = scrappers_bypass
