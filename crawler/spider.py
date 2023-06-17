import scrapy
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse

class CharterSpider(scrapy.Spider):
    name = "charter_spider"

    custom_settings = {
        'DEPTH_LIMIT': 2,  # Limit the depth of the scraping to only one level
    }

    def __init__(self, start_urls=None, *args, **kwargs):
        super(CharterSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls if start_urls is not None else []
        self.link_limit = 40  # Set the desired link limit
        self.keywords = ['calendar', 'events', 'schedule']  # Add more keywords as needed
        self.visited_urls = set()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'link_counter': 0, 'root_domain': urlparse(url).netloc})

    def parse(self, response):
        link_counter = response.meta.get('link_counter', 0)
        root_domain = response.meta.get('root_domain')
        link_extractor = LinkExtractor(allow_domains=root_domain)
        links = link_extractor.extract_links(response)

        for link in links:
            url = link.url
            # Process the link further if it doesn't match the calendar keywords
            if any(keyword in url.lower() for keyword in self.keywords):
                continue

            if url not in self.visited_urls:
                if link_counter >= self.link_limit:
                    break  # Break the loop if the link limit is reached
                

                yield scrapy.Request(url, callback=self.parse_link, meta={'link_counter': link_counter, 'root_domain': root_domain})

                # yield {
                #     "url": url
                # }

                # self.visited_urls.add(url)
                link_counter += 1  # Increment the link counter

        # To follow links
        for link in links:
            if link.url not in self.visited_urls and link_counter < self.link_limit:
                yield response.follow(link.url, self.parse, meta={'link_counter': link_counter, 'root_domain': root_domain})
    
    def parse_link(self, response):
        if response.status == 200:  # replace with whatever status code you want to check for
            self.visited_urls.add(response.url)
            yield {
                "url": response.url,
        }