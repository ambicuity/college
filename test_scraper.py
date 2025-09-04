#!/usr/bin/env python3
"""
Test script for the University Organization Scraper
Tests core functionality with a single university
"""

import sys
import logging
from web_scraper import WebScraper
from excel_generator import ExcelGenerator

def test_web_scraper():
    """Test the web scraper functionality"""
    print("Testing Web Scraper...")
    
    scraper = WebScraper()
    
    # Test with a known university (Biola University)
    test_university = {
        "name": "Biola University",
        "domain": "biola.edu", 
        "potential_paths": [
            "/student-life/clubs",
            "/campus-life/organizations",
            "/clubs",
            "/student-activities",
            "/student-organizations"
        ]
    }
    
    try:
        # Test finding organizations page
        org_url = scraper.find_organizations_page(
            test_university['domain'], 
            test_university['potential_paths']
        )
        
        if org_url:
            print(f"✓ Found organizations page: {org_url}")
            
            # Test extracting organizations
            organizations = scraper.extract_organizations_from_page(org_url)
            print(f"✓ Extracted {len(organizations)} organizations")
            
            if organizations:
                print("Sample organization data:")
                sample_org = organizations[0]
                for key, value in sample_org.items():
                    print(f"  {key}: {value}")
            
            return organizations
        else:
            print("✗ Could not find organizations page")
            return []
            
    except Exception as e:
        print(f"✗ Error testing web scraper: {e}")
        return []
    finally:
        scraper.close()

def test_excel_generator(sample_data):
    """Test the Excel generator functionality"""
    print("\nTesting Excel Generator...")
    
    if not sample_data:
        print("No sample data available for testing Excel generator")
        return
    
    try:
        generator = ExcelGenerator()
        
        # Validate data
        cleaned_data = generator.validate_organizations_data(sample_data)
        print(f"✓ Validated {len(cleaned_data)} organizations")
        
        # Create test Excel file
        filename = generator.create_excel_file("Test University", cleaned_data)
        if filename:
            print(f"✓ Created Excel file: {filename}")
        else:
            print("✗ Failed to create Excel file")
            
    except Exception as e:
        print(f"✗ Error testing Excel generator: {e}")

def test_config_loading():
    """Test configuration loading"""
    print("\nTesting Configuration...")
    
    try:
        from config import universities, ORGANIZATION_FIELDS, PLATFORM_SELECTORS
        
        print(f"✓ Loaded {len(universities)} universities")
        print(f"✓ Loaded {len(ORGANIZATION_FIELDS)} data fields")
        print(f"✓ Loaded {len(PLATFORM_SELECTORS)} platform selectors")
        
        # Display first university as sample
        if universities:
            sample_uni = universities[0]
            print(f"Sample university: {sample_uni['name']} ({sample_uni['domain']})")
        
        return True
        
    except Exception as e:
        print(f"✗ Error loading configuration: {e}")
        return False

def main():
    """Run all tests"""
    print("University Organization Scraper - Test Suite")
    print("=" * 50)
    
    # Test configuration
    config_ok = test_config_loading()
    if not config_ok:
        print("Configuration test failed, stopping tests")
        return
    
    # Test web scraper (this will take time and requires internet)
    sample_organizations = test_web_scraper()
    
    # Test Excel generator
    test_excel_generator(sample_organizations)
    
    print("\n" + "=" * 50)
    print("Test suite completed")

if __name__ == "__main__":
    main()