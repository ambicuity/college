import requests
import time
import logging
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.driver = None
        self.setup_logging()
    
    def setup_logging(self):
        """Configure logging for the scraper"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_selenium(self):
        """Setup Selenium WebDriver with Chrome"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            return True
        except Exception as e:
            self.logger.error(f"Failed to setup Selenium: {e}")
            return False
    
    def get_page_content(self, url, use_selenium=False):
        """Get page content using either requests or Selenium"""
        try:
            if use_selenium:
                if not self.driver:
                    if not self.setup_selenium():
                        return None
                
                self.driver.get(url)
                time.sleep(3)  # Wait for page to load
                return self.driver.page_source
            else:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response.text
        except Exception as e:
            self.logger.error(f"Failed to get content from {url}: {e}")
            return None
    
    def find_organizations_page(self, university_domain, potential_paths):
        """Find the student organizations page for a university"""
        base_urls = [f"https://{university_domain}", f"https://www.{university_domain}"]
        
        for base_url in base_urls:
            # Try direct paths first
            for path in potential_paths:
                test_url = f"{base_url}{path}"
                self.logger.info(f"Trying: {test_url}")
                
                content = self.get_page_content(test_url)
                if content and self.is_organizations_page(content):
                    self.logger.info(f"Found organizations page: {test_url}")
                    return test_url
            
            # Try searching the main page for organization links
            main_content = self.get_page_content(base_url)
            if main_content:
                soup = BeautifulSoup(main_content, 'html.parser')
                org_link = self.find_organization_link_in_content(soup, base_url)
                if org_link:
                    # Verify the found link actually contains organizations
                    link_content = self.get_page_content(org_link)
                    if link_content and self.is_organizations_page(link_content):
                        self.logger.info(f"Found organizations page via link: {org_link}")
                        return org_link
            
            # Try common search patterns
            search_patterns = [
                "/student-life",
                "/campus-life", 
                "/involvement",
                "/activities",
                "/student-engagement"
            ]
            
            for pattern in search_patterns:
                test_url = f"{base_url}{pattern}"
                content = self.get_page_content(test_url)
                if content:
                    soup = BeautifulSoup(content, 'html.parser')
                    org_link = self.find_organization_link_in_content(soup, base_url)
                    if org_link:
                        link_content = self.get_page_content(org_link)
                        if link_content and self.is_organizations_page(link_content):
                            self.logger.info(f"Found organizations page via search: {org_link}")
                            return org_link
        
        self.logger.warning(f"Could not find organizations page for {university_domain}")
        return None
    
    def is_organizations_page(self, content):
        """Check if a page appears to be a student organizations page"""
        if not content:
            return False
        
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text().lower()
        
        # Look for key indicators
        indicators = [
            'student organizations',
            'student clubs',
            'clubs and organizations', 
            'student activities',
            'campus organizations',
            'student involvement'
        ]
        
        return any(indicator in text for indicator in indicators)
    
    def find_organization_link_in_content(self, soup, base_url):
        """Find organization links in page content"""
        # Look for links containing organization-related keywords
        keywords = ['club', 'organization', 'student-life', 'campus-life', 'activities', 'involvement']
        
        # First, look for specific text patterns
        org_keywords = [
            'student organizations',
            'student clubs', 
            'clubs and organizations',
            'student activities',
            'get involved',
            'student involvement',
            'campus organizations'
        ]
        
        for link in soup.find_all('a', href=True):
            link_text = link.get_text().lower().strip()
            href = link['href'].lower()
            
            # Check for exact matches in link text
            if any(org_keyword in link_text for org_keyword in org_keywords):
                full_url = urljoin(base_url, link['href'])
                return full_url
            
            # Check for keywords in href
            if any(keyword in href for keyword in keywords):
                if any(org_word in link_text for org_word in ['organization', 'club', 'activities', 'involvement']):
                    full_url = urljoin(base_url, link['href'])
                    return full_url
        
        # Look for navigation menu items
        nav_selectors = ['nav', '.nav', '.navigation', '.menu', '.header-nav']
        for selector in nav_selectors:
            nav_element = soup.select_one(selector)
            if nav_element:
                for link in nav_element.find_all('a', href=True):
                    link_text = link.get_text().lower().strip()
                    if any(org_keyword in link_text for org_keyword in org_keywords):
                        full_url = urljoin(base_url, link['href'])
                        return full_url
        
        return None
    
    def extract_organizations_from_page(self, url, selectors=None):
        """Extract organization data from a page"""
        organizations = []
        
        # Try both requests and Selenium
        for use_selenium in [False, True]:
            content = self.get_page_content(url, use_selenium=use_selenium)
            if content:
                orgs = self.parse_organizations(content, url, selectors)
                if orgs:
                    organizations.extend(orgs)
                    break
        
        return organizations
    
    def parse_organizations(self, content, base_url, selectors=None):
        """Parse organizations from HTML content"""
        soup = BeautifulSoup(content, 'html.parser')
        organizations = []
        
        # Try different selector strategies
        from config import PLATFORM_SELECTORS
        
        if selectors:
            selector_sets = [selectors]
        else:
            selector_sets = list(PLATFORM_SELECTORS.values())
        
        for selector_set in selector_sets:
            org_elements = soup.select(selector_set.get('organization_list', ''))
            
            if org_elements:
                self.logger.info(f"Found {len(org_elements)} organizations using selector: {selector_set.get('organization_list')}")
                
                for element in org_elements:
                    org_data = self.extract_organization_data(element, base_url, selector_set)
                    if org_data and org_data.get('Organization Name'):
                        organizations.append(org_data)
                
                if organizations:
                    break
        
        # Fallback: try to find organization info in a more generic way
        if not organizations:
            organizations = self.fallback_organization_extraction(soup, base_url)
        
        return organizations
    
    def extract_organization_data(self, element, base_url, selectors):
        """Extract data for a single organization"""
        data = {}
        
        # Organization name
        name_elem = element.select_one(selectors.get('organization_name', ''))
        data['Organization Name'] = name_elem.get_text().strip() if name_elem else ''
        
        # Organization link
        link_elem = element.select_one(selectors.get('organization_link', 'a'))
        if link_elem and link_elem.get('href'):
            data['Organization Link'] = urljoin(base_url, link_elem['href'])
        else:
            data['Organization Link'] = ''
        
        # Category
        category_elem = element.select_one(selectors.get('category', ''))
        data['Category'] = category_elem.get_text().strip() if category_elem else ''
        
        # Description
        desc_elem = element.select_one(selectors.get('description', ''))
        data['Description'] = desc_elem.get_text().strip() if desc_elem else ''
        
        # Logo
        logo_elem = element.select_one(selectors.get('logo', 'img'))
        if logo_elem and logo_elem.get('src'):
            data['Logo Link'] = urljoin(base_url, logo_elem['src'])
        else:
            data['Logo Link'] = ''
        
        # Contact info and social media - extract from the organization detail page
        if data['Organization Link']:
            detail_data = self.extract_organization_details(data['Organization Link'])
            data.update(detail_data)
        
        # Fill in missing fields
        from config import ORGANIZATION_FIELDS
        for field in ORGANIZATION_FIELDS:
            if field not in data:
                data[field] = ''
        
        return data
    
    def extract_organization_details(self, org_url):
        """Extract detailed information from organization page"""
        details = {
            'Email': '',
            'Phone Number': '',
            'LinkedIn Link': '',
            'Instagram Link': '',
            'Facebook Link': '',
            'Twitter Link': '',
            'YouTube Link': '',
            'TikTok Link': ''
        }
        
        content = self.get_page_content(org_url)
        if not content:
            return details
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, content)
        if emails:
            details['Email'] = emails[0]
        
        # Extract phone number
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, content)
        if phones:
            details['Phone Number'] = phones[0]
        
        # Extract social media links
        links = soup.find_all('a', href=True)
        from config import SOCIAL_MEDIA_PATTERNS
        
        for link in links:
            href = link['href']
            for platform, patterns in SOCIAL_MEDIA_PATTERNS.items():
                if any(pattern in href.lower() for pattern in patterns):
                    field_name = f"{platform} Link"
                    if not details[field_name]:  # Only set if not already found
                        details[field_name] = href
                    break
        
        return details
    
    def fallback_organization_extraction(self, soup, base_url):
        """Fallback method to extract organizations when selectors fail"""
        organizations = []
        
        # Look for common patterns
        potential_orgs = soup.find_all(['div', 'li', 'article'], class_=re.compile(r'org|club|student', re.I))
        
        for element in potential_orgs:
            name_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5'])
            if name_elem:
                org_data = {
                    'Organization Name': name_elem.get_text().strip(),
                    'Organization Link': '',
                    'Category': '',
                    'Logo Link': '',
                    'Description': '',
                    'Email': '',
                    'Phone Number': '',
                    'LinkedIn Link': '',
                    'Instagram Link': '',
                    'Facebook Link': '',
                    'Twitter Link': '',
                    'YouTube Link': '',
                    'TikTok Link': ''
                }
                
                # Try to find link
                link_elem = element.find('a', href=True)
                if link_elem:
                    org_data['Organization Link'] = urljoin(base_url, link_elem['href'])
                
                organizations.append(org_data)
        
        return organizations
    
    def close(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
        self.session.close()