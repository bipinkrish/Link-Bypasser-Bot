#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sirigan bypasser
Decodes base64-encoded URLs from sirigan links

Site: sirigan (general base64 decoder)
Method: Recursive base64 decoding
"""

import base64

# Site configuration
SITE_NAME = "sirigan"
URL_PATTERNS = [
    r'sirigan\.',
    r'base64'  # Generic pattern for base64-encoded URLs
]

def process_url(url: str) -> str:
    """
    Decode sirigan base64-encoded URLs
    
    Args:
        url: Sirigan or base64-encoded URL
        
    Returns:
        Decoded URL or error message
    """
    try:
        # Extract the encoded part after the = sign
        url = url.split("=", maxsplit=1)[-1]

        # Recursively decode base64 until no more decoding possible
        while True:
            try:
                decoded = base64.b64decode(url).decode("utf-8")
                url = decoded
            except:
                break

        # Extract final URL if it contains url= parameter
        final_url = url.split("url=")[-1]
        return final_url
        
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
