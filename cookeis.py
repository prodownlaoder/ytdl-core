import sqlite3
import json
import os
import time
from datetime import datetime

# Path to Firefox's cookies.sqlite file
SQLITE_PATH = "/root/snap/firefox/common/.mozilla/firefox/b6my4d5n.myprofile/cookies.sqlite"

# Path to store cookie string as environment variable
ENV_PATH = ".env"

# Function to extract cookies related to YouTube from the Firefox SQLite cookie database
def extract_youtube_cookies(sqlite_path):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔍 Starting YouTube cookie extraction...")

    # Check if the cookies.sqlite file exists
    if not os.path.exists(sqlite_path):
        print("❌ cookies.sqlite not found at the given path.")
        return

    # Connect to the SQLite database
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()

    # Query YouTube cookies
    cursor.execute("""
        SELECT name, value 
        FROM moz_cookies 
        WHERE host LIKE '%youtube.com%'
    """)

    # Fetch results and close connection
    cookies = cursor.fetchall()
    conn.close()

    # If no cookies were found
    if not cookies:
        print("⚠️ No YouTube cookies found.")
        return

    # Build cookie string like: name=value; name2=value2
    cookie_string = '; '.join([f"{name}={value}" for name, value in cookies])

    # Save full cookie list to JSON (optional)
    with open("youtube_cookies.json", "w") as f:
        json.dump([{ "name": name, "value": value } for name, value in cookies], f, indent=2)

    # Save cookie string to .env file
    with open(ENV_PATH, "w") as env_file:
        env_file.write(f'YOUTUBE_COOKIE="{cookie_string}"\n')

    print(f"✅ Saved {len(cookies)} cookies to .env and youtube_cookies.json")

# Main loop: runs every hour
if __name__ == "__main__":
    while True:
        extract_youtube_cookies(SQLITE_PATH)
        
        # Wait 1 hour (3600 seconds) before next run
        print("⏳ Sleeping for 1 hour...\n")
        time.sleep(3600)
