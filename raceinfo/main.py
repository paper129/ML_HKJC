import datetime
import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import timedelta, date

def openWebsite(char):
    link = 'https://racing.hkjc.com/racing/information/English/Horse/SelectHorsebyChar.aspx?ordertype=' + char
    driver.get(link)
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    tbody = soup.find_all("a",{"class":"table_eng_text"})
    for i in tbody:
        # print(i['href'])
        getHorseInfo(i['href'])

def getHorseInfo(link):
    detail_link = 'https://racing.hkjc.com' + str(link) + '&Option=1'
    driver.get(detail_link)
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    grabbingFlag = False
    try:
        bigbordertable = soup.find("table",{"class":"bigborder"}).find('tbody').find_all('tr')
        for i in bigbordertable:
            try:
                if i['height']:
                    if i.find('span').getText() == '20/21':
                        grabbingFlag = True
                    else:
                        grabbingFlag = False
            except:
                pass

            if grabbingFlag:
                try:
                    content = []
                    # driver.get('https://racing.hkjc.com' + str2[0])
                    # time.sleep(2)
                    # html1 = driver.page_source
                    # soup1 = BeautifulSoup(html1,"html.parser")
                    # div = soup1.find_all("div",{"class":"race_tab"})[0]
                    # tbody = div.find_all('table')[0].find('tbody')
                    # tr = tbody.find_all('tr')[1]
                    # td = tr.find_all('td')[0].getText()
                    # print(td)
                    # classes = td.split('-').replace(" ","").replace('Class',"")
                    str1 = i.find_all('td')[0].find('a')['href']
                    str2 = str1.split('java')
                    content.append(str2[0])
                    # content.append(i.find_all('td')[0].find('a').getText())
                    content.append(i.find_all('td')[1].find('span').getText())
                    content.append(i.find_all('td')[2].getText())
                    content.append(i.find_all('td')[3].getText().strip())
                    content.append(i.find_all('td')[4].getText())
                    content.append(i.find_all('td')[5].getText())
                    content.append(i.find_all('td')[6].getText())
                    content.append(i.find_all('td')[7].getText())
                    content.append(i.find_all('td')[8].getText())
                    content.append(i.find_all('td')[9].find('a').getText())
                    content.append(i.find_all('td')[10].find('a').getText())
                    content.append(i.find_all('td')[11].find('span').getText())
                    content.append(i.find_all('td')[12].getText())
                    content.append(i.find_all('td')[13].getText())
                    content.append(i.find_all('td')[14].find('span').getText())
                    content.append(i.find_all('td')[15].getText())
                    content.append(i.find_all('td')[16].getText())
                    content.append(i.find_all('td')[17].getText())
                    with open('racing_record_v2.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(content)
                except:
                    pass
    except:
        pass
    
        
        
#main
driver = webdriver.Chrome()
with open('1718.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Class', 'Place','Date','Location', 'Dist','G','RaceClass','Dr','Rtg','Trainer','Jockey','LBW','Win Odds','Act.Wt.','RunningPosition','FinishTime','Declar.HorseWt.','Gear'])
char = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
for i in char:
    print("grabbing -> "+i)
    openWebsite(i)