import requests
import json
from bs4 import BeautifulSoup
import re
import os
import time

# def similar_url_finder(url, header):
#     """
#     Takes an app's detail page and finds the link to the list of apps with similar URLs
#     """
#     res = requests.get(url, headers=header)
#     soup = BeautifulSoup(res.text, 'html.parser')

#     for link in soup.find_all('a', {'jsname': "hSRGPd", 'href': re.compile("^/store/apps/collection")}):
#         similar_url = link.get('href')
    


def similar_app_scraper(url, header):
    """
    param: takes an app url

    return: returns list of urls of similar apps
    """

    # takes initial app URL from details page
    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')
    app_url_list = []

    for link in soup.find_all('a', {'jsname': "hSRGPd", 'class': "WpHeLc VfPpkd-mRLv6", 'href': re.compile("^/store/apps/collection")}):
        similar_url = link.get('href')
        similar_url = "https://play.google.com" + similar_url
    
    # takes link from above and acquires URLs from similar apps
    try:
        new_res = requests.get(similar_url, headers=header)
        new_soup = BeautifulSoup(new_res.text, 'html.parser')
    except UnboundLocalError:
        return


    for link in new_soup.find_all('a', {'class': "Si6A0c ZD8Cqc", 'href': re.compile("^/store/apps/details")}):
        temp_url = link.get('href')
        url_list = temp_url.split("id=")
        app_url_list.append(url_list[1])
    
    return app_url_list


# check to see if app ID is in the master list or not, and add it to the list if it is not
def url_list(master_list, new_list):

    try:
    # adds new urls to the master list of urls
        for url in new_list:
            if url not in master_list:
                master_list.append(url)
        return master_list
    
    except TypeError:
        return master_list


def main():
    # start_time = time.time()
    header ={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.106 Safari/537.36"
        }
    
    base_url = "https://play.google.com/store/apps/details?id="
    # basic_url = "https://play.google.com/store/apps/details?id=com.snapchat.android"
    master_list = ["com.snapchat.android"]
    count = 0

    # for loop that looks for similar app urls of apps in the master_list
    for url in master_list:
        # just scrapes urls for certain num of apps
        if count > 100:
            break
        full_url = base_url + url
        print(full_url)
        basic_results = similar_app_scraper(full_url, header)
        master_results = url_list(master_list, basic_results)
        count += 1

    print(master_results)
    print(len(master_results))
    
    # end_time = time.time()
    # print(end_time-start_time)


if __name__ == "__main__":
    main()
