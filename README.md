# Toyota Parts Catalog Scraper

A Selenium-based scraper for extracting Toyota genuine parts catalog data from Partsouq.

The scraper automates the complete catalog navigation flow:
Vehicle Models, Specifications, Categories, Parts.

It extracts Toyota vehicle specifications, navigates through categories, and collects OEM part details into structured CSV files.

---

# Features

- Automated browser scraping using SeleniumBase
- Dynamic website handling with Selenium WebDriver
- Toyota model catalog extraction
- Specification extraction
- Category extraction
- OEM parts extraction
- Multi-market support
- Multi-year support
- CSV-based storage
- Resume scraping with status tracking
- Browser restart and recovery handling
- Retry mechanism for failed operations
- Cloudflare handling support

---

# Scraping Pipeline

models.csv -> Specification Extraction -> specifications.csv -> Category Extraction -> catalogs.csv -> Parts Extraction -> parts.csv

---

# Extracted Data

## Specifications

Extracted fields:
- Vehicle Model
- Year
- Destination / Market
- Specification Name
- Description
- Variant
- Options
- Production Period
- Specification URL

Example:
- Model: CAMRY
- Year: 2021
- Destination: PAKISTAN
- Specification: CAMRY HYBRID
- Production Period: 2021-2024

---

## Categories

Extracted fields:
- Vehicle Model
- Year
- Destination
- Specification
- Category Code
- Category Name
- Category URL

Example Categories:
- ENGINE
- BODY
- TRANSMISSION
- ELECTRICAL
- BRAKE SYSTEM

---

## Parts

Extracted fields:
- Vehicle Model
- Year
- Destination
- Specification
- Category
- Part Number
- Part Name
- OEM Code
- Notes
- Quantity
- Applicable Range

Example:
- Part Number: 90915-YZZD1
- Part Name: Oil Filter
- Quantity: 1

---

# Project Structure

```text
Toyota-Parts-Scraper/
├── main.py                 # Main scraper execution pipeline
├── crawler.py              # Browser automation layer
├── extractor.py            # HTML parsing and extraction logic
├── config.py               # Project configuration
│
├── data/
│   ├── models.csv          # Input Toyota models
│   ├── specifications.csv  # Extracted specifications
│   ├── catalogs.csv        # Extracted categories
│   └── parts.csv           # Extracted OEM parts
│
├── requirements.txt
└── README.md
```
---

# Installation

## Requirements

- Python 3.10+
- Google Chrome
- ChromeDriver

## Install Dependencies

pip install -r requirements.txt

---

# Configuration

Update settings inside config.py:

START_YEAR = 2016
END_YEAR = 2026
HEADLESS = False
REQUEST_DELAY_MIN = 0
REQUEST_DELAY_MAX = 0

---

# Supported Markets

The scraper supports Toyota markets including:
- Pakistan
- India
- China
- Thailand
- Indonesia
- Malaysia
- Philippines
- Vietnam
- Singapore
- Brunei
- GCC Countries
- South Korea
- Taiwan
- Hong Kong
- Mongolia
- Nepal
- Bangladesh
- Sri Lanka
- And many more

---

# Running the Scraper

Run:
python main.py

The scraper executes:
1. Extract Toyota specifications
2. Extract catalog categories
3. Extract OEM parts
4. Save results into CSV files

---

# Resume Support

Each record maintains a status:
- PENDING
- DONE
- FAILED

Example:
model,year,status
CAMRY,2021,DONE
COROLLA,2020,PENDING

Completed records are skipped automatically, allowing the scraper to continue after interruption.

---

# Technology Stack

- Browser Automation: SeleniumBase, Selenium WebDriver, Undetected Chrome automation
- Web Parsing: BeautifulSoup4, lxml
- Data Processing: Pandas, CSV
- Programming Language: Python

---

# Error Handling

The scraper includes:
- Browser health monitoring
- Automatic browser restart
- Cloudflare handling
- Retry logic
- Failed task tracking
- Safe CSV appending
- Progress persistence

---

# Future Improvements

- PostgreSQL/MySQL database storage
- Distributed scraping workers
- Proxy rotation
- API-based extraction
- Part image extraction
- Automated OEM catalog search
- Web dashboard for scraped inventory
- Advanced search and filtering system

---

# Author

Muhammad Umer
GitHub: https://github.com/Muhammad-Umer191
