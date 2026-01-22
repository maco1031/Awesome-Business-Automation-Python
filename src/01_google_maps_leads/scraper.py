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
        logging.info("Step 1: Opening Google Maps...")
        driver.get("https://www.google.com/maps")
        logging.info("Step 2: Page opened. Waiting for load...")
        wait = WebDriverWait(driver, 20)
        
        # Handle Cookie Consent Popup (Common in EU/Japan)
        time.sleep(3)  # Give page time to load popup
        logging.info("Step 3: Checking for cookie consent popup...")
        try:
            # Look for common consent button patterns
            consent_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'すべて同意') or contains(., 'Accept all') or contains(., '同意')]")
            if consent_buttons:
                consent_buttons[0].click()
                logging.info("Dismissed cookie consent popup")
                time.sleep(2)
            else:
                logging.info("No cookie consent popup found")
        except Exception as consent_err:
            logging.info(f"Cookie consent check error: {consent_err}")

        # Search Box
        logging.info("Step 4: Looking for search box...")
        search_box_input = None
        
        # Try ID 'searchboxinput' first
        try:
             search_box_input = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
        except:
             logging.info("  ID 'searchboxinput' not found. Trying fallback selectors...")

        # Fallback 1: Input with name="q"
        if not search_box_input:
             try:
                 search_box_input = driver.find_element(By.NAME, "q")
             except:
                 pass
        
        # Fallback 2: Any visible input
        if not search_box_input:
             try:
                 inputs = driver.find_elements(By.TAG_NAME, "input")
                 for i in inputs:
                     if i.is_displayed():
                         search_box_input = i
                         break
             except:
                 pass

        if not search_box_input:
            raise Exception("Search box element could not be found with any selector.")

        logging.info("Step 5: Found search box. Entering query...")
        search_box_input.send_keys(search_query)
        search_box_input.send_keys(Keys.ENTER)
        
        logging.info("Step 6: Searching... waiting for results...")
        time.sleep(7) # Wait for initial load (increased)

        logging.info("Step 7: Scrolling to load more results...")
        # Attempt to scroll a few times to load results
        for i in range(3): 
            scroll_sidebar(driver)
            logging.info(f"  Scroll {i+1}/3 complete")
        
        # Updated Selection Logic (2026/01)
        # Strategy: Look for the main feed, then find all direct child divs that look like results
        # Common structure: An article or a div with an aria-label (which is the business name)
        
        # Try multiple selectors
        items = []
        
        # Method 1: 'article' role (cleanest if available)
        items = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")
        
        # Method 2: Class 'hfpxzc' (Link overlay, very common in 2024-2025)
        if not items:
             items = driver.find_elements(By.CLASS_NAME, "hfpxzc")

        # Method 3: Fallback - Look for any link with /maps/place/ in href inside the feed
        if not items:
            try:
                feed = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
                items = feed.find_elements(By.XPATH, ".//a[contains(@href, '/maps/place/')]")
            except:
                pass

        logging.info(f"Found {len(items)} potential items on loaded view. Processing...")

        count = 0
        seen_links = set()
        
        for i, item in enumerate(items):
            if count >= max_results:
                break
                
            try:
                # Debug logging for first few items
                link = item.get_attribute('href')
                name = item.get_attribute('aria-label')
                
                # If item is a div (no href), look for 'a' tag inside
                if not link:
                    try:
                        # Common pattern: The main link often has class 'hfpxzc' or is just the first 'a'
                        link_el = item.find_element(By.CSS_SELECTOR, "a")
                        link = link_el.get_attribute('href')
                    except:
                        pass
                
                if i < 3: 
                    logging.info(f"  Item {i}: Link={bool(link)}, Name={name}")

                if not name:
                     # Try finding aria-label on the link element if missing on wrapper
                     if link:
                         try:
                             # Re-find the element that gave us the link to check its aria-label
                             # Or just search broadly for aria-label inside
                             name = item.find_element(By.CSS_SELECTOR, "[aria-label]").get_attribute("aria-label")
                         except:
                             pass
                
                # Fallback for name
                if not name:
                    name = "Unknown Details" 

                if link and link not in seen_links:
                    seen_links.add(link)
                    data = {
                        "Name": name,
                        "Search Query": search_query,
                        "Link": link
                    }
                    results.append(data)
                    count += 1
            except Exception as item_err:
                logging.warning(f"  Item error: {item_err}")
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
