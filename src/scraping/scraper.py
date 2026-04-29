import time
import requests
from bs4 import BeautifulSoup
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
from datetime import datetime
from utils.logger import logging as logger
from utils.robots_utils import check_robots_txt

USER_AGENT = "RealEstateBot/1.0 (Student Project)"
HEADERS = {"User-Agent": USER_AGENT}

def scrape_static_pages(base_url, max_pages=2):
    logger.info("Starting Static Web Scraping (BeautifulSoup)...")
    scraped_data = []

    for page in range(1, max_pages + 1):
        if page > 1:
            logger.info("Applying a 2-second delay between requests...")
            time.sleep(2) 
            
        url = f"{base_url}?page={page}"
        
        if not check_robots_txt(url, USER_AGENT):
            logger.warning(f"Skipping {url} due to robots.txt restrictions.")
            break

        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
          
            soup = BeautifulSoup(response.text, 'lxml')
            
            items = soup.select('.product_pod, .quote') 
            
            for item in items:
                text_content = item.get_text(strip=True)
                if text_content:
                    scraped_data.append({
                        "content": text_content,
                        "source": url,
                        "type": "Static Scrape",
                        "timestamp": datetime.now().isoformat()
                    })
                    
            logger.info(f"Scraped page {page} successfully. Found {len(items)} items.")
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {e}")
            break
            
    return scraped_data

def scrape_dynamic_page(url):
    logger.info("Starting Dynamic Web Scraping (Playwright)...")
    dynamic_data = []
    
    if not PLAYWRIGHT_AVAILABLE:
        logger.error("Playwright is not installed. Skipping dynamic scrape.")
        return dynamic_data
    
    if not check_robots_txt(url, USER_AGENT):
        logger.warning(f"Skipping dynamic scrape of {url} due to robots.txt.")
        return dynamic_data
        
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent=USER_AGENT)
            page.goto(url, wait_until="networkidle")
            
            html = page.content()
            soup = BeautifulSoup(html, 'lxml')
            
            items = soup.select('.quote')
            for item in items:
                dynamic_data.append({
                    "content": item.get_text(strip=True),
                    "source": url,
                    "type": "Dynamic Scrape",
                    "timestamp": datetime.now().isoformat()
                })
                
            browser.close()
            logger.info(f"Dynamic scraping completed. Found {len(dynamic_data)} items.")
    except Exception as e:
        logger.error(f"Playwright dynamic scrape failed: {e}")
        
    return dynamic_data