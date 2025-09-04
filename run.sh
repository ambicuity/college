#!/bin/bash

# University Organization Scraper - Setup and Run Script

echo "University Organization Scraper Setup"
echo "====================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python 3 found: $(python3 --version)"

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "Dependencies installed successfully"

# Run tests
echo ""
echo "Running tests..."
python3 test_scraper.py

# Ask user if they want to run the full scraper
echo ""
read -p "Do you want to run the full scraper for all universities? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting full university scraping..."
    python3 main.py
else
    echo "Skipping full scrape. You can run it manually with: python3 main.py"
fi

echo "Setup completed!"