from flask import Flask, request, render_template, make_response, send_file
import re
import os
import sys

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import new simple config system
from config import CONFIG_LIST, get_function_by_url

app = Flask(__name__)

def get_bypasser_type(url):
    """Determine bypasser type for a URL"""
    for config in CONFIG_LIST:
        if re.search(config['url_regex'], url, re.IGNORECASE):
            return config['type']
    return 'bypasser'  # default

def loop_thread(url):
    """Main processing function for URLs"""
    if not url:
        return None

    try:
        # Get the appropriate function for this URL
        func = get_function_by_url(url)
        if func:
            result = func(url)
        else:
            return "No handler found for this URL"
        
        # Handle file download for freewall sites
        if get_bypasser_type(url) == 'freewall' and result and os.path.exists(result):
            try:
                return send_file(result)
            except:
                pass
        
        if result:
            return str(result)
        else:
            return "Unable to bypass this URL"
            
    except Exception as e:
        return f"**Error**: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def home():
    # Get site data for template
    from config import get_all_site_names
    sites = get_all_site_names()
    
    bypasser_sites = sorted(sites.get('bypasser', []))
    ddl_sites = sorted(sites.get('ddl', []))
    freewall_sites = sorted(sites.get('freewall', []))
    
    result = None
    
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            result = loop_thread(url)
    
    return render_template("index.html", 
                         bypasser_sites=bypasser_sites,
                         ddl_sites=ddl_sites,
                         freewall_sites=freewall_sites,
                         result=result)

@app.route("/bypass", methods=["GET", "POST"])
def short():
    if request.method == "POST":
        url = request.form.get("url")
        resp = make_response(loop_thread(url))
        resp.headers["Content-Type"] = "text/plain; charset=utf-8"
        return resp
    elif request.method == "GET":
        url = request.args.get("url")
        resp = make_response(loop_thread(url))
        resp.headers["Content-Type"] = "text/plain; charset=utf-8"
        return resp

@app.route("/api/bypass")
def short_api():
    """API endpoint for URL bypassing"""
    url = request.args.get("url")
    try:
        result = loop_thread(url)
        return {
            "success": True,
            "result": result,
            "message": "Successfully bypassed"
        }
    except Exception as e:
        return {
            "success": False,
            "result": None,
            "message": str(e)
        }

@app.route("/supported")
def supported_sites():
    """Return list of supported sites"""
    supported = {
        'bypasser': [],
        'ddl': [], 
        'freewall': []
    }
    
    for config in CONFIG_LIST:
        # Extract domain from regex for display
        domain_match = re.search(r'([a-zA-Z0-9-]+\.[a-zA-Z]{2,})', config['url_regex'])
        domain = domain_match.group(1) if domain_match else config['url_regex']
        
        site_info = {
            'domain': domain,
            'regex': config['url_regex'],
            'function': config['callback_function'].__name__ if callable(config['callback_function']) else str(config['callback_function'])
        }
        
        if config['type'] in supported:
            supported[config['type']].append(site_info)
    
    return {
        "success": True,
        "supported_sites": supported,
        "total_configs": len(CONFIG_LIST)
    }

@app.route("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "total_configs": len(CONFIG_LIST),
        "bypasser_types": ["bypasser", "ddl", "freewall"]
    }

@app.route("/config")
def show_config():
    """Show current configuration (for debugging)"""
    config_info = []
    for i, config in enumerate(CONFIG_LIST):
        config_info.append({
            "id": i,
            "type": config['type'],
            "regex": config['url_regex'],
            "function": config['callback_function'].__name__ if callable(config['callback_function']) else str(config['callback_function'])
        })
    
    return {
        "success": True,
        "configs": config_info,
        "total": len(CONFIG_LIST)
    }

if __name__ == "__main__":
    print("🚀 Starting Flask app with new configuration system...")
    print(f"📋 Loaded {len(CONFIG_LIST)} bypasser configurations")
    
    # Show summary of config types
    type_counts = {}
    for config in CONFIG_LIST:
        type_counts[config['type']] = type_counts.get(config['type'], 0) + 1
    
    for bypass_type, count in type_counts.items():
        print(f"   {bypass_type}: {count} sites")
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
