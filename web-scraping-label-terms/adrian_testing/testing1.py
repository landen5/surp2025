from bs4 import BeautifulSoup
import requests
import re
# import ssl


header = header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.106 Safari/537.36"
}

# create a master dictionary to store info in from each website
# List Order: ["Count (for data type)", "App functionality", "Analytics", "Developer communications", # "Advertising or marketing",
# "Fraud prevention, security, and compliance", "Personalization", "Account management"]
master_dict = {
               "Data shared": {
               
               "Location" : {"Count": 0,
                    "Approximate location": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Precise location": [0, 0, 0, 0, 0, 0, 0, 0]},
                
                "Personal info": {"Count": 0,
                    "Name": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Email address": [0, 0, 0, 0, 0, 0, 0, 0],
                    "User IDs": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Address": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Phone number": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Race and ethnicity": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Political or religious beliefs": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Sexual orientation": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Other info": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Financial info": {"Count": 0,
                    "User payment info": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Purchase history": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Credit score": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Other financial info": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Health and fitness": {"Count": 0,
                    "Health info": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Fitness info": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Messages": {"Count": 0,
                    "Emails": [0, 0, 0, 0, 0, 0, 0, 0],
                    "SMS or MMS": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Other in-app messages": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Photos and videos": {"Count": 0,
                    "Photos": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Videos": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Audio": {"Count": 0,
                    "Voice or sound recordings": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Music files": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Other audio files": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Files and docs": {"Count": 0,
                    "Files and docs": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Calendar": {"Count": 0,
                    "Calendar events": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Contacts": {"Count": 0,
                    "Contacts": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "App activity": {"Count": 0,
                    "App interactions": [0, 0, 0, 0, 0, 0, 0, 0],
                    "In-app search history": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Installed apps": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Other user-generated content": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Other actions": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Web browsing": {"Count": 0,
                    "Web browsing history": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "App info and performance": {"Count": 0,
                    "Crash logs": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Diagnostics": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Other app performance data": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Device or other IDs": {"Count": 0,
                    "Device or other IDs": [0, 0, 0, 0, 0, 0, 0, 0]}
                },



               "Data collected": {
               
               "Location" : {"Count": 0,
                    "Approximate location": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Precise location": [0, 0, 0, 0, 0, 0, 0, 0]},
                
                "Personal info": {"Count": 0,
                    "Name": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Email address": [0, 0, 0, 0, 0, 0, 0, 0],
                    "User IDs": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Address": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Phone number": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Race and ethnicity": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Political or religious beliefs": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Sexual orientation": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Other info": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Financial info": {"Count": 0,
                    "User payment info": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Purchase history": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Credit score": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Other financial info": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Health and fitness": {"Count": 0,
                    "Health info": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Fitness info": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Messages": {"Count": 0,
                    "Emails": [0, 0, 0, 0, 0, 0, 0, 0],
                    "SMS or MMS": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Other in-app messages": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Photos and videos": {"Count": 0,
                    "Photos": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Videos": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Audio": {"Count": 0,
                    "Voice or sound recordings": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Music files": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Other audio files": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Files and docs": {"Count": 0,
                    "Files and docs": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Calendar": {"Count": 0,
                    "Calendar events": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Contacts": {"Count": 0,
                    "Contacts": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "App activity": {"Count": 0,
                    "App interactions": [0, 0, 0, 0, 0, 0, 0, 0],
                    "In-app search history": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Installed apps": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Other user-generated content": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Other actions": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Web browsing": {"Count": 0,
                    "Web browsing history": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "App info and performance": {"Count": 0,
                    "Crash logs": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Diagnostics": [0, 0, 0, 0, 0, 0, 0, 0],
                    "Other app performance data": [0, 0, 0, 0, 0, 0, 0, 0]},
               
               "Device or other IDs": {"Count": 0,
                    "Device or other IDs": [0, 0, 0, 0, 0, 0, 0, 0]}
                },



               "Security practices": {
                    "Data is encrypted in transit": 0,
                    "You can request that data be deleted": 0}
            }

url= "https://play.google.com/store/apps/datasafety?id=com.instagram.android"

res= requests.get(url, headers= header)
soup = BeautifulSoup(res.text, 'html.parser')


def data_cleaner(string):
    """
    Removes "and" between two data types in google play store

    :param: list
    :return: list without extra "and's"
    """
    word_list = string.split()

    data_type = []
    word_index = 0
    type = ""
    
    while word_index < len(word_list):
        # looking for "and" and no comma
        if word_list[word_index] == "and" and word_list[word_index + 1].isupper and type != "":
            data_type.append(type)
            type = ""
        # looking for comma
        elif word_list[word_index][-1] == ",":
            type = type + " " + word_list[word_index][0:-1]
            data_type.append(type.strip())
            type = ""
        # all else
        else:
            type = type + " " + word_list[word_index]
        word_index += 1
    return data_type



def main():
    # find collection categories
    data_collection = soup.find_all('h2',{'class':"q1rIdc"})
    for categ in data_collection:
        master_dict[categ.text] += 1


    # find data type categories
    data_col_categ = soup.find_all('h3', {'class': "aFEzEb"})
    for categ in data_col_categ:
        master_dict[categ.text] += 1


    # find data types
    data_types = soup.find_all('h4', {'class': "pcmFvf"})
    for categ in data_types:
        type = categ.text
        if len(type) >= 12 and type[-10] == "·":
            type = type[0:-11]
            master_dict[type] += 1
        else:
            master_dict[type] += 1
    

    # find purposes
    data_purposes = soup.find_all('div', {'class': "FnWDne"})
    for categ in data_purposes:
        purpose = categ.text

        category_list = []
        pattern = re.compile(r'([A-Z][^A-Z]*(?:, [^A-Z]+)*)')
        # Iterate over the match objects from pattern.finditer(purposes)
        for category in pattern.findall(purpose):
            # Remove any leading or trailing whitespace from the category
            category = category.strip()
            # Add the category to the list
            category_list.append(category)

        # remove extraneous commas
        for i in range(len(category_list)):
            category_list[i] = category_list[i].rstrip(',')
        
        # counting number of appearances for each purpose
        for elem in category_list:
            master_dict[elem] += 1


        # new_purposes = data_cleaner(categ.text)
        # print(new_purposes)

        # types_list = type_splicer(categ_list)
        # master_dict[]:
        
        # # slices data in google play store to account for only extra "and's"
        # if len(categ_list) == 1:
        #     new_list = and_check(categ_list)
        #     print(new_list)

        # # slices data in google play store to account for commas and extra "and's"
        # else:
        #     i = 0
        #     for type in categ_list:
        #         if type[0] == "a":
        #             categ_list[i] = type[4:]
        #             i += 1
        #         else:
        #             i += 1



if __name__ == "__main__":
    main()
    print(master_dict)


    # categ_list.split(", ")
    # categ_list.split(", and")
    # for type in categ_list:
        # print(type)
    # print(categ_list)
    # if 

        
    #     master_dict[categ.text] += 1

# print(master_dict)



    # print(categ.text)
# print("bye")

# result = data_collection(url)
# print(result)

# for categ in data_collection_categ:
