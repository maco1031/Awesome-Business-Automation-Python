"""
RSS Discord Bot
===============
Monitors an RSS feed and sends updates to a Discord Webhook.
designed to run continuously on a VPS.
"""

import time
import requests
import feedparser
import argparse
import sys
import datetime

def send_discord_webhook(webhook_url, entry, dry_run=False):
    """Sends a notification to Discord."""
    if dry_run:
        print(f"🧪 [Dry Run] Found: {entry.title} ({entry.link})")
        return

    data = {
        "content": f"📰 **From RSS Feed**\nTitle: {entry.title}\nLink: {entry.link}"
    }
    try:
        requests.post(webhook_url, json=data)
        print(f"✅ Sent: {entry.title}")
    except Exception as e:
        print(f"❌ Failed to send webhook: {e}")

def monitor_feed(feed_url, webhook_url, interval_min=10, dry_run=False):
    print(f"📡 Starting RSS Monitor...")
    print(f"Target: {feed_url}")
    print(f"Interval: {interval_min} minutes")
    print(f"Mode: {'Dry Run 🧪' if dry_run else 'Live 🚀'}")
    print("------------------------------------------------")
    
    last_entry_link = None
    
    # First fetch to initialize
    try:
        feed = feedparser.parse(feed_url)
        if feed.entries:
            last_entry_link = feed.entries[0].link
            print(f"🔄 Initialized. Latest post: {feed.entries[0].title}")
            
            # In dry-run, show the latest one as a sample
            if dry_run:
                 print("   (Since this is a dry run, showing this mostly recently entry as a sample test)")
                 send_discord_webhook(None, feed.entries[0], dry_run=True)

    except Exception as e:
        print(f"❌ Init failed: {e}")
        sys.exit(1)
        
    while True:
        try:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Checking feed...")
            feed = feedparser.parse(feed_url)
            
            new_entries = []
            if feed.entries:
                for entry in feed.entries:
                    if entry.link == last_entry_link:
                        break
                    new_entries.append(entry)
                
                for entry in reversed(new_entries):
                    send_discord_webhook(webhook_url, entry, dry_run)
                    last_entry_link = entry.link
                    time.sleep(1)
            
            if dry_run:
                print("✨ Dry run verification complete. Exiting...")
                break

            time.sleep(interval_min * 60)
            
        except KeyboardInterrupt:
            print("\n🛑 Monitor stopped by user.")
            break
        except Exception as e:
            print(f"⚠️ Error in loop: {e}")
            time.sleep(60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RSS Discord Bot")
    parser.add_argument("--feed", default="https://news.yahoo.co.jp/rss/topics/it.xml", help="RSS Feed URL")
    parser.add_argument("--webhook", help="Discord Webhook URL (Required unless --dry-run is set)")
    parser.add_argument("--interval", type=int, default=10, help="Check interval in minutes")
    parser.add_argument("--dry-run", action="store_true", help="Test mode (no Discord, exit after 1 check)")
    
    args = parser.parse_args()
    
    if not args.webhook and not args.dry_run:
        parser.error("❌ --webhook is required (unless --dry-run is used)")
    
    monitor_feed(args.feed, args.webhook, args.interval, args.dry_run)
