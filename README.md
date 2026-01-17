# 🚀 Link Bypasser Bot

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-green.svg)](https://flask.palletsprojects.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A powerful Telegram Bot and Web Application that bypasses ad links, generates direct download links, and jumps paywalls for **100+ websites**. Features a modern, modular architecture with dynamic site support and a premium dark web interface.

## 🌟 Features

- **100+ Supported Sites**: Automatically bypass links from major file hosting and streaming platforms
- **Telegram Integration**: Full-featured bot with real-time processing
- **Web Interface**: Premium dark minimalist design with responsive layout
- **Modular Architecture**: Easy to extend with new site support
- **Smart Caching**: Public database integration for faster responses
- **Auto-Discovery**: Dynamic site loading system
- **Docker Ready**: Production deployment with health checks
- **Mobile Responsive**: Works seamlessly on all devices

## 🎯 Live Demo

- **Telegram Bot**: [@BypassUrlsBot](https://t.me/BypassUrlsBot)
- **Web App**: Try the interface with instant link processing

## 🏗️ Architecture

```
src/
├── app.py              # Flask web application
├── config.py           # Dynamic site discovery system
├── core/
│   ├── texts.py        # Dynamic text generation
│   └── db.py          # Database operations
└── sites/             # Site modules (100+ sites)
    ├── bypasser.py    # Link bypass sites
    ├── ddl.py         # Direct download sites
    └── freewall.py    # Paywall bypass sites
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/bipinkrish/Link-Bypasser-Bot.git
cd Link-Bypasser-Bot

# Build and run with Docker
docker build -t link-bypasser .
docker run -p 5000:5000 link-bypasser
```

### Option 2: Manual Setup

```bash
# Clone and setup
git clone https://github.com/bipinkrish/Link-Bypasser-Bot.git
cd Link-Bypasser-Bot

# Install dependencies
pip install -r requirements.txt

# Configure environment (see Configuration section)
cp config.json.example config.json

# Run the application
python src/app.py
```

### Option 3: Deploy to Heroku

_Note: Fork the repository and change its name before deployment_

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/bipinkrish/Link-Bypasser-Bot)

## ⚙️ Configuration

### Required Variables

Set these environment variables or in `config.json`:

```json
{
  "TOKEN": "Your Bot Token from @BotFather",
  "HASH": "API Hash from my.telegram.org",
  "ID": "API ID from my.telegram.org"
}
```

### Optional Variables

```json
{
  "CRYPT": "GDTot Crypt token",
  "XSRF_TOKEN": "XSRF Token for protected sites",
  "Laravel_Session": "Laravel Session cookie",
  "DRIVEFIRE_CRYPT": "Drivefire bypass token",
  "KOLOP_CRYPT": "Kolop bypass token",
  "HUBDRIVE_CRYPT": "Hubdrive bypass token",
  "KATDRIVE_CRYPT": "Katdrive bypass token",
  "UPTOBOX_TOKEN": "Uptobox premium token",
  "TERA_COOKIE": "Terabox ndus cookie value",
  "CLOUDFLARE": "cf_clearance cookie for Cloudflare sites",
  "PORT": "5000"
}
```

### Database Configuration (Optional)

Enable public caching database:

```json
{
  "DB_API": "DBHub.io API key (Read/Write permission)",
  "DB_OWNER": "bipinkrish",
  "DB_NAME": "link_bypass.db"
}
```

## 🤖 Bot Commands

- `/start` - Welcome message with feature overview
- `/help` - Complete list of supported sites by category

## 🌐 Supported Sites

The bot supports **100+ websites** across three main categories:

### 🔗 Link Bypass Sites (40+)

- LinkVertise, Shortlinks, AdFly, GPLinks, and more
- Automatically detected via URL patterns

### 📁 Direct Download Sites (50+)

- Google Drive, Mega, MediaFire, Terabox, and more
- Generates direct download links

### 🔓 Paywall Bypass Sites (15+)

- Medium, Telegraph, Scribd, and more
- Provides unrestricted access

_For the complete list, run the bot's `/help` command or check the web interface_

## 🛠️ How to Contribute

We welcome contributions! Here's how to extend site support:

### Adding a New Site Module

1. **Fork and Clone**

   ```bash
   git fork https://github.com/bipinkrish/Link-Bypasser-Bot.git
   git clone https://github.com/yourusername/Link-Bypasser-Bot.git
   ```

2. **Choose the Right Module**

   - Add to `src/sites/bypasser.py` for ad/short links
   - Add to `src/sites/ddl.py` for direct downloads
   - Add to `src/sites/freewall.py` for paywall bypass

3. **Implement Required Components**

   Each site needs these components in the module:

   ```python
   # Site metadata
   SITE_NAME = "YourSite"

   # URL patterns for auto-detection
   URL_PATTERNS = [
       r'https?://yoursite\.com/.*',
       r'https?://.*\.yoursite\.com/.*'
   ]

   # Main processing function
   def process_url(url):
       """
       Process the URL and return result

       Args:
           url (str): The URL to process

       Returns:
           str: The processed result (direct link, bypassed URL, etc.)

       Raises:
           Exception: On processing errors
       """
       # Your implementation here
       return processed_url
   ```

4. **Example Implementation**

   ```python
   import requests
   from bs4 import BeautifulSoup

   SITE_NAME = "ExampleSite"
   URL_PATTERNS = [r'https?://example\.com/.*']

   def process_url(url):
       try:
           response = requests.get(url)
           soup = BeautifulSoup(response.text, 'html.parser')

           # Extract the direct link
           direct_link = soup.find('a', {'id': 'download'})['href']

           return direct_link
       except Exception as e:
           raise Exception(f"Failed to process {url}: {str(e)}")
   ```

5. **Test Your Implementation**

   ```bash
   # Test locally
   python src/app.py

   # Test with your URLs in the web interface
   ```

6. **Submit a Pull Request**
   - Ensure your code follows the existing patterns
   - Test with multiple URLs from the site
   - Include a brief description of the site and implementation

### Advanced Contribution Guidelines

- **Error Handling**: Always wrap requests in try-except blocks
- **User Agents**: Use realistic browser user agents for requests
- **Rate Limiting**: Implement delays for sites that require them
- **Dependencies**: Minimize external dependencies, use standard libraries when possible
- **Documentation**: Comment complex logic and unusual patterns
- **Testing**: Test edge cases like expired links, private files, etc.

### Development Setup

```bash
# Setup development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8

# Run tests
pytest tests/

# Format code
black src/
```

## 📚 API Documentation

### Auto-Discovery System

The application automatically discovers and loads site modules using:

```python
from src.config import get_all_site_names, get_function_by_url

# Get all supported sites
sites = get_all_site_names()

# Process URL automatically
result = get_function_by_url(url)
```

### Web API Endpoints

- `GET /` - Main interface with site listings
- `POST /bypass` - Process URLs via API
- `GET /health` - Health check endpoint

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running from project root
2. **Site Not Working**: Check if cookies/tokens are required
3. **Docker Issues**: Verify port mapping and environment variables
4. **Database Errors**: Check DBHub.io API key permissions

### Getting Help

- Create an issue for bugs or feature requests
- Check existing issues for solutions
- Join our community discussions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- All contributors who help expand site support
- The open-source community for tools and libraries
- Users who test and report issues

---

⭐ **Star this repository** if you find it useful!

[![GitHub stars](https://img.shields.io/github/stars/bipinkrish/Link-Bypasser-Bot?style=social)](https://github.com/bipinkrish/Link-Bypasser-Bot/stargazers)
