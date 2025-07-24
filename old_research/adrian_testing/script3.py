import requests
from bs4 import BeautifulSoup
import csv

collection_dict = {"Track": 0, "Linked": 0, "Not Linked": 0}

URL = "https://apps.apple.com/us/app/instagram/id389801252"
r = requests.get(URL)
  
soup = BeautifulSoup(r.content, 'html.parser')
res = soup.find_all("h3", {"class": "privacy-type__heading"})
list_res = []

for elem in res:
    res_initial = elem.text
    list_res.append(res_initial)

for elem in list_res:
    if elem == "Data Used to Track You":
        collection_dict["Track"] += 1
    elif elem == "Data Linked to You":
        collection_dict["Linked"] += 1
    elif elem == "Data Not Linked to You":
        collection_dict["Not Linked"] += 1

print("Data Used to Track You: " + str(collection_dict["Track"]))
print("Data Linked to You: " + str(collection_dict["Linked"]))
print("Data Not Linked to You: " + str(collection_dict["Not Linked"]))



# print(soup.prettify())


# URL = "https://apps.apple.com/us/app/instagram/id389801252"
# response = requests.get(URL)
# print(response.content)


# header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36"}
# r = requests.get(url=URL, headers=header)
# print(r.content)