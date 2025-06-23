import requests
import json
from bs4 import BeautifulSoup
import re
import os
import time
import queue


def similar_app_scraper(url):
    """
    param: takes an app url
    return: returns list of urls of similar apps
    """
    # takes initial app URL from details page

    header ={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.106 Safari/537.36"
    }
    
    prefix = "https://play.google.com"

    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')
    app_url_list = []
    for link in soup.find_all('a', {'jsname': "hSRGPd", 'class': "WpHeLc VfPpkd-mRLv6", 'href': re.compile("^/store/apps/collection")}):
        similar_url = link.get('href')
        similar_url = prefix + similar_url
    
    # takes link from above and acquires URLs from similar apps
    try:
        new_res = requests.get(similar_url, headers=header)
        new_soup = BeautifulSoup(new_res.text, 'html.parser')
    except UnboundLocalError:
        return
    
    for link in new_soup.find_all('a', {'class': "Si6A0c ZD8Cqc", 'href': re.compile("^/store/apps/details")}):
        temp_url = link.get('href')
        app_url_list.append(prefix + temp_url)

    return app_url_list


def main():

    starting_links = ["https://play.google.com/store/apps/details?id=com.snapchat.android"]


    processed_apps = {}

    master_queue = queue.SimpleQueue()
    for link in starting_links:  # takes links from starting page and puts them into the master queue
        master_queue.put(link)
    while not master_queue.empty():
        url = master_queue.get()
        # scrape = AndroidScraper(url)
        # scrape.scrape_data()
        # scrape.write_to_json()
        more_urls = similar_app_scraper(url)  # finds similar app URLs
        processed_apps[url] = True  # signals that current URL has been analyzed
        print(f"app processed: {url}")
        for new_link in more_urls:
            if new_link not in processed_apps.keys():
                master_queue.put(new_link)


    # # for class purposes
    # master_queue = queue.SimpleQueue()
    # for link in self.starting_links:  # takes links from starting page and puts them into the master queue
    #     master_queue.put(link)
    # while not master_queue.empty():
    #     url = master_queue.get()
    #     # scrape = AndroidScraper(url)
    #     # scrape.scrape_data()
    #     # scrape.write_to_json()
    #     more_urls = self.similar_app_scraper(url)  # finds similar app URLs
    #     self.processed_apps[url] = True  # signals that current URL has been analyzed
    #     print(f"app processed: {url}")
    #     for new_link in more_urls:
    #         if new_link not in self.processed_apps.keys():
    #             master_queue.put(new_link)



if __name__ == "__main__":
    main()
