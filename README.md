# Web Scraping Tool

This Python script is a simple web scraper designed to extract information from a website and save it to a CSV file. The script uses the `requests`, `BeautifulSoup`, and `pandas` libraries to make HTTP requests, parse HTML content, and manage data, respectively.

## Prerequisites

Make sure you have Python installed on your machine. If not, you can download it from [python.org](https://www.python.org/).

Install the required Python libraries using the following command:

```bash
pip install requests beautifulsoup4 pandas
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/moonnight90/whereorg.git
cd whereorg
```

2. Run the script:

```bash
python main.py
```

3. Enter the main category link when prompted.

## Configuration

- `OUTPUT_FILE`: The name of the CSV file where the scraped data will be saved (`Data.csv` by default).

## Script Explanation

- The script defines a `Scraper` class with methods for making HTTP requests, creating BeautifulSoup objects, extracting text from HTML elements, and scraping links.
- The `filter_categories` method filters and scrapes links based on specified categories.
- The `filter_location` method filters and scrapes links based on location.
- The `run` method initiates the scraping process.

## Disclaimer

This script is provided as-is, and the user should review and comply with the terms of service of the website being scraped. Unauthorized web scraping may violate the terms of service of the website and legal regulations. Use this script responsibly and only for ethical purposes. The author is not responsible for any misuse or legal consequences resulting from the use of this script.