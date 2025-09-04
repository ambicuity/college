#!/usr/bin/env python3
"""
Demo script to showcase the Excel generation functionality
Creates sample data and generates an Excel file
"""

from excel_generator import ExcelGenerator
from config import ORGANIZATION_FIELDS

def create_sample_data():
    """Create sample organization data for demonstration"""
    sample_organizations = [
        {
            "Category": "Academic",
            "Organization Name": "Computer Science Club", 
            "Organization Link": "https://example.edu/organizations/cs-club",
            "Logo Link": "https://example.edu/images/cs-logo.png",
            "Description": "A club for computer science students to collaborate on projects, learn new technologies, and network with industry professionals.",
            "Email": "csclub@example.edu",
            "Phone Number": "555-123-4567",
            "LinkedIn Link": "https://linkedin.com/company/cs-club-example",
            "Instagram Link": "https://instagram.com/csclub_example",
            "Facebook Link": "https://facebook.com/csclub.example",
            "Twitter Link": "https://twitter.com/csclub_example",
            "YouTube Link": "https://youtube.com/c/csclub-example",
            "TikTok Link": ""
        },
        {
            "Category": "Cultural",
            "Organization Name": "International Student Association",
            "Organization Link": "https://example.edu/organizations/isa",
            "Logo Link": "https://example.edu/images/isa-logo.png", 
            "Description": "Promoting cultural diversity and supporting international students through events, mentorship, and community building.",
            "Email": "isa@example.edu",
            "Phone Number": "",
            "LinkedIn Link": "",
            "Instagram Link": "https://instagram.com/isa_example",
            "Facebook Link": "https://facebook.com/isa.example",
            "Twitter Link": "",
            "YouTube Link": "",
            "TikTok Link": "https://tiktok.com/@isa_example"
        },
        {
            "Category": "Sports",
            "Organization Name": "Ultimate Frisbee Club",
            "Organization Link": "https://example.edu/organizations/ultimate-frisbee",
            "Logo Link": "",
            "Description": "Competitive and recreational ultimate frisbee for all skill levels. We compete in regional tournaments and host campus events.",
            "Email": "frisbee@example.edu",
            "Phone Number": "555-987-6543",
            "LinkedIn Link": "",
            "Instagram Link": "https://instagram.com/ultimate_example",
            "Facebook Link": "https://facebook.com/ultimate.frisbee.example",
            "Twitter Link": "https://twitter.com/ultimate_example",
            "YouTube Link": "",
            "TikTok Link": ""
        },
        {
            "Category": "Service",
            "Organization Name": "Habitat for Humanity Campus Chapter",
            "Organization Link": "https://example.edu/organizations/habitat",
            "Logo Link": "https://example.edu/images/habitat-logo.png",
            "Description": "Building homes and hope in our local community through volunteer construction projects and fundraising efforts.",
            "Email": "habitat@example.edu", 
            "Phone Number": "",
            "LinkedIn Link": "https://linkedin.com/company/habitat-example",
            "Instagram Link": "https://instagram.com/habitat_example",
            "Facebook Link": "https://facebook.com/habitat.example",
            "Twitter Link": "",
            "YouTube Link": "https://youtube.com/c/habitat-example",
            "TikTok Link": ""
        },
        {
            "Category": "Religious",
            "Organization Name": "Interfaith Campus Ministry",
            "Organization Link": "https://example.edu/organizations/interfaith",
            "Logo Link": "",
            "Description": "Bringing together students of all faith traditions for dialogue, service, and spiritual growth.",
            "Email": "interfaith@example.edu",
            "Phone Number": "555-456-7890",
            "LinkedIn Link": "",
            "Instagram Link": "",
            "Facebook Link": "https://facebook.com/interfaith.example",
            "Twitter Link": "",
            "YouTube Link": "",
            "TikTok Link": ""
        }
    ]
    
    return sample_organizations

def main():
    """Run the demo"""
    print("University Organization Scraper - Excel Demo")
    print("=" * 50)
    
    # Create sample data
    print("Creating sample organization data...")
    sample_data = create_sample_data()
    print(f"✓ Created {len(sample_data)} sample organizations")
    
    # Generate Excel file
    print("\nGenerating Excel file...")
    excel_gen = ExcelGenerator()
    
    # Validate the data
    cleaned_data = excel_gen.validate_organizations_data(sample_data)
    print(f"✓ Validated {len(cleaned_data)} organizations")
    
    # Create Excel file
    filename = excel_gen.create_excel_file("Demo University", cleaned_data)
    
    if filename:
        print(f"✓ Successfully created Excel file: {filename}")
        
        # Display summary of created file
        print(f"\nFile Details:")
        print(f"  - Filename: {filename}")
        print(f"  - Organizations: {len(cleaned_data)}")
        print(f"  - Data Fields: {len(ORGANIZATION_FIELDS)}")
        
        print(f"\nSample Organizations:")
        for i, org in enumerate(cleaned_data[:3], 1):
            print(f"  {i}. {org['Organization Name']} ({org['Category']})")
        
        if len(cleaned_data) > 3:
            print(f"  ... and {len(cleaned_data) - 3} more")
        
        print(f"\nExcel file '{filename}' is ready for review!")
        
    else:
        print("✗ Failed to create Excel file")
    
    print("\n" + "=" * 50)
    print("Demo completed successfully!")

if __name__ == "__main__":
    main()