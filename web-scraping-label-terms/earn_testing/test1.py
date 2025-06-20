from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import requests 

def scrape(url):
    # Set up the WebDriver
    s=Service('/Users/earnsmacbookair/Desktop/chromedriver_mac64/chromedriver')  # creating selenium service
    driver = webdriver.Chrome(service=s) # creating web browser instance 

    # Open the url
    driver.get(url)

    # Wait for the page to load completely
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "modal-trigger-ember17")))

    # Click the button to open the pop up
    button = driver.find_element(By.ID, "modal-trigger-ember17")  # Or use find_element_by_class_name, if you prefer
    button.click()

    # Now the pop up should be open, so you can get its content
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Use BeautifulSoup to find the content you want
    # content = soup.find_all("h2", {'class': "privacy-type__heading"})
    content = soup.find_all("h3", {'class': "privacy-type__data-category-heading"})


    # Make sure to close the driver after you're done with it
    driver.quit()

    # Return the content you found
    return content
            
               

def main():
    print(scrape("https://apps.apple.com/us/app/instagram/id389801252"))

if __name__ == "__main__":
    main()
    
"body", {'class': "globalnav-scrim ember-application has-js no-touch has-modal--page-overlay"}
"div", {'class' : "we-modal we-modal--page-overlay we-modal--open app-privacy--modal privacy-type--modal"}
"div", {'class': "we-modal__content large-10 medium-12 "}
"div", {'class': "we-modal__content__wrapper"}
"div", {'class': "app-privacy__modal-section"}


"h2", {'class': "privacy-type__heading"}
"h3", {'class': "privacy-type__data-category-heading"}
"ul", {'class': "privacy-type__category-items"}



"h3", {'class': "privacy-type__purpose-heading"}
"h3", {'class': "privacy-type__data-category-heading"}





"a", {'class': "inline-list__item"}


'span', {'class': "we-localnav__title__qualifier"}

