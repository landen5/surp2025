import requests
import json
from bs4 import BeautifulSoup
import re

class AndroidScraper:
    def __init__(self, compact_url, header):
        self.compact_url = compact_url
        self.header = header
        self.expanded_dict = {}
        self.compact_dict = {}
        self.info_collection = {
            "App name": "",
            "App category": "",
            "URL": "",
            "App ID": ""
            }


    # scrapes expanded label info
    def scrape_expanded_label(self):
        # determine expanded label url
        expanded = self.compact_url.split("details?")
        expanded_url = "datasafety?".join(expanded)

        res = requests.get(expanded_url, headers=self.header)
        soup = BeautifulSoup(res.text, 'html.parser')

        data_collection = soup.find_all('h2', {'class': "q1rIdc"})

        for elem in data_collection:
            y = elem.find_next_sibling('div', {'class': "XgPdwe"})

            h3_elements = y.find_all('h3', {'class': "aFEzEb"})
            h4_elements = y.find_all('h4', {'class': "pcmFvf"})
            purposes_elements = y.find_all('div', {'class': "FnWDne"})

            sub_dict = {}

            for h3_elem in h3_elements:
                h3_text = h3_elem.text
                h4_texts = []
                h4_texts_temp = []
                purposes_texts = []

                for h4_elem, purposes_elem in zip(h4_elements, purposes_elements):
                    if h4_elem.find_previous('h3') == h3_elem:
                        h4_texts_temp.append(h4_elem.text)
                        for type in h4_texts_temp:
                            if len(type) >= 12 and type[-10] == "·":
                                type = type[0:-11]
                                h4_texts.append(type)
                            else:
                                h4_texts.append(type)

                        purposes_texts.append(purposes_elem.text)

                # removes duplicates from list
                h4_texts = list(dict.fromkeys(h4_texts))

                data_items = {}
                for data, purpose in zip(h4_texts, purposes_texts):
                    data_items[data] = [purpose]

                sub_dict[h3_text] = data_items

            self.expanded_dict[elem.text] = sub_dict


    # scrapes compact label info
    def scrape_compact_label(self):
        res = requests.get(self.compact_url, headers=self.header)
        soup = BeautifulSoup(res.text, 'html.parser')

        # find compact label info
        raw_data = soup.find_all('div', {'class': "wGcURe"})
        for elem in raw_data:
            print(elem.text)
            compact_list = re.split(r'(?<=[a-z])(?=[A-Z])', elem.text, 1)
            print(compact_list)
            
            # accounting for labels with no description (ex. data can be deleted)
            if len(compact_list) > 1:
                self.compact_dict[compact_list[0]] = compact_list[1]
            else:
                self.compact_dict[compact_list[0]] = None


    # scrapes app name, app category, url, and app ID
    def scrape_app_info(self):
        res = requests.get(self.compact_url, headers=self.header)
        soup = BeautifulSoup(res.text, 'html.parser')

        # find app name
        name_data = soup.find('h1', {'class': "Fd93Bb ynrBgc xwcR9d"})
        app_name = name_data.text
        self.info_collection["App name"] = app_name

        # find app categories
        category_data = soup.find_all('div', {'class': "Uc6QCc"})
        for elem in category_data:
            category_list = re.findall('[A-Z][^A-Z]*', elem.text)
            self.info_collection["App category"] = category_list
        
        # find app url
        for link in soup.find_all('link', {'rel': "canonical", 'href': re.compile("^https://")}):
            app_url = link.get('href')
            self.info_collection["URL"] = app_url

        # find app ID
        ID_data = app_url.split("details?")
        app_ID = ID_data[1]
        self.info_collection["App ID"] = app_ID


    # uploads expanded label info to json file
    def save_el_data_to_file(self, filename):
        # Serializing json
        json_object = json.dumps(self.expanded_dict, indent=4)
        with open(filename, 'w') as file:
            json.dump(self.expanded_dict, file)
            file.write(json_object)


    # uploads compact label info to json file
    def save_cl_data_to_file(self, filename):
    # Serializing json
        json_object = json.dumps(self.compact_dict, indent=4)
        with open(filename, 'w') as file:
            json.dump(self.compact_dict, file)
            file.write(json_object)


    # uploads other key app info to json file
    def save_ai_data_to_file(self, filename):
        # Serializing json
        json_object = json.dumps(self.info_collection, indent=4)
        with open(filename, 'w') as file:
            json.dump(self.info_collection, file)
            file.write(json_object)
    

    def get_expanded_dict(self):
        return self.expanded_dict
    

    def get_compact_dict(self):
        return self.compact_dict


    def get_app_info(self):
        return self.info_collection


def main():
    # compact label url
    compact_url= "https://play.google.com/store/apps/details?id=com.instagram.android&hl=en_US&gl=US"
    # compact_url = "https://play.google.com/store/apps/details?id=com.google.android.apps.maps&hl=en_US&gl=US"
    # compact_url = "https://play.google.com/store/apps/details?id=com.rovio.baba&hl=en_US&gl=US"
    # compact_url = "https://play.google.com/store/apps/details?id=org.pbskids.video&hl=en_US&gl=US"

    

    header ={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.106 Safari/537.36"
    }

    insta = AndroidScraper(compact_url, header)

    el_file = "android_expanded_label_data.json"
    cl_file = "android_compact_label_data.json"
    ai_file = "android_app_info_data.json"


    # gets expanded label info
    insta.scrape_expanded_label()
    insta.save_el_data_to_file(el_file)

    # gets compact label info
    insta.scrape_compact_label()
    insta.save_cl_data_to_file(cl_file)

    # gets other key app info
    insta.scrape_app_info()
    insta.save_ai_data_to_file(ai_file)

    # print(el_dict)

    # gets compact label info
    # insta.scrape_compact_label()
    # insta.save_data_to_file(filename2)
    # # print(cl_dict)

    # # gets other key app info
    # insta.scrape_app_info()
    # insta.save_data_to_file(filename3)
    # # print(ai_dict)

    # # save data to a json file
    # insta.save_data_to_file(filename)

if __name__ == "__main__":
    main()
