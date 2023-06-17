from scrapy.crawler import CrawlerProcess
from spider import CharterSpider  # Make sure to adjust the import statement based on your project structure
import pandas as pd


def run_spider(start_urls):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',  # Add more settings as needed
        'FEED_FORMAT': 'csv',  # Output format
        'FEED_URI': 'crawler_result.csv',  # Output file
    })

    process.crawl(CharterSpider, start_urls=start_urls)
    process.start()

if __name__ == "__main__":
    
    input_data = pd.read_csv("../processed_data/merge_charter_district.csv")
    start_urls=list(input_data['school_homepage'])
    print(start_urls)
    # Replace with your actual start URLs
    run_spider(start_urls)
