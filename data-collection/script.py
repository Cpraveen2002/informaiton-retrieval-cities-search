import os
import sys
import pip._vendor.requests as requests
import bs4
from bs4 import BeautifulSoup
import re
import warnings
import time
import codecs
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument("--log-level=3")
options.add_argument("--window-size=1920,1080")

chrome_driver = r"C:/users/arivappa/documents/seleniumDrivers/chromedriver_108.exe"
# ser = Service(chrome_driver)
# driver = webdriver.Chrome(service=ser, options=options)
driver = webdriver.Chrome(executable_path=chrome_driver, options=options)


def get_seed_urls(url):
    driver.get(url)
    innerHTML = driver.page_source
    soup = BeautifulSoup(innerHTML, 'html.parser')

    cities_file = open('cities.txt', 'a', encoding='utf-8')

    main_table = soup.find('table', attrs={'class': 'wikitable sortable jquery-tablesorter'})
    # print(main_table)
    main_body = main_table.find('tbody')
    for kk, row_elem in enumerate(main_body.find_all('tr')):
        td_elements = row_elem.find_all('td')
        anchor_tags = td_elements[1].find_all(href=True)
        req_link = anchor_tags[0]['href']
        req_link = "https://en.wikipedia.org" + req_link
        cities_file.write(req_link)
        cities_file.write("\n")
    
    cities_file.close()

def transform_to_filename(input):
    input = input.lower()
    input = input.replace(" ", "-")
    input = input.replace("_", "-")
    input = input.replace(" ", "-")
    input = input.replace(",", "-")
    input = input.replace("--", "-")
    return input

def clean_data(input):
    input = input.lower()
    input = input.replace("\n", " ").replace("\t", " ").strip()
    return input

def get_city_information(url):
    driver.get(url)
    innerHTML = driver.page_source
    soup = BeautifulSoup(innerHTML, 'html.parser')

    main_div = soup.find('div', attrs={'id': 'mw-content-text'})
    content_div = main_div.find('div', attrs={'class': 'mw-parser-output'})

    ## remove style and script components
    for style_comp in content_div.select('style'):
        style_comp.extract()
    for script_comp in content_div.select('script'):
        script_comp.extract()
    ## remove sup components
    for sup_comp in content_div.select('sup'):
        sup_comp.extract()
    ## remove contents div
    contents_div = content_div.find('div', attrs={'id': 'toc'})
    contents_div.extract()
    
    name = url[url.rfind('/')+1:]
    name = transform_to_filename(name)
    curr_file = open('./cities/' + name + ".txt", 'w', encoding='utf-8')
    curr_file.write(name)
    curr_file.write("\n")
    
    contents = content_div.findChildren(recursive=False)
    for content in contents:
        if content.name == "h2":
            if content.text.lower().find("reference") != -1:
                break
            curr_file.close()
            new_name = transform_to_filename(name + " " + content.text)
            curr_file = open('./cities/' + new_name + ".txt", 'w', encoding='utf-8')
            curr_file.write(name)
            curr_file.write("\n")
            curr_file.write(content.text)
            curr_file.write("\n")
        text = clean_data(content.text)
        curr_file.write(text)
        curr_file.write("\n")
    curr_file.close()
    # print(name)

    # pass




cities_file = open('cities.txt', 'r', encoding='utf-8')
for line in cities_file.readlines():
    link = line.replace("\n", "")
    if link == "":
        continue
    try:
        get_city_information(link)
        print("Completed " + link[link.rfind('/')+1:])
    except Exception:
        notfound_file = open('notfound.txt', 'a', encoding='utf-8')
        notfound_file.write(link)
        notfound_file.write("\n")
        notfound_file.close()
        print("Exception in " + link)

# get_city_information("https://en.wikipedia.org/wiki/Mumbai")


##### collecting seed urls ########
# get_seed_urls("https://en.wikipedia.org/wiki/List_of_cities_in_India_by_population")

driver.close()