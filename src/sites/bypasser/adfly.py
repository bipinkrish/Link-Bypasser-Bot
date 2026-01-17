"""
Adfly bypasser
"""

import re
import base64
import cloudscraper
from urllib.parse import unquote

# Site configuration
SITE_NAME = "Adfly"
URL_PATTERNS = [
    r'adf\.ly/',
    r'adfly\.com/',
    r'j\.gs/',
    r'adfoc\.us/'
]

def decrypt_url(code):
    """
    Decrypt Adfly URL using original algorithm
    """
    a, b = "", ""
    for i in range(0, len(code)):
        if i % 2 == 0:
            a += code[i]
        else:
            b = code[i] + b
    key = list(a + b)
    i = 0
    while i < len(key):
        if key[i].isdigit():
            for j in range(i + 1, len(key)):
                if key[j].isdigit():
                    u = int(key[i]) ^ int(key[j])
                    if u < 10:
                        key[i] = str(u)
                    i = j
                    break
        i += 1
    key = "".join(key)
    try:
        decrypted = base64.b64decode(key)[16:-16]
        return decrypted.decode("utf-8")
    except:
        return None

def adfly_bypass(url):
    """
    Bypass Adfly short links using original algorithm
    """
    try:
        client = cloudscraper.create_scraper(allow_brotli=False)
        res = client.get(url).text
        
        try:
            ysmm = re.findall(r"ysmm\s*=\s*['\"](.*?)['\"]", res)[0]
        except:
            return f"Error: Could not find Adfly decryption key in {url}"
            
        decoded_url = decrypt_url(ysmm)
        if not decoded_url:
            return f"Error: Failed to decrypt Adfly URL"
            
        if re.search(r"go\.php\?u=", decoded_url):
            decoded_url = base64.b64decode(re.sub(r"(.*?)u=", "", decoded_url)).decode()
        elif "&dest=" in decoded_url:
            decoded_url = unquote(re.sub(r"(.*?)dest=", "", decoded_url))
            
        return decoded_url

    except Exception as e:
        return f"Error bypassing Adfly: {str(e)}"

# Common export function name
process_url = adfly_bypass
