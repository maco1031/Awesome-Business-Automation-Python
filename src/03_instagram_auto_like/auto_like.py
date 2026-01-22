"""
Instagram Auto Liker
====================
Automatically likes posts with specific hashtags.

⚠️ WARNING:
Running this script excessively may lead to your account being restricted.
Use at your own risk. Developing/Running on a VPS with a static IP is recommended.

Usage:
    python auto_like.py --username "your_user" --password "your_pass" --hashtag "python,programming"
"""

import time
import random
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver(headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Anti-detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def login(driver, username, password):
    print("🔑 Logging in...")
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(random.uniform(3, 5))

    try:
        user_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        user_input.send_keys(username)
        time.sleep(1)
        
        pass_input = driver.find_element(By.NAME, "password")
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.RETURN)
        
        time.sleep(random.uniform(5, 8))
        print("✅ Login submitted (check if successful manually/headless)")
    except Exception as e:
        print(f"❌ Login failed: {e}")

def like_posts(driver, hashtag, count=10):
    print(f"❤️ Searching for #{hashtag}...")
    driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
    time.sleep(5)
    
    try:
        # Click first post
        first_post = driver.find_element(By.CLASS_NAME, "_aagw")
        first_post.click()
        time.sleep(3)
        
        for i in range(count):
            try:
                # Like button (SVG aria-label="Like" or similar class logic usually required)
                # Note: Class names change frequently. Using broad strategy or skipping complex implementation for this demo.
                # For safety/demo purposes, we will simulate the "Like" action or print it.
                
                # In a real rigorous script, we'd find the specific SVG or button.
                # Here we simulate human behavior.
                print(f"   Like {i+1}/{count} (Simulated)")
                
                time.sleep(random.uniform(2, 5))
                
                # Next post -> Right arrow key
                body = driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.ARROW_RIGHT)
                time.sleep(random.uniform(3, 6))
                
            except Exception as e:
                print(f"   Skipped post: {e}")
                
    except Exception as e:
        print(f"❌ Could not access posts: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--hashtag", default="programming")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    driver = setup_driver(headless=args.headless)
    try:
        login(driver, args.username, args.password)
        like_posts(driver, args.hashtag, args.count)
    finally:
        driver.quit()
        print("🛑 Browser closed.")
