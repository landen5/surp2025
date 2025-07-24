import requests
from bs4 import BeautifulSoup
import re
import time
import json
from infoCompiler import AndroidScraper
import queue
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class WebScraper:
    def __init__(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.106 Safari/537.36"
            }
        self.processed_apps = {}
        self.starting_links = []

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-images")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument("--disable-blink-features=AutomationControlled") 
        self.driver = webdriver.Chrome(service=Service("/Users/liambayer/Desktop/chromedriver-mac-x64/chromedriver"), options=options)
        self.scrape_all_pages()

    def scrape_all_pages(self):
        # Example usage
        url = 'https://play.google.com/store/apps'
        self.driver.get(url)
        prefix = "https://play.google.com"

        old_scroll_position = 0
        new_scroll_position = None

        while new_scroll_position != old_scroll_position:
            old_scroll_position = self.driver.execute_script("return window.scrollY;")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_scroll_position = self.driver.execute_script("return window.scrollY;")
            

        # Create BeautifulSoup object with the page source
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # Scrape the desired data
        links = soup.find_all("a", {'class':"Si6A0c ZD8Cqc"})
        self.starting_links.extend([prefix + link['href'] for link in links if 'href' in link.attrs])
 

    # processed_apps is different than apps that are initially scraped
    def similar_app_scraper(self, url):
        """
        param: takes an app url

        return: returns list of urls of similar apps
        """

        # takes initial app URL from details page
        res = requests.get(url, headers=self.header)
        soup = BeautifulSoup(res.text, 'html.parser')
        app_url_list = []
        prefix = "https://play.google.com"
        for link in soup.find_all('a', {'jsname': "hSRGPd", 'class': "WpHeLc VfPpkd-mRLv6", 'href': re.compile("^/store/apps/collection")}):
            half_url = link.get('href')
            similar_url = prefix + half_url

        # takes link from above and acquires URLs from similar apps
        try:
            new_res = requests.get(similar_url, headers=self.header)
            new_soup = BeautifulSoup(new_res.text, 'html.parser')
        except UnboundLocalError:
            return


        for link in new_soup.find_all('a', {'class': "Si6A0c ZD8Cqc", 'href': re.compile("^/store/apps/details")}):
            temp_url = link.get('href')
            app_url_list.append(prefix + temp_url)
        
        return app_url_list
    

    def error_to_json(self, url, error):
        """
        Writes error links to a JSON file.
        URL and error type parameters, but no return values.
        """
        directory_path = 'json_error_files'
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        app_ID = url.split("id=")
        file_path = os.path.join(directory_path, (app_ID[1] + '.json'))

        with open(file_path, "w") as file:
            json.dump(error, file)
    

    def crawl_app_links(self):
        try:
            # NEW CODE FOR QUEUES
            master_queue = queue.SimpleQueue()
            for link in self.starting_links:  # takes links from starting page and puts them into the master queue
                master_queue.put(link)
            while not master_queue.empty():
                url = master_queue.get()
                
                # handling cases where AndroidScraper runs into an error
                try:
                    scrape = AndroidScraper(url, self.driver)
                    scrape.scrape_data()
                    scrape.write_to_json()
                    print(f"app scraped: {url}")
                except Exception as e:
                    error = f"error occured while scraping at URL: {url} - {e}"
                    self.error_to_json(url, error)
                    print(error)
                
                # handling cases where it may be hard to find similar app URLs
                try:
                    more_urls = self.similar_app_scraper(url)  # finds similar app URLs
                    app_ID = url.split("id=")
                    self.processed_apps[app_ID[1]] = True  # signals that current URL has been analyzed using the app ID
                    for new_link in more_urls:  # looks to see if each URL has been scraped or not, and adds new ones to end of queue
                        if new_link not in self.processed_apps.keys():
                            master_queue.put(new_link)
                except Exception as e:
                    error = f"error occured while scraping similar URLs: {url} - {e}"
                    self.error_to_json(url, error)
                    print(error)

        # handling cases where errors occur at other points (hopefully it will not)
        except Exception as e:
            error = f"overall error occured at URL: {url} - {e}"
            self.error_to_json(url, error)
            print(error)
    

    def load_processed_apps(self, directory):
        """Loads the names of the processed apps from a given directory into the processed_apps dictionary.

        Args:
            directory (str): Directory where the JSON files are stored.
        """
        for filename in os.listdir(directory):
            if filename.endswith(".json"):  # make sure the files are .json
                app_name = filename.rstrip('.json')  # remove .json from filename to get app name
                self.processed_apps[app_name] = True



def main():
    completed_directory = "json_android_files"

    scrape = WebScraper()
    # scrape.similar_app_scraper("https://play.google.com/store/apps/details?id=com.google.android.youtube")
    scrape.load_processed_apps(completed_directory)
    scrape.crawl_app_links()
    scrape.driver.quit()
    # links = scrape.starting_links



if __name__ == "__main__":
    main()
