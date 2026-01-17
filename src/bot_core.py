"""
Core Bot Logic - Cleaned up and organized
"""

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from threading import Thread
from time import time
import re
from urlextract import URLExtract
from os import remove

# Import config and utilities
from config import CONFIG_LIST, process_url, is_ddl_url, is_freewall_url, is_index_url
from src.core.texts import HELP_TEXT
from src.core.db import DB

class BotCore:
    def __init__(self, app_client, database=None):
        self.app = app_client
        self.database = database
        self.extractor = URLExtract()
        self.URL_REGEX = r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+'
        
    def setup_handlers(self):
        """Setup all message handlers"""
        
        @self.app.on_message(filters.command(["start"]))
        def send_start(client, message):
            self.handle_start(message)
            
        @self.app.on_message(filters.command(["help"]))
        def send_help(client, message):
            self.handle_help(message)
            
        @self.app.on_message(filters.command(["config"]))
        def send_config(client, message):
            self.handle_config_command(message)
            
        @self.app.on_callback_query()
        def handle_callback(client, callback_query):
            self.handle_callback_query(callback_query)
            
        @self.app.on_message(filters.text)
        def receive(client, message):
            self.handle_text_message(message)
            
        @self.app.on_message([filters.document, filters.photo, filters.video])
        def docfile(client, message):
            self.handle_media_message(message)
    
    def handle_start(self, message):
        """Handle /start command"""
        self.app.send_message(
            message.chat.id,
            f"__👋 Hi **{message.from_user.mention}**, I am Link Bypasser Bot v2.0, send me any supported links and I will get you results.\nCheckout /help to Read More__",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🌐 Source Code", url="https://github.com/bipinkrish/Link-Bypasser-Bot")],
                [InlineKeyboardButton("🔗 Supported Sites", callback_data="supported_sites")],
            ]),
            reply_to_message_id=message.id,
        )
    
    def handle_help(self, message):
        """Handle /help command"""
        self.app.send_message(
            message.chat.id,
            HELP_TEXT,
            reply_to_message_id=message.id,
            disable_web_page_preview=True,
        )
    
    def handle_config_command(self, message):
        """Handle /config command"""
        # Group configs by type
        config_groups = {}
        for config in CONFIG_LIST:
            config_type = config["type"]
            if config_type not in config_groups:
                config_groups[config_type] = []
            config_groups[config_type].append(config)
        
        config_text = "**🔧 Current Configuration:**\n\n"
        for config_type, configs in config_groups.items():
            config_text += f"**{config_type.upper()}** ({len(configs)} sites)\n"
            for i, config in enumerate(configs[:5], 1):
                config_text += f"`{i}.` {config['description']}\n"
            if len(configs) > 5:
                config_text += f"... and {len(configs) - 5} more\n"
            config_text += "\n"
        
        self.app.send_message(message.chat.id, config_text, reply_to_message_id=message.id)
    
    def handle_callback_query(self, callback_query):
        """Handle callback queries"""
        if callback_query.data == "supported_sites":
            # Group configs for display
            config_groups = {}
            for config in CONFIG_LIST:
                config_type = config["type"]
                if config_type not in config_groups:
                    config_groups[config_type] = []
                config_groups[config_type].append(config)
            
            sites_text = "**🌐 Supported Sites by Category:**\n\n"
            for config_type, configs in config_groups.items():
                sites_text += f"**{config_type.upper()}** ({len(configs)} sites)\n"
                for i, config in enumerate(configs[:10], 1):
                    domain = config['url_regex'].replace('\\', '').replace('r"', '').replace('"', '')
                    sites_text += f"`{domain}`\n"
                if len(configs) > 10:
                    sites_text += f"... and {len(configs) - 10} more\n"
                sites_text += "\n"
            
            callback_query.edit_message_text(
                sites_text,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
                ])
            )
        elif callback_query.data == "back_to_start":
            callback_query.edit_message_text(
                f"__👋 Hi **{callback_query.from_user.mention}**, I am Link Bypasser Bot v2.0, send me any supported links and I will get you results.\nCheckout /help to Read More__",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🌐 Source Code", url="https://github.com/bipinkrish/Link-Bypasser-Bot")],
                    [InlineKeyboardButton("🔗 Supported Sites", callback_data="supported_sites")],
                ])
            )
    
    def handle_text_message(self, message):
        """Handle text messages"""
        bypass = Thread(target=lambda: self.process_message(message), daemon=True)
        bypass.start()
    
    def handle_media_message(self, message):
        """Handle media messages"""
        try:
            if message.document and message.document.file_name.endswith("dlc"):
                bypass = Thread(target=lambda: self.handle_dlc_file(message), daemon=True)
                bypass.start()
                return
        except:
            pass
        bypass = Thread(target=lambda: self.process_message(message, is_media=True), daemon=True)
        bypass.start()
    
    def handle_dlc_file(self, message):
        """Handle DLC file processing"""
        msg = self.app.send_message(
            message.chat.id, "🔎 __processing DLC file...__", reply_to_message_id=message.id
        )
        
        try:
            file = self.app.download_media(message)
            from src.bypasser.bypasser_functions import getlinks
            dlccont = open(file, "r").read()
            links = getlinks(dlccont)
            self.app.edit_message_text(
                message.chat.id, msg.id, f"__{links}__", disable_web_page_preview=True
            )
        except Exception as e:
            self.app.edit_message_text(
                message.chat.id, msg.id, f"__Error processing DLC file: {e}__"
            )
        finally:
            try:
                remove(file)
            except:
                pass
    
    def extract_urls(self, message, is_media=False):
        """Extract URLs from message"""
        urls = []
        texts = message.caption if is_media else message.text
        if not texts:
            return []
        
        # Get entities
        entities = []
        if is_media and hasattr(message, 'caption_entities') and message.caption_entities:
            entities = message.caption_entities
        elif message.entities:
            entities = message.entities
        
        # Extract URLs from entities
        if entities:
            for entity in entities:
                entity_type = str(entity.type).split('.')[-1].lower()
                if entity_type == "url":
                    url = texts[entity.offset:entity.offset + entity.length]
                    urls.append(url)
                elif entity_type == "text_link" and hasattr(entity, 'url'):
                    urls.append(entity.url)
        
        # Fallback URL extraction
        urls.extend(self.extractor.find_urls(texts))
        urls.extend(re.findall(self.URL_REGEX, texts))
        
        # Clean and normalize URLs
        cleaned_urls = []
        for url in urls:
            cleaned_url = url.strip(".,").rstrip("/")
            if cleaned_url:
                if not cleaned_url.startswith(('http://', 'https://')):
                    cleaned_url = 'https://' + cleaned_url
                cleaned_urls.append(cleaned_url)
        
        return list(dict.fromkeys(cleaned_urls))  # Remove duplicates
    
    def get_processing_message(self, url):
        """Get appropriate processing message based on URL type"""
        if is_ddl_url(url):
            return "⚡ __generating direct link...__"
        elif is_freewall_url(url):
            return "🕴️ __jumping the wall...__"
        elif is_index_url(url):
            return "📋 __scraping index...__"
        elif "olamovies" in url or "psa.wf" in url:
            return "⏳ __this might take some time...__"
        else:
            return "🔎 __bypassing...__"
    
    def handle_index_processing(self, url, message, msg):
        """Handle index page processing"""
        result = process_url(url)
        try:
            self.app.delete_messages(message.chat.id, msg.id)
        except:
            pass
        
        if self.database and result:
            self.database.insert(url, result)
        
        if isinstance(result, list):
            for page in result:
                self.app.send_message(
                    message.chat.id,
                    page,
                    reply_to_message_id=message.id,
                    disable_web_page_preview=True,
                )
        else:
            self.app.send_message(
                message.chat.id,
                str(result),
                reply_to_message_id=message.id,
                disable_web_page_preview=True,
            )
    
    def handle_freewall_processing(self, url, message, msg):
        """Handle freewall processing"""
        freefile = process_url(url)
        if freefile and isinstance(freefile, str) and freefile.endswith(('.png', '.jpg', '.pdf', '.pptx', '.html')):
            try:
                self.app.send_document(
                    message.chat.id, freefile, reply_to_message_id=message.id
                )
                remove(freefile)
                self.app.delete_messages(message.chat.id, [msg.id])
                return True
            except Exception as e:
                print(f"Error sending file: {e}")
        
        self.app.send_message(
            message.chat.id, "__Failed to bypass paywall__", reply_to_message_id=message.id
        )
        try:
            self.app.delete_messages(message.chat.id, [msg.id])
        except:
            pass
        return True
    
    def process_message(self, message, is_media=False):
        """Main message processing logic"""
        urls = self.extract_urls(message, is_media)
        
        if not urls:
            self.app.send_message(
                message.chat.id,
                "No valid URLs found in the message.",
                reply_to_message_id=message.id
            )
            return
        
        # Send processing message
        first_url = urls[0]
        processing_msg = self.get_processing_message(first_url)
        msg = self.app.send_message(message.chat.id, processing_msg, reply_to_message_id=message.id)
        
        start_time = time()
        results = []
        
        for url in urls:
            # Check database first
            db_result = None
            if self.database:
                db_result = self.database.find(url)
            
            if db_result:
                print("Found in DB")
                results.append(str(db_result))
                continue
            
            # Handle special cases
            if is_index_url(url):
                self.handle_index_processing(url, message, msg)
                return
            
            if is_freewall_url(url):
                if self.handle_freewall_processing(url, message, msg):
                    return
                continue
            
            # Process normally
            try:
                result = process_url(url)
                if result:
                    # Add to database if successful
                    if (not db_result) and ("http://" in str(result) or "https://" in str(result)) and self.database:
                        self.database.insert(url, result)
                    results.append(str(result))
                    print(f"Bypassed: {result}")
            except Exception as e:
                results.append(f"**Error**: {str(e)}")
                print(f"Error processing {url}: {e}")
        
        # Send results
        self.send_results(message, msg, results, time() - start_time)
    
    def send_results(self, message, msg, results, processing_time):
        """Send the final results to user"""
        if not results:
            self.app.edit_message_text(
                message.chat.id, msg.id, "__No results found__"
            )
            return
        
        # Combine results
        final_text = "\n".join(results)
        
        # Split large messages
        final_messages = []
        tmp = ""
        for line in final_text.split("\n"):
            if len(tmp + line + "\n") > 4000:
                final_messages.append(tmp)
                tmp = line + "\n"
            else:
                tmp += line + "\n"
        if tmp:
            final_messages.append(tmp)
        
        try:
            self.app.delete_messages(message.chat.id, msg.id)
        except:
            pass
        
        # Send messages
        tmsgid = message.id
        for text in final_messages:
            if text.strip():
                tmsg = self.app.send_message(
                    message.chat.id,
                    f"__{text}__",
                    reply_to_message_id=tmsgid,
                    disable_web_page_preview=True,
                )
                tmsgid = tmsg.id
        
        print(f"Processing took {processing_time:.2f} seconds")
