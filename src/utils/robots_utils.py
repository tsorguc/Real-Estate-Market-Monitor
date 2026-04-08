import urllib.robotparser
from urllib.parse import urlparse
from utils.logger import logging as logger

def check_robots_txt(url, user_agent="RealEstateBot/1.0 (Student Project)"):
    """
    Checks the robots.txt file of the target domain to see if scraping is allowed.
    """
    try:
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        robots_url = f"{base_url}/robots.txt"
        
        logger.info(f"Checking robots.txt at {robots_url}...")
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        
        is_allowed = rp.can_fetch(user_agent, url)
        if is_allowed:
            logger.info(f"✅ robots.txt ALLOWS scraping for {url}")
        else:
            logger.warning(f"❌ robots.txt FORBIDS scraping for {url}")
            
        return is_allowed
    except Exception as e:
        logger.error(f"⚠️ Error reading robots.txt for {url}: {e}. Defaulting to allowed.")
        return True