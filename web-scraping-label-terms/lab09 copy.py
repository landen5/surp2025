"""
    CS051P Lab Assignments: Lab09 - Working with the Web

    Author: Nannapas Wonghirundacha

    Date:   11/21/2021

    The goal of this assignment is to give you experience working
    with data from websites.  You'll use the BeautifulSoup package
    and will also practice using dictionaries, lists, and tuples.
"""
from bs4 import BeautifulSoup
import requests


def num_results_google(string):
    """
    This function takes a string and returns an integer. The function accesses a google url and opens up the html file.
    It finds the tag and the attribute of the search result number then takes the result and turns it
    into an integer.

    :param string: string, added to the end of the URL, what the user searches for
    :return: integer, -1 when the search result doesn't exist
    """
    # write the header
    header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" +
                            "AppleWebKit/605.1.15 (KHTML, like Gecko)" + "Version/14.1.2 Safari/605.1.15"}

    # when there isn't space in the the phrase
    if " " not in string:
        url = "https://www.google.com/search?q=" + string
        res = requests.get(url, headers=header)
        if res.status_code == requests.codes.ok:
            soup = BeautifulSoup(res.text, "html.parser")
            # find the tag and attribute for the search result
            if not soup.find("div", {'id': "result-stats"}):
                # when the search result doesn't exist
                return -1
            # when the search result does exist
            else:
                out = soup.find("div", {'id': "result-stats"})
                # change the tag into a string
                out_str = out.text
                # split the sentence into a list
                list1 = out_str.split()
                # take out the comma in the string and turn it into an integer
                integer = int(list1[1].replace(",", ""))
                return integer

    # when the phrase does have a space
    else:
        # split the string into a list
        url_list = string.split()
        url = "https://www.google.com/search?q="

        # empty string for the end of url
        end = ""
        # for loop into the list to access each word
        for elem in url_list:
            # format the words into the correct syntax for url
            end = end + elem + "+"
            end_of_url = end.rstrip("+")
        url = url + '"' + end_of_url + '"'
        res = requests.get(url, headers=header)

        if res.status_code == requests.codes.ok:
            soup = BeautifulSoup(res.text, "html.parser")
            # find the attribute and key for the search result
            if not soup.find("div", {'id': "result-stats"}):
                # when there is no search result
                return -1
            # when there is a search result
            else:
                out = soup.find("div", {'id': "result-stats"})
                # make tag into a string
                out_str = out.text
                # split the sentence into a list
                list1 = out_str.split()
                # take out the comma in the string and turn it into an integer
                integer = int(list1[1].replace(",", ""))
                return integer


def num_results_yahoo(string):
    """
    This function takes a string and returns an integer. The function accesses a yahoo url and opens up the html file.
    It finds the tag and the attribute of the search result number then takes the result and turns it
    into an integer.

    :param string: string, added to the end of the URL, what the user searches for
    :return: integer, -1 when the search result doesn't exist
    """
    # write the header
    header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" +
                            "AppleWebKit/605.1.15 (KHTML, like Gecko)" + "Version/14.1.2 Safari/605.1.15"}

    # when there isn't space in the the phrase
    if " " not in string:
        url = "https://search.yahoo.com/search?p=" + string
        res = requests.get(url, headers=header)
        if res.status_code == requests.codes.ok:
            soup = BeautifulSoup(res.text, "html.parser")
            # find the tag and attribute for the search result
            if not soup.find("span", {'class': "fz-14 lh-22"}):
                # when the search result does not exist
                return -1
            # when the search result does exist
            else:
                out = soup.find("span", {'class': "fz-14 lh-22"})
                # change the tag into a string
                out_str = out.text
                # split the string into a list
                list1 = out_str.split()
                # take out the comma in the string and turn it into an integer
                integer = int(list1[1].replace(",", ""))
                return integer

    else:
        # split the string into a list
        url_list = string.split()
        url = "https://search.yahoo.com/search?p="

        # empty string for the end of url
        end = ""
        # for loop into the list to access each word
        for elem in url_list:
            # format the words into the correct syntax for url
            end = end + elem + "+"
            end_of_url = end.rstrip("+")
        url = url + '"' + end_of_url + '"'
        res = requests.get(url, headers=header)

        if res.status_code == requests.codes.ok:
            soup = BeautifulSoup(res.text, "html.parser")
            if not soup.find("span", {'class': "fz-14 lh-22"}):
                # when there is no search result
                return -1
            # when there is a search result
            else:
                # find the tag and attribute for the search result
                out = soup.find("span", {'class': "fz-14 lh-22"})
                # make tag into a string
                out_str = out.text
                # make string into a list
                list1 = out_str.split()
                # take out the comma in the string and turn it into an integer
                integer = int(list1[1].replace(",", ""))
                return integer


def count_compare(words):
    """
    This function takes a list of strings and returns a dictionary which maps each
    string in the list to a 2-element tuple.

    :param words: list, list of strings
    :return: dictionary, key = string - value = 2 element tuple
    """
    # create an empty dictionary
    dict1 = {}

    # loop into the list to access each string
    for elem in words:
        # call functions and create a tuple
        t = (num_results_google(elem), num_results_yahoo(elem))
        # make a dictionary
        if elem in dict1.keys():
            dict1[elem] = t
        else:
            dict1[elem] = t

    return dict1


def main():
    """
    1. Repeatedly ask the user for phrases, stopping when the user enters -1.
    2. Call count_compare on a list of the entered phrases
    3. Print the number of results for each phrase with each search engine

    :return: none
    """
    # make an empty list
    phrase_list = []

    # ask user for a phrase
    phrase = input("Enter a phrase (-1 to stop)\n")
    # append input to list - remove any white spaces, make it lowercase
    phrase_list.append(phrase.rstrip().lstrip().lower())
    # loop to continuously ask for the phrase
    while phrase != "-1":
        phrase = input("Enter a phrase (-1 to stop)\n")
        phrase.rstrip(" ")
        # append input to list - remove any white spaces, make it lowercase
        phrase_list.append(phrase.rstrip().lstrip().lower())
    # remove -1 from the list
    phrase_list.remove("-1")
    print("\n")

    # call the count compare function
    compare_dict = count_compare(phrase_list)
    # loop to print out results from the search engine
    for i in compare_dict:
        print(i + ": " + str(compare_dict[i][0]) + " (google)" + ", " + str(compare_dict[i][1]) + " (yahoo)")


if __name__ == "__main__":
    main()

