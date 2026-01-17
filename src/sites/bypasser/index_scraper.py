#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Index scraper
Scrapes index links with authentication

Site: Index directories
Method: Authenticated API requests with token pagination
"""

import base64
import json
from urllib.parse import quote

try:
    import requests
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False

# Site configuration
SITE_NAME = "index_scraper"
URL_PATTERNS = [
    r'index',  # Generic pattern for index links
    r'directory'
]

def authorization_token(username, password):
    """Generate authorization token for index access"""
    user_pass = f"{username}:{password}"
    return f"Basic {base64.b64encode(user_pass.encode()).decode()}"

def decrypt(string):
    """Decrypt index response"""
    return base64.b64decode(string[::-1][24:-20]).decode("utf-8")

def process_url(url: str, username="none", password="none") -> str:
    """
    Scrape index directory
    
    Args:
        url: Index directory URL
        username: Authentication username
        password: Authentication password
        
    Returns:
        Formatted file listing or error message
    """
    if not SCRAPER_AVAILABLE:
        return "ERROR: requests module not available"
    
    def func(payload_input, url, username, password):
        next_page = False
        next_page_token = ""

        url = f"{url}/" if url[-1] != "/" else url

        try:
            headers = {"authorization": authorization_token(username, password)}
        except:
            return "username/password combination is wrong", None, None

        encrypted_response = requests.post(url, data=payload_input, headers=headers)
        if encrypted_response.status_code == 401:
            return "username/password combination is wrong", None, None

        try:
            decrypted_response = json.loads(decrypt(encrypted_response.text))
        except:
            return (
                "something went wrong. check index link/username/password field again",
                None,
                None,
            )

        page_token = decrypted_response["nextPageToken"]
        if page_token is None:
            next_page = False
        else:
            next_page = True
            next_page_token = page_token

        if list(decrypted_response.get("data").keys())[0] != "error":
            file_length = len(decrypted_response["data"]["files"])
            result = ""

            for i, _ in enumerate(range(file_length)):
                files_type = decrypted_response["data"]["files"][i]["mimeType"]
                if files_type != "application/vnd.google-apps.folder":
                    files_name = decrypted_response["data"]["files"][i]["name"]
                    direct_download_link = url + quote(files_name)
                    result += f"• {files_name} :\n{direct_download_link}\n\n"
            return result, next_page, next_page_token

    def format_results(result):
        long_string = "".join(result)
        new_list = []

        while len(long_string) > 0:
            if len(long_string) > 4000:
                split_index = long_string.rfind("\n\n", 0, 4000)
                if split_index == -1:
                    split_index = 4000
            else:
                split_index = len(long_string)

            new_list.append(long_string[:split_index])
            long_string = long_string[split_index:].lstrip("\n\n")

        return new_list

    try:
        # Main processing
        x = 0
        next_page = False
        next_page_token = ""
        result = []

        payload = {"page_token": next_page_token, "page_index": x}
        temp, next_page, next_page_token = func(payload, url, username, password)
        if temp is not None:
            result.append(temp)

        while next_page == True:
            payload = {"page_token": next_page_token, "page_index": x}
            temp, next_page, next_page_token = func(payload, url, username, password)
            if temp is not None:
                result.append(temp)
            x += 1

        if len(result) == 0:
            return "ERROR: No files found in index"
        
        formatted_results = format_results(result)
        return "\n".join(formatted_results)
        
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
