"""
Dynamic text generation from configuration
Builds help text automatically from CONFIG_LIST
"""

"""
Dynamic text generation from configuration
Builds help text automatically from CONFIG_LIST
"""

def build_dynamic_text():
    """Build help text dynamically from config"""
    try:
        # Import here to avoid circular imports
        from ..config import get_all_site_names
        
        sites = get_all_site_names()
        
        # Build DDL text
        ddl_sites = sites.get('ddl', [])
        if ddl_sites:
            ddl_list = ' \n- '.join(ddl_sites)
            ddltext = f"__- {ddl_list}\n    __"
        else:
            ddltext = "__- No DDL sites configured\n    __"
        
        # Build Bypasser text (shorteners)
        bypasser_sites = sites.get('bypasser', [])
        if bypasser_sites:
            bypasser_list = ' \n- '.join(bypasser_sites)
            shortnertext = f"__- {bypasser_list}\n    __"
        else:
            shortnertext = "__- No bypasser sites configured\n    __"
        
        # Build Freewall text
        freewall_sites = sites.get('freewall', [])
        if freewall_sites:
            freewall_list = ' \n- '.join(freewall_sites)
            freewalltext = f"__- {freewall_list}\n    __"
        else:
            freewalltext = "__- No freewall sites configured\n    __"
        
        # GDrive sites are part of DDL but show separately
        gdrive_related = [site for site in ddl_sites if 'drive' in site.lower() or 'gdrive' in site.lower()]
        if not gdrive_related:
            gdrive_related = ['google_drive', 'onedrive']
        if gdrive_related:
            gdrive_list = ' \n- '.join(gdrive_related)
            gdrivetext = f"__- {gdrive_list}\n    __"
        else:
            gdrivetext = "__- No gdrive sites configured\n    __"
        
        # Others (general utilities)
        all_sites = bypasser_sites + ddl_sites + freewall_sites
        if all_sites:
            others_list = ' \n- '.join(all_sites[:5])
            otherstext = f"__- {others_list}\n    __"
        else:
            otherstext = "__- No sites configured\n    __"
        
        return ddltext, shortnertext, freewalltext, gdrivetext, otherstext
        
    except ImportError:
        # Fallback to static text if config not available
        return get_static_texts()

def get_static_texts():
    """Dynamic fallback texts from config if available"""
    try:
        # Try to get from config even in fallback mode
        from ..config import get_all_site_names
        sites = get_all_site_names()
        
        # Build from available sites
        ddl_sites = sites.get('ddl', [])
        if ddl_sites:
            ddl_list = ' \n- '.join(ddl_sites)
            ddltext = f"__- {ddl_list}\n    __"
        else:
            ddltext = "__- No DDL sites configured\n    __"
        
        bypasser_sites = sites.get('bypasser', [])
        if bypasser_sites:
            bypasser_list = ' \n- '.join(bypasser_sites)
            shortnertext = f"__- {bypasser_list}\n    __"
        else:
            shortnertext = "__- No bypasser sites configured\n    __"
        
        freewall_sites = sites.get('freewall', [])
        if freewall_sites:
            freewall_list = ' \n- '.join(freewall_sites)
            freewalltext = f"__- {freewall_list}\n    __"
        else:
            freewalltext = "__- No freewall sites configured\n    __"
        
        gdrive_related = [site for site in ddl_sites if 'drive' in site.lower() or 'gdrive' in site.lower()]
        if not gdrive_related:
            gdrive_related = ['No GDrive sites available']
        gdrive_list = ' \n- '.join(gdrive_related)
        gdrivetext = f"__- {gdrive_list}\n    __"
        
        all_sites = bypasser_sites + ddl_sites + freewall_sites
        if all_sites:
            others_list = ' \n- '.join(all_sites[:10])
            otherstext = f"__- {others_list}\n    __"
        else:
            otherstext = "__- No sites configured\n    __"
        
        return ddltext, shortnertext, freewalltext, gdrivetext, otherstext
        
    except:
        # Ultimate fallback - minimal text
        return ("__- No sites available\n    __",) * 5

# Get texts (dynamic or static)
ddltext, shortnertext, freewalltext, gdrivetext, otherstext = build_dynamic_text()

# Build the main help text
ddltext, shortnertext, freewalltext, gdrivetext, otherstext = build_dynamic_text()

HELP_TEXT = (f"**--Just Send me any Supported Links From Below Mentioned Sites--** \n\n"
            f"**List of Sites for DDL : ** \n\n{ddltext} \n"
            f"**List of Sites for Shortners : ** \n\n{shortnertext} \n"
            f"**List of Sites for GDrive Look-ALike : ** \n\n{gdrivetext} \n"
            f"**List of Sites for Jumping Paywall : ** \n\n{freewalltext} \n"
            f"**Other Supported Sites : ** \n\n{otherstext}")

def get_dynamic_help_text():
    """Get updated help text with current config"""
    ddl, shortner, freewall, gdrive, others = build_dynamic_text()
    return (f"**--Just Send me any Supported Links From Below Mentioned Sites--** \n\n"
            f"**List of Sites for DDL : ** \n\n{ddl} \n"
            f"**List of Sites for Shortners : ** \n\n{shortner} \n"
            f"**List of Sites for GDrive Look-ALike : ** \n\n{gdrive} \n"
            f"**List of Sites for Jumping Paywall : ** \n\n{freewall} \n"
            f"**Other Supported Sites : ** \n\n{others}")

def get_stats_text():
    """Get statistics text about supported sites"""
    try:
        from ..config import get_config_stats
        stats = get_config_stats()
        return f"""**📊 Bot Statistics:**
        
**Total Supported Sites:** {stats.get('total', 0)}
• **Bypassers:** {stats.get('bypasser', 0)} sites
• **Direct Downloads:** {stats.get('ddl', 0)} sites  
• **Paywall Bypass:** {stats.get('freewall', 0)} sites

*Bot is ready to process your links!*"""
    except:
        return "**Bot is ready to process your links!**"
