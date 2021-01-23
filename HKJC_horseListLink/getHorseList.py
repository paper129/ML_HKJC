import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def getLinks():
    links = []
    url = 'https://racing.hkjc.com/racing/information/chinese/Horse/HorseFormerName.aspx'
    driver = webdriver.Firefox() #call Firefox to open the webpage - HKJC website request for JS & cookies which cannot simulate using requests
    driver.get(url)
    time.sleep(20) #allow time for loading the webpage
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")

    #full url of HKJC Horse data page is: 
    # + (web host)
    # /racing/information/chinese/Horse/Horse.aspx?HorseId=HK_2019_D466 (appen from file) + 
    # &Option=1 (all past results)
    # the for loop is used to append the head & tail of the url and write to file
    for link in soup.find_all('a', attrs={'href': re.compile("HorseId=")}):
        links.append(link.get('href'))
        print('https://racing.hkjc.com' + link.get('href') + '&Option=1')
        hs = open("links.txt","a")
        hs.write('https://racing.hkjc.com' + link.get('href') + '&Option=1' + "\n")
        hs.close()
    return links