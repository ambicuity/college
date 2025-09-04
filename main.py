#!/usr/bin/env python3
"""
AI Web Scraping Agent for University Student Organizations
Main orchestration script for scraping student organization data from universities
"""

import logging
import time
import sys
from datetime import datetime
from web_scraper import WebScraper
from excel_generator import ExcelGenerator
from config import universities

class UniversityOrgScraper:
    def __init__(self):
        self.scraper = WebScraper()
        self.excel_generator = ExcelGenerator()
        self.results = {}
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_filename = f"university_scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("University Organization Scraper initialized")
    
    def scrape_university(self, university):
        """Scrape a single university for student organizations"""
        university_name = university['name']
        domain = university['domain']
        potential_paths = university['potential_paths']
        
        self.logger.info(f"Starting scrape for: {university_name}")
        start_time = time.time()
        
        result = {
            'organizations': [],
            'organizations_url': None,
            'status': 'Failed',
            'scraping_time': None,
            'error': None
        }
        
        try:
            # Find the organizations page
            org_page_url = self.scraper.find_organizations_page(domain, potential_paths)
            
            if not org_page_url:
                result['error'] = "Could not find organizations page"
                self.logger.warning(f"No organizations page found for {university_name}")
                return result
            
            result['organizations_url'] = org_page_url
            
            # Extract organizations from the page
            organizations = self.scraper.extract_organizations_from_page(org_page_url)
            
            if organizations:
                # Validate and clean the data
                cleaned_organizations = self.excel_generator.validate_organizations_data(organizations)
                result['organizations'] = cleaned_organizations
                result['status'] = 'Success'
                
                self.logger.info(f"Found {len(cleaned_organizations)} organizations for {university_name}")
                
                # Create Excel file
                excel_filename = self.excel_generator.create_excel_file(university_name, cleaned_organizations)
                if excel_filename:
                    result['excel_file'] = excel_filename
                
            else:
                result['error'] = "No organizations found on the page"
                self.logger.warning(f"No organizations extracted for {university_name}")
        
        except Exception as e:
            result['error'] = str(e)
            self.logger.error(f"Error scraping {university_name}: {e}")
        
        finally:
            end_time = time.time()
            result['scraping_time'] = f"{end_time - start_time:.2f} seconds"
        
        return result
    
    def scrape_all_universities(self):
        """Scrape all universities in the configuration"""
        self.logger.info(f"Starting to scrape {len(universities)} universities")
        
        for i, university in enumerate(universities, 1):
            university_name = university['name']
            self.logger.info(f"[{i}/{len(universities)}] Processing: {university_name}")
            
            # Scrape the university
            result = self.scrape_university(university)
            self.results[university_name] = result
            
            # Log result
            if result['status'] == 'Success':
                self.logger.info(f"✓ {university_name}: {len(result['organizations'])} organizations")
            else:
                self.logger.error(f"✗ {university_name}: {result.get('error', 'Unknown error')}")
            
            # Add delay between requests to be respectful
            if i < len(universities):
                time.sleep(2)
        
        # Generate summary report
        summary_file = self.excel_generator.create_summary_report(self.results)
        if summary_file:
            self.logger.info(f"Summary report created: {summary_file}")
        
        # Print final summary
        self.print_final_summary()
    
    def print_final_summary(self):
        """Print a final summary of the scraping results"""
        print("\n" + "="*80)
        print("FINAL SCRAPING SUMMARY")
        print("="*80)
        
        successful = 0
        failed = 0
        total_organizations = 0
        
        for university_name, result in self.results.items():
            status_icon = "✓" if result['status'] == 'Success' else "✗"
            org_count = len(result['organizations'])
            
            print(f"{status_icon} {university_name:<40} {org_count:>5} organizations")
            
            if result['status'] == 'Success':
                successful += 1
                total_organizations += org_count
            else:
                failed += 1
                print(f"    Error: {result.get('error', 'Unknown')}")
        
        print("-" * 80)
        print(f"Universities processed: {len(universities)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Total organizations found: {total_organizations}")
        print("="*80)
    
    def cleanup(self):
        """Clean up resources"""
        self.scraper.close()
        self.logger.info("Cleanup completed")

def main():
    """Main function to run the scraping process"""
    scraper = UniversityOrgScraper()
    
    try:
        scraper.scrape_all_universities()
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
        scraper.logger.info("Scraping interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
        scraper.logger.error(f"Unexpected error: {e}")
    finally:
        scraper.cleanup()

if __name__ == "__main__":
    main()