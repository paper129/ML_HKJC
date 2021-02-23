from logging import NullHandler
from os import link, write
import re
from sys import excepthook
from urllib.parse import quote
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

def webcatching(link):
    print(link)
    driver = webdriver.Chrome('chromedriver')
    #options = webdriver.ChromeOptions() 
    #options.headless = True
    driver.get(link)
    time.sleep(3)
    driver.implicitly_wait(5)
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    #Horse Data - Name, Current Trainer, Sire
    horse_name = soup.find("span", {'class': 'title_text'}).getText()
    #trianer_name = soup.find('a', attrs={'href': re.compile('TrainerId=')}).getText()
    trainer_name = ""
    try: 
        trianer_name = soup.find('a', attrs={'href': re.compile('TrainerId=')}).getText()
    except AttributeError:
        trainer_name = "No record"
    sire_name = ""
    try:
        sire_name = soup.find('a', attrs={'href': re.compile('HorseSire=')}).getText().strip()
    except AttributeError:
        sire_name = "Undefined"
    #History of Horse
    data_list = []
    table = soup.find("table", {"class" : "bigborder"})
    filepath = './data/' + horse_name + '.csv'
    with open(filepath, 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile)
        for table_body in soup.body.find_all('td', attrs={'class': 'htable_eng_text'}):
            #print(table_body.get_text().strip())
            if "---" not in table_body.get_text().strip():
                    data_list.append(' ')
            else:
                data_list.append('\n')        
        writer.writerows([data_list],)
    
    
    # table_body = table.find('tbody')
    # for row in table_body:
    #     print(row)
    #     parsed_row = BeautifulSoup(row, 'html_parser')
    #     print(parsed_row.find_all('td', {'class': 'htable_eng_text'}).getText())        
    driver.close()
    print(horse_name)
    print(trainer_name)
    print(sire_name)
    #print(data_list)

# def main(): # testing purpose - FLYING MONKEY (T361)
#     webcatching(link= "https://racing.hkjc.com/racing/information/English/Horse/Horse.aspx?HorseId=HK_2018_C324&Option=1")

def main():
    n = 0
    with open("fullLinkList.txt", "r") as f:
        for line in f:
            print(n+1)
            n = n + 1
            webcatching(line)
            if line == '':
                break

if __name__ == '__main__':
    main()