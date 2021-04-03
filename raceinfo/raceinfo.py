from logging import NullHandler
import logging
from sys import excepthook
import sys
from urllib.parse import quote
from warnings import catch_warnings
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
from itertools import islice 


def web(link, year, mth, day, RaceNo, loc, syr):
    file_name = 'raceInfo_log.log'
    log_obj = Logger(file_name)
    log_obj.info("Web Fetch Starts".format())
    driver = webdriver.Chrome('chromedriver')
    driver.get(link)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    tempwebstr = soup.find_all("div", {"id": "errorContainer"}) or None
        #print(str(soup.find_all("div", {"id": "errorContainer"})))
    if tempwebstr is not None:
        log_obj.info('Error Container Found, skipping'.format())
        pass
    try:
        content = []
        RaceYr = year
        RaceMth = mth
        RaceDay = day
        RaceNum = RaceNo
        RaceLoc = loc
        date = str(RaceYr + RaceMth + RaceDay) + "-" + str(RaceNo)
        temp = soup.find("td", {"colspan" : "16"}).getText().strip()
        temp1 = temp.split("(")
        temp2 = temp1[1].split(")")
        year1 = int(syr) + 1
        RaceID = str(syr) + "-" + str(year1) + "-" + temp2[0] #identifer of Race (season + raceid)
        log_obj.info('RaceID %s'.format(), RaceID)
        #print("RaceID: " + RaceID)
        temp = ""
        temp = soup.find('td', {'style':'width: 385px;'}).getText()
        RaceClass = str(temp).split(" - ")[0]
        #print("Class " + RaceClass)
        RaceLenth = str(temp).split(" - ")[1]
        #print("Length " + RaceLenth)
        RaceGoing = soup.find('td', {'colspan': '14'}).getText()
        #print("Going " + RaceGoing)
        RaceTrack = soup.find_all('td', {'colspan': '14'})[1].getText()
        #print("Track: " + RaceTrack)
        TotalRaceTime = soup.find_all('td', {'style' : 'width:65px;'})
        i=0
        raceTime = []
        while i < (len(TotalRaceTime)):
            temp = ""
            temp1 = ""
            temp = TotalRaceTime[i].getText().split("(")
            temp1 = temp[1].split(")")
            raceTime.append(temp1[0])
            temp = ""
            temp1 = ""
            i = i + 1
        print(raceTime)
        my_dict = {}
        #headers = [header.text for header in soup.findAll('table')[2].find('tr', {'class': 'bg_blue color_w'}).find_all('td')]
        headers = ["Pla","Horse No","Horse","Jockey","Trainer","Act Wt","Declare Horse Wt","Draw","LBW","RunningPos","Finish Time","Win Odds","RaceID",'Class','Loc', 'Length', 'Going', 'Track']
        resultTable = soup.findAll('table')[2].find_all('tr', {'class' : None})
        #filename = RaceID + ".csv"
        filename = 'racing_record_18to20.csv'
        with open('./data/' + filename, 'a', newline='') as csvfile:
            log_obj.info('Logging to csv: Date: %s - Race %s'.format(),date ,RaceID)
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for vals in resultTable:                
                vals = [i.text.replace('\n', '').replace("\xa0", '').replace('                                ', '')
                .replace('                ','').replace('            ','').replace('        ',' ') for i in vals.find_all('td')]
                my_dict.update(dict(zip(headers, vals)))
                my_dict.update({'RaceID': RaceID})
                my_dict.update({'Class': RaceClass})
                my_dict.update({'Loc': RaceLoc})
                my_dict.update({'Length': RaceLenth})
                my_dict.update({'Going': RaceGoing})
                my_dict.update({'Track': RaceTrack})
                #print(my_dict)
                writer.writerow(my_dict)
                log_obj.info('Logging to csv: Date: %s - Race %s Done'.format(),date ,RaceID) 


    except Exception as e:
        log_obj.critical('Error: Expection %s', exc_info=e)
        pass

    driver.close()
    log_obj.info('Loop Finish')

def main():
    
    grabbing = True
    #Fetch all race data from 2018/19 - 2019/20 (SHA TIN)
    syr = 21
    year = "20" + str(syr)
    mth = 1
    day = 1
    num = 0
    #loc = "ST"
    loc = "HV" 
    #link = "https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate=2021/02/28"
    while grabbing == True:
        if day >= 1 and day <= 9:
            tempday = "0" + str(day) #1-9 should be 01-09
        else:
            tempday = str(day)
        
        if mth >= 1 and mth <= 9:
            tempmth = "0" + str(mth) #1-9 should be 01 - 09
        else:
            tempmth = mth
        link = 'https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate=' + str(year) + '/' + str(tempmth) + '/'+ str(tempday) + "&Racecourse=" + str(loc) + "&RaceNo=" + str(num)
        print("Race" + str(num))
        print("Date: " + str(year) + str(tempmth) + str(tempday))
        file_name = 'raceInfo_log'
        log_obj1 = Logger(file_name)
        log_obj1.info("Link: %s", link)
        web(link=link, year=str(year), mth=str(mth), day=str(day), RaceNo=str(num), loc=str(loc), syr=str(syr))
        if mth == 12 and day == 31 and num == 11:
            syr += 1
            num = 1
            mth = 1
            day = 1 
            continue
        if day == 31 and num == 11:
            day = 1
            mth += 1
        if num == 11:
            day +=1
            num = 1
        if num >= 0 and num < 11:
            num += 1
            
        
        
    if year == 20 and mth == 3 and day == 9:
        grabbing = False
        print("done")
    

def Logger(file_name):
    formatter = logging.Formatter(fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                      datefmt='%Y/%m/%d %H:%M:%S') # %I:%M:%S %p AM|PM format
    logging.basicConfig(filename = '%s.log' %(file_name),format= '%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                      datefmt='%Y/%m/%d %H:%M:%S', filemode = 'w', level = logging.INFO)
    log_obj = logging.getLogger()
    log_obj.setLevel(logging.DEBUG)
    # log_obj = logging.getLogger().addHandler(logging.StreamHandler())

    # console printer
    screen_handler = logging.StreamHandler(stream=sys.stdout) #stream=sys.stdout is similar to normal print
    screen_handler.setFormatter(formatter)
    logging.getLogger().addHandler(screen_handler)

    log_obj.info("Logger object created successfully..")
    return log_obj

if __name__ == '__main__':
    main()