"""
EZ4Short bypasser
"""

import requests
import re
import time
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "EZ4Short"
URL_PATTERNS = [
    r'ez4short\.com/',
    r'e-z\.host/'
]

def ez4short_bypass(url):
    """
    Bypass EZ4Short URLs
    """
    try:
        domain = 'https://ez4short.com'
        code = url.split('/')[-1]
        
        sess = requests.Session()
        h = {
            'authority': 'ez4short.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        
        resp = sess.get(url, headers=h)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Look for the form with hidden inputs
        inputs = soup.find_all('input')
        data = {inp.get('name'): inp.get('value') for inp in inputs if inp.get('name')}
        
        if 'id' in data and 'tp' in data:
            time.sleep(5)
            
            # Submit the form
            post_url = f"{domain}/links/go"
            h['x-requested-with'] = 'XMLHttpRequest'
            h['referer'] = url
            
            resp2 = sess.post(post_url, data=data, headers=h)
            try:
                result = resp2.json()
                if 'url' in result:
                    return result['url']
            except:
                pass
        
        return f"Could not bypass EZ4Short URL: {url}"
        
    except Exception as e:
        return f"Error bypassing EZ4Short: {str(e)}"

# Common export function name
process_url = ez4short_bypass
