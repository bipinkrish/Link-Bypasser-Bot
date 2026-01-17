"""
Krakenfiles direct download link generator
"""

import requests
from lxml import etree

# Site configuration
SITE_NAME = "Krakenfiles"
URL_PATTERNS = [
    r'krakenfiles\.com/'
]

def krakenfiles_bypass(url):
    """
    Generate direct download link for Krakenfiles
    """
    try:
        sess = requests.session()
        
        try:
            res = sess.get(url)
            html = etree.HTML(res.text)
            
            # Find the form action URL
            post_url_list = html.xpath('//form[@id="dl-form"]/@action')
            if post_url_list:
                post_url = f"https:{post_url_list[0]}"
            else:
                sess.close()
                return "ERROR: Unable to find post link on Krakenfiles."
                
            # Find the token
            token_list = html.xpath('//input[@id="dl-token"]/@value')
            if token_list:
                data = {"token": token_list[0]}
            else:
                sess.close()
                return "ERROR: Unable to find token for Krakenfiles."
                
        except Exception as e:
            sess.close()
            return f"ERROR: {e.__class__.__name__} while parsing Krakenfiles page"

        try:
            dl_response = sess.post(post_url, data=data).json()
            return dl_response["url"]
        except Exception as e:
            sess.close()
            return f"ERROR: {e.__class__.__name__} while getting Krakenfiles download link"

    except Exception as e:
        return f"Error processing Krakenfiles: {str(e)}"

# Common export function name
process_url = krakenfiles_bypass
