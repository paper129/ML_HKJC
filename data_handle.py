import csv
from warnings import catch_warnings

from pandas.core.arrays.categorical import contains

with open('HV-Prod.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    #writer.writerow(['Pla','Horse No','Horse','Jockey','Trainer','Act Wt','Declare Horse Wt','Draw','LBW','RunningPos','Finish Time','Win Odds','RaceID','Class','Loc','Length','Going','Track'])
    writer.writerow(['Pla','Going','Dist','Draw','JW','AW','Time','WOdd'])

with open('HV_Dataset.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row.keys())
        try:
            content = []
            #Place
            content.append(row['Pla'])

            #Location
            if "HV" in row['Loc']:
                content.append("0") #ST CODE: 0
            else:
                content.append("1")
            
            #Track
            if 'T-1F' in row['Track']: #TURF TRACK
                content.append('0')
                if "FIRM" == row['Going']:
                    content.append('0')
                if "GOOD TO FIRM" == row['Going']:
                    content.append('1')
                if "GOOD" == row['Going']:
                    content.append('2')
                if "GOOD TO YIELDING" == row['Going']:
                    content.append('3')
                if "YIELDING" == row['Going']:
                    content.append('4')
                if "YIELDING TO SOFT" == row['Going']:
                    content.append('5')
                if "SOFT" == row['Going']:
                    content.append('6')
                if "HEAVY" == row['Going']:
                    content.append('7')
            else:
                if "ALL WEATHER TRACK" in row['Track']:
                    content.append('1')
                    if "WET FAST" == row['Going']:
                        content.append('0')
                    if "FAST" == row['Going']:
                        content.append('1')
                    if "GOOD" == row['Going']:
                        content.append('2')
                    if "SLOW" == row['Going']:
                        content.append('3')
                    if "WET SLOW" == row['Going']:
                        content.append('4')
                    if "RAIN AFFECTED" == row['Going']:
                        content.append('5')
                    if "NORMAL WATERING" == row['Going']:
                        content.append('6')
            #Distance
            if '-' in row['Length']:
                content.append('0')
            else:
                leng = row["Length"].split('M')[0]
                print(leng)
                content.append(leng)
            #Draw
            if '-' in row['Draw']:
                content.append('0')
            else:
                content.append(row["Draw"])
            #Jockey Weight
            if '-' in row['Act Wt']:
                content.append('0')
            else:
                content.append(row['Act Wt'])
            #Horse Weight
            if '-' in row['Declare Horse Wt']:
                content.append('0')
            else:
                content.append(row['Declare Horse Wt'])
            #FinishTime
            if '-' in row['Finish Time']:
                time = '0'
            else:
                FinishTime = row["Finish Time"].replace(".",":")
                M,S,ms = FinishTime.split(":")
                time = 0.00
                time = time + (int(M)*60)
                time = time + int(S)
                time = time + int(ms)/100
            content.append(str(time))
            #Win Odds
            errstr = '-'
            if errstr not in row['Win Odds']:
                odds = float(row['Win Odds'])
            else:
                odds = -1
            content.append(odds)
            print(content)

            with open('HV-Prod.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(content)
        except Exception as e:
            print(e)