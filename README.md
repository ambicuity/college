# University Student Organizations Web Scraper

An advanced AI web scraping agent designed to systematically collect student organization data from university websites and compile it into structured Excel files.

## Features

- **Multi-University Support**: Scrapes data from 11 target universities
- **Comprehensive Data Extraction**: Collects 13 different data fields per organization
- **Flexible Website Compatibility**: Handles various website platforms (Engage, Campus Labs, Presence, etc.)
- **Excel Output**: Generates professional Excel files with proper formatting
- **Error Handling**: Robust error handling and logging
- **Selenium Support**: Uses both requests and Selenium for dynamic content

## Target Universities

1. Bethesda University
2. Bethune-Cookman University  
3. Beulah Heights University
4. Bevill State Community College
5. Big Bend Community College
6. Biola University
7. Bishop State Community College
8. Black Hills State University
9. Blackfeet Community College
10. Bladen Community College
11. Blue Mountain Community College

## Data Fields Extracted

For each student organization, the scraper extracts:

- **Category**: Type of organization (Academic, Cultural, Sports, etc.)
- **Organization Name**: Full official name
- **Organization Link**: URL to organization's detail page
- **Logo Link**: Direct URL to organization's logo image
- **Description**: Organization's mission and purpose
- **Email**: Primary contact email
- **Phone Number**: Contact phone number
- **LinkedIn Link**: Official LinkedIn page
- **Instagram Link**: Official Instagram profile
- **Facebook Link**: Official Facebook page
- **Twitter Link**: Official Twitter/X profile  
- **YouTube Link**: Official YouTube channel
- **TikTok Link**: Official TikTok profile

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd college
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the setup script (optional):**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

## Usage

### Quick Test
Test the functionality with a single university:
```bash
python3 test_scraper.py
```

### Full Scraping
Run the complete scraping process for all universities:
```bash
python3 main.py
```

### Output Files
The scraper generates:
- Individual Excel files for each university: `[University Name] - Organizations.xlsx`
- A summary report: `Scraping_Summary_[timestamp].xlsx`
- Detailed logs: `university_scraper_[timestamp].log`

## Configuration

### University Settings
Edit `config.py` to modify:
- University domains and potential URL paths
- Data fields to extract
- Platform-specific selectors
- Social media patterns

### Example Configuration
```python
{
    "name": "Example University",
    "domain": "example.edu",
    "potential_paths": [
        "/student-life/clubs",
        "/campus-life/organizations",
        "/clubs"
    ]
}
```

## Architecture

### Core Components

1. **`main.py`**: Main orchestration script
2. **`web_scraper.py`**: Web scraping logic and data extraction
3. **`excel_generator.py`**: Excel file creation and formatting
4. **`config.py`**: Configuration and university data
5. **`test_scraper.py`**: Test suite for validation

### Key Features

- **Adaptive Scraping**: Automatically detects website platforms
- **Pagination Support**: Handles "Next Page" navigation
- **Dynamic Content**: Uses Selenium for JavaScript-heavy sites
- **Data Validation**: Cleans and validates extracted data
- **Professional Output**: Creates formatted Excel files

## Error Handling

The scraper handles common issues:
- Dead links and 404 errors
- CAPTCHA and login walls
- Missing organization data
- Network timeouts
- JavaScript-dependent content

## Logging

Comprehensive logging includes:
- University processing status
- Organizations found per university
- Error details and stack traces
- Performance metrics
- Summary statistics

## Requirements

- Python 3.7+
- Chrome browser (for Selenium)
- Internet connection
- Required Python packages (see requirements.txt)

## Legal and Ethical Considerations

- Only scrapes publicly accessible information
- Respects robots.txt and rate limiting
- Includes delays between requests
- Does not bypass authentication or paywalls

## Troubleshooting

### Common Issues

1. **Chrome driver not found**
   - The script automatically downloads ChromeDriver
   - Ensure Chrome browser is installed

2. **No organizations found**
   - Check university URL paths in config.py
   - Verify website structure hasn't changed
   - Review logs for detailed error information

3. **Selenium timeouts**
   - Increase timeout values in web_scraper.py
   - Check internet connection stability

### Getting Help

1. Check the log files for detailed error information
2. Run the test script to isolate issues
3. Verify university websites are accessible manually

## Contributing

To add support for additional universities:

1. Research the university's student organizations page
2. Add university configuration to `config.py`
3. Test with `test_scraper.py`
4. Update documentation

## License

This project is intended for educational and research purposes. Please respect website terms of service and applicable laws when using this tool.