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
data_shared_dict = {
               
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
                }


data_collected_dict = {
               
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
                }


security_dict = {
               "Data is encrypted in transit": 0,
               "You can request that data be deleted": 0,
               "Independent security review": 0,
               "Committed to follow the Play Families Policy": 0
               }
            

compact_label_dict = {
               "This app may share these data types with third parties": 0,
               "This app may collect these data types": 0,
               "Data is encrypted in transit": 0,
               "You can request that data be deleted": 0,
               "Independent security review": 0,
               "Committed to follow the Play Families Policy": 0
               }


expanded_label_dict = {
               "Data shared": 0, "Data collected": 0, "Security practices": 0,
               "Location" : 0, "Personal info": 0, "Financial info": 0, "Health and fitness": 0, "Messages": 0,
               "Photos and videos": 0, "Audio": 0, "Files and docs": 0, "Calendar": 0, "Contacts": 0,
               "App activity": 0, "Web browsing": 0, "App info and performance": 0, "Device or other IDs": 0,
               "Approximate location": 0, "Precise location": 0, "Name": 0, "Email address": 0, "User IDs": 0,
               "Address": 0, "Phone number": 0, "Race and ethnicity": 0, "Political or religious beliefs": 0,
               "Sexual orientation": 0, "Other info": 0, "User payment info": 0, "Purchase history": 0,
               "Credit score": 0, "Other financial info": 0, "Health info": 0, "Fitness info": 0, "Emails": 0,
               "SMS or MMS": 0, "Other in-app messages": 0, "Photos": 0, "Videos": 0, "Voice or sound recordings": 0,
               "Music files": 0, "Other audio files": 0, "Files and docs": 0, "Calendar events": 0, "Contacts": 0,
               "App interactions": 0, "In-app search history": 0, "Installed apps": 0, "Other user-generated content": 0,
               "Other actions": 0, "Web browsing history": 0, "Crash logs": 0, "Diagnostics": 0,
               "Other app performance data": 0, "Device or other IDs": 0,
               "App functionality": 0, "Analytics": 0, "Developer communications": 0,
               "Advertising or marketing": 0,"Fraud prevention, security, and compliance": 0,
               "Personalization": 0, "Account management": 0,
               "Data is encrypted in transit": 0, "You can request that data be deleted": 0, "Independent security review": 0,
               "Committed to follow the Play Families Policy": 0
               }

# res= requests.get(url, headers= header)
# soup = BeautifulSoup(res.text, 'html.parser')


def scrape_appinfo(url):
     header = header = {
     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.106 Safari/537.36"
     }
     res= requests.get(url, headers= header)
     soup = BeautifulSoup(res.text, 'html.parser')

     # find collection categories
     data_collection = soup.find_all('h2',{'class':"q1rIdc"})
     for categ in data_collection:
          expanded_label_dict[categ.text] += 1


     # find data type categories
     data_col_categ = soup.find_all('h3', {'class': "aFEzEb"})
     for categ in data_col_categ:
          expanded_label_dict[categ.text] += 1


     # find data types
     data_types = soup.find_all('h4', {'class': "pcmFvf"})
     for categ in data_types:
          type = categ.text
          if len(type) >= 12 and type[-10] == "·":
              type = type[0:-11]
              expanded_label_dict[type] += 1
          else:
              expanded_label_dict[type] += 1
    

     # find purposes
     data_purposes = soup.find_all('div', {'class': "FnWDne"})
     for categ in data_purposes:
          purpose = categ.text
          print(purpose)
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
              expanded_label_dict[elem] += 1



def main():
     scrape_appinfo("https://play.google.com/store/apps/datasafety?id=com.instagram.android")
     # print(expanded_label_dict)




if __name__ == "__main__":
     main()