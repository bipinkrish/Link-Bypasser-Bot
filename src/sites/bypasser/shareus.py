"""
ShareUs bypasser
"""

import requests

# Site configuration
SITE_NAME = "ShareUs"
URL_PATTERNS = [
    r'shareus\.io/'
]

def shareus_bypass(url):
    """
    Bypass ShareUs short links
    """
    try:
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }
        DOMAIN = "https://us-central1-my-apps-server.cloudfunctions.net"
        sess = requests.session()

        code = url.split("/")[-1]
        params = {
            "shortid": code,
            "initial": "true",
            "referrer": "https://shareus.io/",
        }
        response = requests.get(f"{DOMAIN}/v", params=params, headers=headers)

        for i in range(1, 4):
            json_data = {
                "current_page": i,
            }
            response = sess.post(f"{DOMAIN}/v", headers=headers, json=json_data)

        response = sess.get(f"{DOMAIN}/get_link", headers=headers).json()
        return response["link_info"]["destination"]

    except Exception as e:
        return f"Error bypassing ShareUs: {str(e)}"

# Common export function name
process_url = shareus_bypass
