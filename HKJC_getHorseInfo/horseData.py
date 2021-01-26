from os import link
import re
from urllib.parse import quote
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

def webcatching(link):
    print(link)
    driver = webdriver.Chrome()
    driver.get(link)
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    #Horse Data - Name, Current Trainer, Sire
    horse_name = soup.find("span", {'class': 'title_text'}).getText()
    trainer_name = soup.find('a', attrs={'href': re.compile('TrainerId=')}).getText()
    sire_name = soup.find('a', attrs={'href': re.compile('HorseSire=')}).getText().strip()
    #History of Horse
    data_list = []
    table = soup.find("table", {"class" : "bigborder"})
    with open(horse_name + '.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for table_body in soup.body.find_all('td', attrs={'class': 'htable_eng_text'}):
            data_list.append(table_body.get_text().strip())
        writer.writerows([data_list,])
    
    # table_body = table.find('tbody')
    # for row in table_body:
    #     print(row)
    #     parsed_row = BeautifulSoup(row, 'html_parser')
    #     print(parsed_row.find_all('td', {'class': 'htable_eng_text'}).getText())        
    driver.close()
    print(horse_name)
    print(trainer_name)
    print(sire_name)
    print(data_list)

def main(): # testing purpose - FLYING MONKEY (T361)
    webcatching(link= "https://racing.hkjc.com/racing/information/English/Horse/Horse.aspx?HorseId=HK_2019_D508&Option=1")

# def main():
#     n = 0
#     with open("fullLinkList.txt", "r") as f:
#         for line in f:
#             print(n+1)
#             n = n + 1
#             webcatching(line)
#             if line == '':
#                 break

if __name__ == '__main__':
    main()