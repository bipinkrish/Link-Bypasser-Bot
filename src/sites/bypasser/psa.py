"""
PSA bypasser
"""

import requests
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "PSA"
URL_PATTERNS = [
    r'psa\.wf/',
    r'psa\.pm/'
]

def psa_bypass(psa_url):
    """
    Bypass PSA (Protected Shortened URLs)
    """
    try:
        headers = {
            "authority": "psa.wf",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "referer": "https://psa.wf/",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        }

        r = requests.get(psa_url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Find protected content boxes
        content_boxes = soup.find_all(
            class_="dropshadowboxes-drop-shadow dropshadowboxes-rounded-corners dropshadowboxes-inside-and-outside-shadow dropshadowboxes-lifted-both dropshadowboxes-effect-default"
        )
        
        if not content_boxes:
            return "No protected content found in PSA link"
        
        links = []
        for link in content_boxes:
            try:
                exit_gate = link.a.get("href")
                if "/exit" in exit_gate:
                    # Extract the actual URL from exit gate
                    if "url=" in exit_gate:
                        actual_url = exit_gate.split("url=")[-1]
                        links.append(actual_url)
                    else:
                        links.append(exit_gate)
            except:
                pass

        if not links:
            return "No extractable links found in PSA content"

        # Format the result
        result = f"PSA Content ({len(links)} links found):\n\n"
        for i, link in enumerate(links, 1):
            result += f"{i}. {link}\n"
            
        return result

    except Exception as e:
        return f"Error bypassing PSA: {str(e)}"

# Common export function name
process_url = psa_bypass
