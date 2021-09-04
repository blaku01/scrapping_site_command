import requests
from bs4 import BeautifulSoup
import csv


# READ KEYWORDS AND PASS THEM TO KEYWORDS LIST
class GoogleSearchScraper:

    def __init__(self):
        self._GOOGLE_Q_LINK = "https://www.google.com/search?q="
        self.site = "https://www.searchenginejournal.com/"
        self.num_of_pages = 2
        self.keywords = []
        self.links = []
        self.query_results = []
        self.nums_of_results = []
        self.num_of_results = int()

    def set_keywords_from_file(self, keywords_file):
        with open(keywords_file, 'r') as keywords:
            self.keywords = [x.strip().replace(',', '') for x in keywords.readlines()]
        self.create_links_from_keywords()

    def create_links_from_keywords(self):
        self.links = [self._GOOGLE_Q_LINK + "site:" + self.site + " " + keyword for keyword in self.keywords]

    def get_num_of_results(self, link):
        result = requests.get(link, headers={
            "Accept-Language":
                "en-US,en;q=0.9,pl-PL;q=0.8,pl;q=0.7",
            "User-Agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/80.0.3987.87 Safari/537.36 ",
        })
        assert result.status_code == 200
        src = result.content
        document = BeautifulSoup(src, 'lxml')
        num_of_results = document.find(id="result-stats")
        if num_of_results != None:
            num_of_results = num_of_results.get_text().strip()
            num_of_results = num_of_results.split('About ')[-1]
            num_of_results = num_of_results.split(' results')[0]
        else:
            num_of_results = 0
        self.num_of_results = int(num_of_results)

    def get_links_from_site(self, link):
        result = requests.get(link, headers={
            "Accept-Language":
                "en-US,en;q=0.9,pl-PL;q=0.8,pl;q=0.7",
            "User-Agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/80.0.3987.87 Safari/537.36 ",
        })
        assert result.status_code == 200
        src = result.content
        document = BeautifulSoup(src, 'lxml')
        search_results = document.find_all("div", {"class": "yuRUbf"})
        for result in search_results:
            result = result.find("a")['href']
            self.query_results.append([result])

    def save_query_as_csv(self):
        with open('query_results.csv', 'w') as f:
            write = csv.writer(f)
            write.writerows(self.query_results)
        with open('num_of_results.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(['keyword', 'num_of_results'])
            write.writerows(self.nums_of_results)

    def query(self):
        for link in self.links:
            self.get_num_of_results(link)
            google_and_site_link = self._GOOGLE_Q_LINK + "site:" + self.site
            self.nums_of_results.append([link.lstrip(google_and_site_link), self.num_of_results])
            num_of_query_pages = self.num_of_results // 10
            if num_of_query_pages < self.num_of_pages:
                for i in range(0, num_of_query_pages):
                    self.get_links_from_site(link + "&start=" + str(i*10))
            else:
                for i in range(0, self.num_of_pages):
                    self.get_links_from_site(link + "&start=" + str(i*10))
        
        save_query_as_csv(self)




