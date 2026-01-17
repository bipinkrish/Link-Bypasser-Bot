"""
Dropbox direct download link generator
"""

# Site configuration
SITE_NAME = "Dropbox"
URL_PATTERNS = [
    r'dropbox\.com/',
    r'db\.tt/'
]

def dropbox_bypass(url):
    """
    Convert Dropbox share links to direct download links
    """
    try:
        # Simple URL transformation for Dropbox
        direct_url = (
            url.replace("www.", "")
            .replace("dropbox.com", "dl.dropboxusercontent.com")
            .replace("?dl=0", "")
            .replace("?dl=1", "")
        )
        
        # Ensure it ends with ?dl=1 for direct download
        if "?" not in direct_url:
            direct_url += "?dl=1"
        elif "dl=" not in direct_url:
            direct_url += "&dl=1"
            
        return direct_url

    except Exception as e:
        return f"Error processing Dropbox: {str(e)}"

# Common export function name
process_url = dropbox_bypass
