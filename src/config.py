"""
Dynamic configuration system that auto-discovers site modules
Scans sites/ directory and builds CONFIG_LIST from module metadata
"""

import re
import importlib.util
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Auto-discovered configuration list
CONFIG_LIST = []

def discover_and_load_sites():
    """
    Dynamically discover and load site modules from their directories
    """
    global CONFIG_LIST
    CONFIG_LIST.clear()
    
    src_dir = Path(__file__).parent
    sites_dir = src_dir / "sites"
    
    if not sites_dir.exists():
        logger.warning(f"Sites directory not found: {sites_dir}")
        return
    
    # Load sites from each category
    categories = {
        'bypasser': sites_dir / 'bypasser',
        'ddl': sites_dir / 'ddl',
        'freewall': sites_dir / 'freewall'
    }
    
    for category, category_dir in categories.items():
        if not category_dir.exists():
            continue
            
        for py_file in category_dir.glob("*.py"):
            if py_file.name in ['__init__.py']:
                continue
                
            try:
                # Load the module
                module_name = py_file.stem
                spec = importlib.util.spec_from_file_location(f"{category}_{module_name}", py_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check if module has required attributes
                if not (hasattr(module, 'SITE_NAME') and hasattr(module, 'URL_PATTERNS') and hasattr(module, 'process_url')):
                    logger.warning(f"Module {py_file} missing required attributes (SITE_NAME, URL_PATTERNS, process_url)")
                    continue
                
                # Add each URL pattern as a separate config entry
                for pattern in module.URL_PATTERNS:
                    CONFIG_LIST.append({
                        'name': module.SITE_NAME.lower().replace(' ', '_'),
                        'display_name': module.SITE_NAME,
                        'type': category,
                        'url_regex': pattern,
                        'callback_function': module.process_url,
                        'module_file': str(py_file.relative_to(src_dir))
                    })
                
                logger.info(f"Loaded {category} module: {module.SITE_NAME} ({len(module.URL_PATTERNS)} patterns)")
                
            except Exception as e:
                logger.error(f"Failed to load {category} module {py_file}: {e}")
                
                # Add a fallback entry so it shows in lists
                CONFIG_LIST.append({
                    'name': py_file.stem,
                    'display_name': py_file.stem.title(),
                    'type': category,
                    'url_regex': f'.*{py_file.stem}.*',
                    'callback_function': lambda url, err=str(e): f"Module {py_file.stem} failed to load: {err}",
                    'module_file': str(py_file.relative_to(src_dir))
                })

def get_function_by_url(url):
    """Get the appropriate function for a URL"""
    for item in CONFIG_LIST:
        if re.search(item['url_regex'], url, re.IGNORECASE):
            return item['callback_function']
    return None

def get_sites_by_type(site_type):
    """Get all site names of a specific type"""
    seen = set()
    result = []
    for item in CONFIG_LIST:
        if item['type'] == site_type and item['display_name'] not in seen:
            seen.add(item['display_name'])
            result.append(item['display_name'])
    return result

def get_all_site_names():
    """Get all site names grouped by type"""
    return {
        'bypasser': get_sites_by_type('bypasser'),
        'ddl': get_sites_by_type('ddl'),
        'freewall': get_sites_by_type('freewall')
    }

def get_config_stats():
    """Get statistics about the configuration"""
    unique_sites = {}
    for item in CONFIG_LIST:
        site_type = item['type']
        display_name = item['display_name']
        if site_type not in unique_sites:
            unique_sites[site_type] = set()
        unique_sites[site_type].add(display_name)
    
    stats = {
        'total': sum(len(sites) for sites in unique_sites.values()),
        'bypasser': len(unique_sites.get('bypasser', set())),
        'ddl': len(unique_sites.get('ddl', set())),
        'freewall': len(unique_sites.get('freewall', set())),
        'total_patterns': len(CONFIG_LIST)
    }
    return stats

def reload_sites():
    """Reload all site modules (useful for development)"""
    discover_and_load_sites()
    return get_config_stats()

# Initialize on import
discover_and_load_sites()

# Print loading summary
stats = get_config_stats()
print(f"✅ Auto-discovered {stats['total']} sites with {stats['total_patterns']} URL patterns:")
print(f"   - Bypassers: {stats['bypasser']} sites")
print(f"   - DDL: {stats['ddl']} sites")  
print(f"   - Freewall: {stats['freewall']} sites")
