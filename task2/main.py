from scraper import *

gsp = GoogleSearchScraper()
gsp.set_keywords_from_file("keywords.txt")
gsp.query()