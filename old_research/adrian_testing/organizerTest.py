from bs4 import BeautifulSoup
import requests
import re
# import ssl


# header = header = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.106 Safari/537.36"
# }


# url= "https://play.google.com/store/apps/datasafety?id=com.instagram.android"

# res = requests.get(url, headers=header)
# soup = BeautifulSoup(res.text, 'html.parser')

# data_collection = soup.find_all('h2', {'class': "q1rIdc"})
# data_dict = {}

def app_scrape(url, section):
    """
    """
    # Find the next sibling div element with class "XgPdwe"
    y = section.find_next_sibling('div', {'class': "XgPdwe"})
    
    # Find all h3 elements with class "aFEzEb" within the div element
    h3_elements = y.find_all('h3', {'class': "aFEzEb"})
    
    # Find all h4 elements with class "pcmFvf" within the div element
    h4_elements = y.find_all('h4', {'class': "pcmFvf"})

    # Find all div elements with class "FnWDne" within the div element
    purposes_elements = y.find_all('div', {'class': "FnWDne"})
    
    # Create an empty dictionary to store the data for the current element
    sub_dict = {}
    
    # Iterate over each h3 element within the div element
    for h3_elem in h3_elements:
        # Get the text content of the h3 element
        h3_text = h3_elem.text
        
        # Create empty lists to store the h4 texts and purposes texts
        h4_texts = []
        h4_texts_temp = []
        purposes_texts = []
        
        # Iterate over the h4 and purposes elements simultaneously
        for h4_elem, purposes_elem in zip(h4_elements, purposes_elements):
            # Check if the h4 element has a preceding h3 element that matches the current h3 element
            if h4_elem.find_previous('h3') == h3_elem:
                # Accounting for ". Optional" wording and appending the text content of the h4 element to h4_texts list
                h4_texts_temp.append(h4_elem.text)
                for type in h4_texts_temp:
                    if len(type) >= 12 and type[-10] == "·":
                        type = type[0:-11]
                        h4_texts.append(type)
                    else:
                        h4_texts.append(type)

                # Append the text content of the purposes element to purposes_texts list
                purposes_texts.append(purposes_elem.text)

        # print(purposes_texts)
        
        # differentiating between different purposes
        purposes_texts = " ".join(purposes_texts)
        new_purposes_list = []
        pattern = re.compile(r'([A-Z][^A-Z]*(?:, [^A-Z]+)*)')
        # Iterate over the match objects from pattern.finditer(purposes)
        for category in pattern.findall(purposes_texts):
            # Remove any leading or trailing whitespace from the category
            category = category.strip()
            # Add the category to the list
            new_purposes_list.append(category)
        # remove extraneous commas
        for i in range(len(new_purposes_list)):
            new_purposes_list[i] = new_purposes_list[i].rstrip(',')
        # print(new_purposes_list)

        # Create a dictionary to store data items and their corresponding purposes
        data_items = {}

        # Iterate over each data item and purpose, and add them to the data_items dictionary
        for data in h4_texts:
            temp_list = [0, 0, 0, 0, 0, 0, 0, 0]
            temp_list[0] += 1
            # purpose_found = False
            # while not purpose_found:
            for purpose in new_purposes_list:
                if purpose == "App functionality" and temp_list[1] != 1:
                    temp_list[1] += 1
                elif purpose == "Analytics" and temp_list[2] != 1:
                    temp_list[2] += 1
                elif purpose == "Developer communications" and temp_list[3] != 1:
                    temp_list[3] += 1
                elif purpose == "Advertising or marketing" and temp_list[4] != 1:
                    temp_list[4] += 1
                elif purpose == "Fraud prevention, security, and compliance" and temp_list[5] != 1:
                    temp_list[5] += 1
                elif purpose == "Personalization" and temp_list[6] != 1:
                    temp_list[6] += 1
                elif purpose == "Account management" and temp_list[7] != 1:
                    temp_list[7] += 1
                
                # data_items[data] = [purpose]
                data_items[data] = temp_list
                # print(data_items)
        
        # Add the data_items dictionary to the sub_dict with h3_text as the key
        sub_dict[h3_text] = data_items

# Print the resulting data_dict
# print(data_dict)

def main():
    header = header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.106 Safari/537.36"
    }


    url= "https://play.google.com/store/apps/datasafety?id=com.instagram.android"

    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')

    data_collection = soup.find_all('h2', {'class': "q1rIdc"})
    for elem in data_collection:
        # print(elem)
        if elem.text == "Data shared":
            data_shared_dict = app_scrape(url, elem)
            # print(data_shared_dict)
        elif elem.text == "Data collected":
            data_collected_dict = app_scrape(url, elem)
            # print(data_collected_dict)
        elif elem.text == "Security practices":
            security_practices_dict = app_scrape(url, elem)
            # print(security_practices_dict)


if __name__ == "__main__":
     main()


# find a way to add +1 to dictionaries instead of adding word itself