import requests
import simplejson as json
import datetime
import csv
import os.path
import pandas as pd
import os
import sys
import base64
import smtplib
from datetime import date, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
import time



def datei():
    from datetime import date, timedelta
    a = []
    d1 = date(2020,7,13)
    
    d2 = date.today()
    
    dd = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]

    ddd = [str(d1 + timedelta(days=x)) for x in range((d2-d1).days + 1)]
    for x in ddd:
        a.append(x.replace("-",""))
    return a

def links(a):
    urls = []
    count = len(a)
    for i in range(0,count):
        link = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{a[i]}/5.30?MD=1'
        urls.append(link)
    return urls

def js(i):
   
    r = requests.get(i)
    test = r.json()
    return test

#get data locally
def page(ff):
    data = []
    try:
        con1 = ff['T1'][0]['CoNm']
    except:
        con1 = ' '

    try:
        con2 = ff['T2'][0]['CoNm']
    except:
        con2 = ' '

    #League
    try:
        league = ff['Stg']['Sdn']
    except:
        league = ' '

    #Team 1 Name
    try:
        team1name = ff['T1'][0]['Nm']
    except:
        team1name = ' '

    #Team1score
    try:
        team1score = ff['Tr1']
    except:
        team1score = ' '

    #Team2 Name
    try:
        team2name = ff['T2'][0]['Nm']
    except:
        team2name = ' '

    #Team2score
    try:
        team2score = ff['Tr2']
    except:
        team2score = ' '

    #win/lose/draw
    try:
        if (team1score>team2score):
            wld = 'T1'
        if (team2score>team1score):
            wld = 'T2'
        if (team1score == team2score):
            wld = 'D'
        if (team1score == ' ' and team2score == ' '):
            wld = ' '
    except:
        wld = ' '

    data.append(league)
    data.append(con1)
    data.append(con2)
    data.append(team1name)
    data.append(team1score)
    data.append(team2name)
    data.append(team2score)
    data.append(wld)
    
    return data

#check for unique teams
def lopp(keyy,khali):
    lip = []
    goals = []
    for a in khali:
        if(a[3] == keyy):
            lip.append(a)
        if(a[5] == keyy):
            lip.append(a)

    if(len(lip)>30):
        lip = lip[-30:]

    cnt = len(lip)

    cntry = lip[0][1]
    legue = lip[0][0]
    teamname = keyy
   

    for i in lip:
        if (i[3] == keyy):
            scored = i[4]
            conceded = i[6]
        if (i[5] == keyy):
            scored = i[6]
            conceded = i[4]

        goals.append(scored)
        goals.append(conceded)

    if (len(goals)<60):
        rem = 60-len(goals)
        for i in range(rem):
            goals.append(' ')


    #WLD
    for i in lip:
        if(i[7] == 'T1'):
            wld = 'W'
        if((i[7] == 'T2')):
            wld = 'L'
        if((i[7] == 'D')):
            wld = 'D'
        if((i[7] == ' ')):
            wld = ' '

        goals.append(wld)


    goals.insert(0,cntry) 
    goals.insert(1,legue)
    goals.insert(2,teamname)
    return goals

#final
def final(khali):
    csvv = []
    teams = []
    ul = []
    
    for i in khali:
        teams.append(i[3])
        teams.append(i[5])

    for a in teams:
        if a not in ul:
            ul.append(a)

    for i in ul:
        yy = lopp(i,khali)
        csvv.append(yy)

    for i in csvv:
        if len(i)<93:
            remv = 93-len(i)
            for f in range(remv):
                i.append(' ')
    return csvv

#khali list
def ooo():
    khi = []
    jatre = []
    khali = []
    for i in links(datei()):
        tess = js(i)
        khi.append(tess)
    try:
        for l in khi:
            for k in l['Stages']:
                for i in k['Events']:
                    jatre.append(i)
    except:
        pass

    for i in jatre:
        ss = page(i)
        khali.append(ss)
        
    return khali

#next day
def nxtday(siu):
    ul1 = []
    teams1 = []
    teams1d = []


    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=1)
    NextDay_Date_Formatted = NextDay_Date.strftime ('%Y%m%d')
    NextDay_Date_Formatted1 = NextDay_Date.strftime ('%d-%m-%Y') 
    day1l = str(NextDay_Date_Formatted)
    day1p = str(NextDay_Date_Formatted1)


    nxl1 = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{day1l}/5.30?MD=1'
    #function to get json
    nxtj1 = js(nxl1)

    aa = nxtj1['Stages']
    for k in aa:
        for i in k['Events']:
            teams1d.append(i)

    for i in teams1d:
        teams1.append(i['T1'][0]['Nm'])
        teams1.append(i['T2'][0]['Nm'])

    for a in teams1:
        if a not in ul1:
            ul1.append(a)

    for i in ul1:
        for a in siu:
            if(a[2] == i):
                a.append(day1p)
    
    return siu

#next day
def nxtday2(ty):
    ul2 = []
    teams2 = []
    teams2d = []


    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=2)
    NextDay_Date_Formattedd = NextDay_Date.strftime ('%Y%m%d')
    NextDay_Date_Formatted2 = NextDay_Date.strftime ('%d-%m-%Y') 
    day2l = str(NextDay_Date_Formattedd)
    day2p = str(NextDay_Date_Formatted2)


    nxl2 = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{day2l}/5.30?MD=1'
    #function to get json
    nxtj2 = js(nxl2)

    aa = nxtj2['Stages']
    for k in aa:
        for i in k['Events']:
            teams2d.append(i)

    for i in teams2d:
        teams2.append(i['T1'][0]['Nm'])
        teams2.append(i['T2'][0]['Nm'])

    for a in teams2:
        if a not in ul2:
            ul2.append(a)

    for i in ul2:
        for a in ty:
            if(a[2] == i):
                a.append(day2p)
    
    return ty

#next day
def nxtday3(ty1):
    ul3 = []
    teams3 = []
    teams3d = []


    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=3)
    NextDay_Date_Formatteddd = NextDay_Date.strftime ('%Y%m%d')
    NextDay_Date_Formatted3 = NextDay_Date.strftime ('%d-%m-%Y') 
    day3l = str(NextDay_Date_Formatteddd)
    day3p = str(NextDay_Date_Formatted3)


    nxl3 = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{day3l}/5.30?MD=1'
    #function to get json
    nxtj3 = js(nxl3)

    aa = nxtj3['Stages']
    for k in aa:
        for i in k['Events']:
            teams3d.append(i)

    for i in teams3d:
        teams3.append(i['T1'][0]['Nm'])
        teams3.append(i['T2'][0]['Nm'])

    for a in teams3:
        if a not in ul3:
            ul3.append(a)

    for i in ul3:
        for a in ty1:
            if(a[2] == i):
                a.append(day3p)
    
    return ty1

#day 4
def nxtday4(ty2):
    ul4 = []
    teams4 = []
    teams4d = []


    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=3)
    NextDay_Date_Formattedddd = NextDay_Date.strftime ('%Y%m%d')
    NextDay_Date_Formatted4 = NextDay_Date.strftime ('%d-%m-%Y') 
    day4l = str(NextDay_Date_Formattedddd)
    day4p = str(NextDay_Date_Formatted4)

    nxl4 = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{day4l}/5.30?MD=1'
    #function to get json
    nxtj4 = js(nxl4)

    aa = nxtj4['Stages']
    for k in aa:
        for i in k['Events']:
            teams4d.append(i)

    for i in teams4d:
        teams4.append(i['T1'][0]['Nm'])
        teams4.append(i['T2'][0]['Nm'])

    for a in teams4:
        if a not in ul4:
            ul4.append(a)

    for i in ul4:
        for a in ty2:
            if(a[2] == i):
                a.append(day4p)
    
    return ty2


#day 5
def nxtday5(ty3):
    ul5 = []
    teams5 = []
    teams5d = []


    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=4)
    NextDay_Date_Formatteddddd = NextDay_Date.strftime ('%Y%m%d')
    NextDay_Date_Formatted5 = NextDay_Date.strftime ('%d-%m-%Y') 
    day5l = str(NextDay_Date_Formatteddddd)
    day5p = str(NextDay_Date_Formatted5)

    nxl5 = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{day5l}/5.30?MD=1'
    #function to get json
    nxtj5 = js(nxl5)

    aa = nxtj5['Stages']
    for k in aa:
        for i in k['Events']:
            teams5d.append(i)

    for i in teams5d:
        teams5.append(i['T1'][0]['Nm'])
        teams5.append(i['T2'][0]['Nm'])

    for a in teams5:
        if a not in ul5:
            ul5.append(a)

    for i in ul5:
        for a in ty3:
            if(a[2] == i):
                a.append(day5p)
    
    return ty3

def nxtday6(ty4):
    ul6 = []
    teams6 = []
    teams6d = []
    
    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=5)
    NextDay_Date_Formattedddddd = NextDay_Date.strftime ('%Y%m%d')
    NextDay_Date_Formatted6 = NextDay_Date.strftime ('%d-%m-%Y') 
    day6l = str(NextDay_Date_Formattedddddd)
    day6p = str(NextDay_Date_Formatted6)

    nxl6 = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{day6l}/5.30?MD=1'
    nxtj6 = js(nxl6)

    aa = nxtj6['Stages']
    for k in aa:
        for i in k['Events']:
            teams6d.append(i)

    for i in teams6d:
        teams6.append(i['T1'][0]['Nm'])
        teams6.append(i['T2'][0]['Nm'])

    for a in teams6:
        if a not in ul6:
            ul6.append(a)

    for i in ul6:
        for a in ty4:
            if(a[2] == i):
                a.append(day6p)
    
    return ty4

def nxtday7(ty5):
    ul7 = []
    teams7 = []
    teams7d = []
    
    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=6)
    NextDay_Date_Formatteddddddd = NextDay_Date.strftime ('%Y%m%d')
    NextDay_Date_Formatted7 = NextDay_Date.strftime ('%d-%m-%Y') 
    day7l = str(NextDay_Date_Formatteddddddd)
    day7p = str(NextDay_Date_Formatted7)

    nxl7 = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{day7l}/5.30?MD=1'
    nxtj7 = js(nxl7)

    aa = nxtj7['Stages']
    for k in aa:
        for i in k['Events']:
            teams7d.append(i)

    for i in teams7d:
        teams7.append(i['T1'][0]['Nm'])
        teams7.append(i['T2'][0]['Nm'])

    for a in teams7:
        if a not in ul7:
            ul7.append(a)

    for i in ul7:
        for a in ty5:
            if(a[2] == i):
                a.append(day7p)
    
    return ty5

def nxtday8(ty6):
    ul8 = []
    teams8 = []
    teams8d = []
    
    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=6)
    NextDay_Date_Formattedddddddd = NextDay_Date.strftime ('%Y%m%d')
    NextDay_Date_Formatted8 = NextDay_Date.strftime ('%d-%m-%Y') 
    day8l = str(NextDay_Date_Formattedddddddd)
    day8p = str(NextDay_Date_Formatted8)

    nxl8 = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{day8l}/5.30?MD=1'
    nxtj8 = js(nxl8)

    aa = nxtj8['Stages']
    for k in aa:
        for i in k['Events']:
            teams8d.append(i)

    for i in teams8d:
        teams8.append(i['T1'][0]['Nm'])
        teams8.append(i['T2'][0]['Nm'])

    for a in teams8:
        if a not in ul8:
            ul8.append(a)

    for i in ul8:
        for a in ty6:
            if(a[2] == i):
                a.append(day8p)
    
    return ty6



#khali list
def ooo():
    khi = []
    jatre = []
    khali = []
    for i in links(datei()):
        tess = js(i)
        khi.append(tess)
    try:
        for l in khi:
            for k in l['Stages']:
                for i in k['Events']:
                    jatre.append(i)
    except:
        pass

    for i in jatre:
        ss = page(i)
        khali.append(ss)
        
    return khali

#next day
def nxtday(siu):
    ul1 = []
    teams1 = []
    teams1d = []


    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=1)
    NextDay_Date_Formatted = NextDay_Date.strftime ('%Y%m%d')
    NextDay_Date_Formatted1 = NextDay_Date.strftime ('%d-%m-%Y') 
    day1l = str(NextDay_Date_Formatted)
    day1p = str(NextDay_Date_Formatted1)


    nxl1 = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{day1l}/5.30?MD=1'
    #function to get json
    nxtj1 = js(nxl1)

    aa = nxtj1['Stages']
    for k in aa:
        for i in k['Events']:
            teams1d.append(i)

    for i in teams1d:
        teams1.append(i['T1'][0]['Nm'])
        teams1.append(i['T2'][0]['Nm'])

    for a in teams1:
        if a not in ul1:
            ul1.append(a)

    for i in ul1:
        for a in siu:
            if(a[2] == i):
                a.append(day1p)
    
    return siu

#next day
def nxtday2(ty):
    ul2 = []
    teams2 = []
    teams2d = []


    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=2)
    NextDay_Date_Formattedd = NextDay_Date.strftime ('%Y%m%d')
    NextDay_Date_Formatted2 = NextDay_Date.strftime ('%d-%m-%Y') 
    day2l = str(NextDay_Date_Formattedd)
    day2p = str(NextDay_Date_Formatted2)


    nxl2 = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{day2l}/5.30?MD=1'
    #function to get json
    nxtj2 = js(nxl2)

    aa = nxtj2['Stages']
    for k in aa:
        for i in k['Events']:
            teams2d.append(i)

    for i in teams2d:
        teams2.append(i['T1'][0]['Nm'])
        teams2.append(i['T2'][0]['Nm'])

    for a in teams2:
        if a not in ul2:
            ul2.append(a)

    for i in ul2:
        for a in ty:
            if(a[2] == i):
                a.append(day2p)
    
    return ty

#next day
def nxtday3(ty1):
    ul3 = []
    teams3 = []
    teams3d = []


    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=3)
    NextDay_Date_Formatteddd = NextDay_Date.strftime ('%Y%m%d')
    NextDay_Date_Formatted3 = NextDay_Date.strftime ('%d-%m-%Y') 
    day3l = str(NextDay_Date_Formatteddd)
    day3p = str(NextDay_Date_Formatted3)


    nxl3 = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{day3l}/5.30?MD=1'
    #function to get json
    nxtj3 = js(nxl3)

    aa = nxtj3['Stages']
    for k in aa:
        for i in k['Events']:
            teams3d.append(i)

    for i in teams3d:
        teams3.append(i['T1'][0]['Nm'])
        teams3.append(i['T2'][0]['Nm'])

    for a in teams3:
        if a not in ul3:
            ul3.append(a)

    for i in ul3:
        for a in ty1:
            if(a[2] == i):
                a.append(day3p)
    
    return ty1

#day 4
def nxtday4(ty2):
    ul4 = []
    teams4 = []
    teams4d = []


    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=3)
    NextDay_Date_Formattedddd = NextDay_Date.strftime ('%Y%m%d')
    NextDay_Date_Formatted4 = NextDay_Date.strftime ('%d-%m-%Y') 
    day4l = str(NextDay_Date_Formattedddd)
    day4p = str(NextDay_Date_Formatted4)

    nxl4 = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{day4l}/5.30?MD=1'
    #function to get json
    nxtj4 = js(nxl4)

    aa = nxtj4['Stages']
    for k in aa:
        for i in k['Events']:
            teams4d.append(i)

    for i in teams4d:
        teams4.append(i['T1'][0]['Nm'])
        teams4.append(i['T2'][0]['Nm'])

    for a in teams4:
        if a not in ul4:
            ul4.append(a)

    for i in ul4:
        for a in ty2:
            if(a[2] == i):
                a.append(day4p)
    
    return ty2


#day 5
def nxtday5(ty3):
    ul5 = []
    teams5 = []
    teams5d = []


    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=4)
    NextDay_Date_Formatteddddd = NextDay_Date.strftime ('%Y%m%d')
    NextDay_Date_Formatted5 = NextDay_Date.strftime ('%d-%m-%Y') 
    day5l = str(NextDay_Date_Formatteddddd)
    day5p = str(NextDay_Date_Formatted5)

    nxl5 = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{day5l}/5.30?MD=1'
    #function to get json
    nxtj5 = js(nxl5)

    aa = nxtj5['Stages']
    for k in aa:
        for i in k['Events']:
            teams5d.append(i)

    for i in teams5d:
        teams5.append(i['T1'][0]['Nm'])
        teams5.append(i['T2'][0]['Nm'])

    for a in teams5:
        if a not in ul5:
            ul5.append(a)

    for i in ul5:
        for a in ty3:
            if(a[2] == i):
                a.append(day5p)
    
    return ty3

def nxtday6(ty4):
    ul6 = []
    teams6 = []
    teams6d = []
    
    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=5)
    NextDay_Date_Formattedddddd = NextDay_Date.strftime ('%Y%m%d')
    NextDay_Date_Formatted6 = NextDay_Date.strftime ('%d-%m-%Y') 
    day6l = str(NextDay_Date_Formattedddddd)
    day6p = str(NextDay_Date_Formatted6)

    nxl6 = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{day6l}/5.30?MD=1'
    nxtj6 = js(nxl6)

    aa = nxtj6['Stages']
    for k in aa:
        for i in k['Events']:
            teams6d.append(i)

    for i in teams6d:
        teams6.append(i['T1'][0]['Nm'])
        teams6.append(i['T2'][0]['Nm'])

    for a in teams6:
        if a not in ul6:
            ul6.append(a)

    for i in ul6:
        for a in ty4:
            if(a[2] == i):
                a.append(day6p)
    
    return ty4

def nxtday7(ty5):
    ul7 = []
    teams7 = []
    teams7d = []
    
    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=6)
    NextDay_Date_Formatteddddddd = NextDay_Date.strftime ('%Y%m%d')
    NextDay_Date_Formatted7 = NextDay_Date.strftime ('%d-%m-%Y') 
    day7l = str(NextDay_Date_Formatteddddddd)
    day7p = str(NextDay_Date_Formatted7)

    nxl7 = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{day7l}/5.30?MD=1'
    nxtj7 = js(nxl7)

    aa = nxtj7['Stages']
    for k in aa:
        for i in k['Events']:
            teams7d.append(i)

    for i in teams7d:
        teams7.append(i['T1'][0]['Nm'])
        teams7.append(i['T2'][0]['Nm'])

    for a in teams7:
        if a not in ul7:
            ul7.append(a)

    for i in ul7:
        for a in ty5:
            if(a[2] == i):
                a.append(day7p)
    
    return ty5

def nxtday8(ty6):
    ul8 = []
    teams8 = []
    teams8d = []
    
    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=6)
    NextDay_Date_Formattedddddddd = NextDay_Date.strftime ('%Y%m%d')
    NextDay_Date_Formatted8 = NextDay_Date.strftime ('%d-%m-%Y') 
    day8l = str(NextDay_Date_Formattedddddddd)
    day8p = str(NextDay_Date_Formatted8)

    nxl8 = f'https://prod-public-api.livescore.com/v1/api/react/date/soccer/{day8l}/5.30?MD=1'
    nxtj8 = js(nxl8)

    aa = nxtj8['Stages']
    for k in aa:
        for i in k['Events']:
            teams8d.append(i)

    for i in teams8d:
        teams8.append(i['T1'][0]['Nm'])
        teams8.append(i['T2'][0]['Nm'])

    for a in teams8:
        if a not in ul8:
            ul8.append(a)

    for i in ul8:
        for a in ty6:
            if(a[2] == i):
                a.append(day8p)
    
    return ty6

def csvu(cc):
    df = pd.DataFrame(cc)
    #directory = os.path.dirname(os.path.realpath('__file__'))
    #filename = "scrapedfile.csv"
    #print(os.path.dirname(os.path.realpath('__file__')))
    #file_path = os.path.join(directory, filename)
    df.to_csv('Scraped.csv',index=False,header=['County','LeagueName','TeamName','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','GoalsScored','GoalsConceded','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','WLD','NextDate'])
    return 
    
    
def send_mail():
    email_user = 'charanyes1@outlook.com'
    email_password = 'Chiru@7887...'
    email_send = 'jdevendraraj@outlook.com'

    subject = 'Output CSV'
    
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = '***Hi there, sending this email from Python!***'
    msg.attach(MIMEText(body,'plain'))
    
    filename='Footballdata.csv'
    attachment  = open('Scraped.csv','rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.office365.com',587)
    server.starttls()
    server.login(email_user,email_password)
    server.sendmail(email_user,email_send,text)
    server.quit()
    return
    
    
def main():
    yyf = [ ]
    khali = ooo()
    siu = final(khali)
    ty = nxtday(siu)
    ty1 = nxtday2(ty)
    ty2 = nxtday3(ty1)
    ty3 = nxtday4(ty2)
    ty4 = nxtday5(ty3)
    ty5 = nxtday6(ty4)
    ty6 = nxtday7(ty5)
    ty7 = nxtday8(ty6)
    
    #last
    for i in ty7:
        if (len(i)>92):
            yyf.append(i[:94])
        
    aaj = csvu(yyf)
    khali.clear()
    siu.clear()
    ty.clear()
    ty1.clear()
    ty2.clear()
    ty3.clear()
    ty4.clear()
    ty5.clear()
    ty6.clear()
    ty7.clear()
    yyf.clear()
    return 


if __name__ == "__main__":
    aapp = main()
    sm = send_mail()

