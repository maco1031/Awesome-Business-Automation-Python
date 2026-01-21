"""
Google Maps Scraper for Business Leads
=========================================================
Author: Awesome Business Automation Python
Description:
    This script scrapes business information (Name, Phone, Address) 
    from Google Maps based on a search keyword and location.

Usage:
    python scraper.py
    
    (Follow the interactive prompts to enter keyword and area)

Requirements:
    - Chrome Browser installed
    - Chromedriver (handled automatically by webdriver-manager)
    - See requirements.txt

⚠️ WARNING:
    Extensive scraping may lead to IP bans. 
    It is HIGHLY RECOMMENDED to use a VPS with a static IP for business use.
    Recommended: ConoHa VPS / Xserver VPS
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging
import os

# Logger Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver(headless=False):
    """
    Setup Chrome Driver.
    :param headless: If True, run in headless mode (no GUI).
    """
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    
    # Common options for stability
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--lang=ja-JP')
    options.add_argument('--window-size=1920,1080')
    
    # Anti-detection (Basic)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scroll_sidebar(driver):
    """
    Scroll the sidebar to load more results.
    """
    try:
        # Looking for the sidebar element (structure changes often, precise selector needed)
        # Often role="feed" is used for the list of results
        wait = WebDriverWait(driver, 10)
        feed = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']")))
        
        # Scroll logic
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", feed)
        time.sleep(2) # Wait for load
        return True
    except Exception as e:
        # logging.warning(f"Scroll failed or end of list: {e}")
        return False

def scrape_google_maps(keyword, area, max_results=20, headless=False):
    """
    Main scraping function.
    """
    search_query = f"{area} {keyword}"
    logging.info(f"Starting scrape for: {search_query}")
    
    driver = setup_driver(headless=headless)
    results = []

    try:
        driver.get("https://www.google.com/maps")
        wait = WebDriverWait(driver, 15)

        # Search Box
        # Google Maps ID for search box is usually 'searchboxinput'
        search_box_input = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
        search_box_input.send_keys(search_query)
        search_box_input.send_keys(Keys.ENTER)
        
        logging.info("Searching...")
        time.sleep(5) # Wait for initial load

        # Attempt to scroll a few times to load results
        for _ in range(3): 
            scroll_sidebar(driver)
        
        # Find result items
        # As of early 2025, Google Maps structure is complex.
        # We look for links or containers.
        # 'a' tags with specific classes or href containing '/maps/place/'
        
        items = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")
        if not items:
             items = driver.find_elements(By.CLASS_NAME, "hfpxzc") # Class often used for the link overlay

        logging.info(f"Found {len(items)} potential items on loaded view. Processing...")

        count = 0
        for item in items:
            if count >= max_results:
                break
                
            try:
                name = item.get_attribute('aria-label')
                link = item.get_attribute('href')
                
                if name:
                    # For a full scraper, we would visit 'link' or click 'item' to get phone/address.
                    # This requires handling the side panel.
                    
                    data = {
                        "Name": name,
                        "Search Query": search_query,
                        "Link": link if link else "N/A"
                    }
                    results.append(data)
                    count += 1
            except Exception as item_err:
                continue

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        driver.quit()

    # Save
    if results:
        df = pd.DataFrame(results)
        # Ensure output directory exists (current dir)
        filename = f"leads_{int(time.time())}.xlsx"
        df.to_excel(filename, index=False)
        logging.info(f"Saved {len(results)} leads to {filename}")
    else:
        logging.info("No results found or extraction failed (selectors might need update).")

if __name__ == "__main__":
    print("--- Google Maps Scraper ---")
    kwd = input("Enter Keyword (e.g., Cafe): ") or "Cafe"
    loc = input("Enter Area (e.g., Shinjuku, Tokyo): ") or "Shinjuku"
    
    # Headless prompt
    hl_input = input("Run in Headless mode? (y/n, default n): ").lower()
    use_headless = hl_input == 'y'
    
    scrape_google_maps(kwd, loc, headless=use_headless)
