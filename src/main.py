#!/usr/bin/env python3
"""
Link Bypasser Bot - Main Entry Point
Clean and simple main file using bot core
"""

from pyrogram import Client, BotCommand
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.bot_core import BotCore
from src.core.db import DB
from src.config import CONFIG_LIST

def get_env_config():
    """Get configuration from environment variables (config.json optional)"""
    # Try to load config.json as fallback, but don't require it
    DATA = {}
    try:
        from json import load
        with open("config.json", "r") as f:
            DATA = load(f)
    except:
        print("📄 config.json not found or invalid - using environment variables only")
    
    def getenv(var, default=None):
        return os.environ.get(var) or DATA.get(var, default)
    
    return {
        "bot_token": getenv("TOKEN"),
        "api_hash": getenv("HASH"), 
        "api_id": getenv("ID"),
        "db_api": getenv("DB_API"),
        "db_owner": getenv("DB_OWNER", "bipinkrish"),  # default owner
        "db_name": getenv("DB_NAME", "link_bypass.db")  # default db name
    }

def setup_database(config):
    """Setup database connection"""
    try:
        if all([config["db_api"], config["db_owner"], config["db_name"]]):
            return DB(
                api_key=config["db_api"],
                db_owner=config["db_owner"], 
                db_name=config["db_name"]
            )
    except Exception as e:
        print(f"Database setup failed: {e}")
    
    print("Database not configured or failed to connect")
    return None

def main():
    """Main function to start the bot"""
    print("🚀 Starting Link Bypasser Bot v2.0...")
    print(f"📋 Loaded {len(CONFIG_LIST)} bypasser configurations")
    
    # Show summary of config types
    type_counts = {}
    for config in CONFIG_LIST:
        type_counts[config['type']] = type_counts.get(config['type'], 0) + 1
    
    for bypass_type, count in type_counts.items():
        print(f"   {bypass_type}: {count} sites")
    
    # Get configuration
    config = get_env_config()
    
    if not all([config["bot_token"], config["api_hash"], config["api_id"]]):
        print("❌ Missing required bot configuration (TOKEN, HASH, ID)")
        print("   Please set environment variables or config.json file")
        return
    
    # Setup database
    database = setup_database(config)
    
    # Create bot client
    app = Client(
        "link_bypasser_bot",
        api_id=config["api_id"],
        api_hash=config["api_hash"],
        bot_token=config["bot_token"]
    )
    
    # Setup bot commands
    with app:
        app.set_bot_commands([
            BotCommand("start", "Welcome Message"),
            BotCommand("help", "List of All Supported Sites"),
            BotCommand("config", "Show Current Configuration"),
        ])
    
    # Initialize bot core
    bot_core = BotCore(app, database)
    bot_core.setup_handlers()
    
    print("✅ Bot is ready and running...")
    
    # Start the bot
    app.run()

if __name__ == "__main__":
    main()
