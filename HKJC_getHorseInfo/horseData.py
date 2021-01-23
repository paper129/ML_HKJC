from os import link
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def webcatching(link):
    driver = webdriver.Chrome()
    driver.get(link)
    time.sleep(3)
    html = driver.page_source
    print(html)
    soup = BeautifulSoup(html,"html.parser")

def linkpassing():
    with open("fullLinkList.txt", "r") as f:
        for line in f:
            print(line)
            webcatching(line)
            if 'str' in link:
                break