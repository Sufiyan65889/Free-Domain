import asyncio
import pyshorteners
import re
from urllib.parse import urlparse
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Banner
banner = r'''
███████╗ █████╗  ██████╗ █████╗ ██████╗  ██╗███╗   ██╗ ██████╗ 
██╔════╝██╔══██╗██╔════╝██╔══██╗██╔══██╗███║████╗  ██║██╔════╝ 
█████╗  ███████║██║     ███████║██║  ██║╚██║██╔██╗ ██║██║  ███╗
██╔══╝  ██╔══██║██║     ██╔══██║██║  ██║ ██║██║╚██╗██║██║   ██║
██║     ██║  ██║╚██████╗██║  ██║██████╔╝ ██║██║ ╚████║╚██████╔╝
╚═╝     ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
            The Ultimate Masking Tool by Sufiyan
'''

print(banner)

# URL shorteners
s = pyshorteners.Shortener()
shorteners = [s.tinyurl, s.dagd, s.clckru, s.osdb]

def mask_url(domain, keyword, url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{domain}-{keyword}@{parsed_url.netloc}{parsed_url.path}"

# Telegram bot handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = """
    ✨ *Welcome to Sufiyan's Masking Bot* ✨

    👋 Hello, I'm here to help you mask URLs in a customized way!  
    You can create your own masked URLs using the following format:

    `/mask [original_url] [custom_domain] [keyword]`

    💡 Example:
    `/mask https://example.com gmail.com login`

    🚀 Let's get started!
    """
    await update.message.reply_text(welcome_msg, parse_mode="Markdown")

async def mask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 3:
            await update.message.reply_text("Use: `/mask [original_url] [custom_domain] [keyword]`", parse_mode="Markdown")
            return

        web_url, custom_domain, keyword = args

        if not re.match(r'^(https?://)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', web_url):
            await update.message.reply_text("Invalid original URL.")
            return
        if not re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', custom_domain):
            await update.message.reply_text("Invalid domain.")
            return
        if " " in keyword or len(keyword) > 15:
            await update.message.reply_text("Invalid keyword (no spaces, max 15 chars).")
            return

        short_urls = []
        for shortener in shorteners:
            try:
                short_url = shortener.short(web_url)
                short_urls.append(short_url)
            except:
                continue

        if not short_urls:
            await update.message.reply_text("Failed to shorten the URL.")
            return

        msg = f"🔗 *Masked URLs for:* `{web_url}`\n\n"
        for i, su in enumerate(short_urls, start=1):
            masked = mask_url(custom_domain, keyword, su)
            msg += f"{i}. `{masked}`\n"
        
        # Surprise Feature: Quick facts after masking!
        surprise_fact = """
        🤩 *Quick Fact:*
        Did you know? The world's shortest URL ever was just `http://a/`! 
        And yes, you can create even shorter masked URLs now! Keep experimenting!
        """
        await update.message.reply_text(msg + surprise_fact, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Replace this with your actual bot token
TOKEN = "7277293554:AAFsPVjxT8Ngb19qopkItybn5FCyVE1wQq8"

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("mask", mask_command))

print("Bot is running...")
app.run_polling()