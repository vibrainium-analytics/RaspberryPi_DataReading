#!/usr/bin/env python

import urllib.request
import datetime
import csv
import os
import shutil


# Initialize Variables
path = "/home/pi/"
temp = path + "temp/"

# Start program
print ("Starting...\n")
input(
    ("Turn on Wi-fi and connect to wifi101-network.\n"
     "Press enter when done\n")
    )

# Run connection test and sensor self test
pasd = False
while pasd == False:
    try:
        self = urllib.request.urlopen("http://192.168.1.1/S", timeout=20).read()
        selftest = self.decode('ascii')
        connect = True
    except (UnicodeDecodeError, urllib.error.URLError):
        input(
            ("Not connected. Reset Wi-Fi connection and try again.\n"
             "Press enter when done.\n")
            )
        connect = False
    if connect == True:
        if 'fail' in selftest:
            input(
                ("Self test failed. Check sensor for damage or low battery./n"
                "Press enter to exit\n")
                )
            quit()
        elif 'pass' in selftest:
            pasd = True

# Get vehicle name. Check for baseline data and report to user
veh = input("Enter the name of the vehicle (ex: Steve-Toyota).\n")
pathI = path + veh + "-BaseIdle/"
pathAC = path + veh + "-BaseACIdle/"
pathSS = path + veh + "-BaseStdySpd/"
if os.path.exists(pathI):
    print('Baseline folder exists for AC off')
    baseI = True
else:
    print('No standard baseline exists for this vehicle with AC off at idle')
    baseI = False    
if os.path.exists(pathAC):
    print('Baseline folder exists for AC on')
    baseAC = True
else:
    print('No standard baseline exists for this vehicle with AC on at idle')
    baseAC = False
if os.path.exists(pathSS):
    print ('Steady Speed baseline folder exists')
    baseSS = True 
else:
    print('No standard baselines exist for this vehicle at steady speed.')
    baseSS = False

# Get number of test to run
isgood = False
while isgood == False:
    try:
        test = int(input(
            ("\nEnter type of test to run:\n"
             "For baseline at idle enter 1\n"
             "For suspected trouble at idle enter 2\n"
             "For baseline at steady speed enter 3\n"
             "For trouble at steady speed enter 4\n")
            ))
        isgood = True
        if test < 1 or test > 4:
            print('Please enter and number between 1 and 4')
            isgood = False
    except (ValueError):
        print('Please enter and number between 1 and 4')      

# Check for delay request and test length
isgood = False
while isgood == False:
    try:
        pause = int(input(
            ("\nHow many minutes do you want to delay to allow the vehicle\n"
             "to reach test conditions. (enter 0 for no delay)\n")
            ))
        samples = int(input("\nHow many one minute samples? (there should be at least 3)\n"))
        isgood = True
    except (ValueError):
        print('Please enter a number')
        
# Pause for vehicle to reach test conditions
print ('waiting...')       
for i in range(0, pause):
    print ('minute ' + str(i+1))
    delay = urllib.request.urlopen("http://192.168.1.1/D")
    count = delay.read()
    delay.close()

# collect data
print ('sampling...')
for j in range(0, samples):
    name = "Three Axes" + ' ' + str(j+1)
    num = str(j+1)
    print ('sample #' + num)                                                
    mkr = urllib.request.urlopen("http://192.168.1.1/A")
    accl = mkr.read().decode()
    mkr.close()
    os.makedirs(temp)
    filenam = temp + name + '.txt'
    f = open(filenam,"w")
    f.write(accl)
    f.close
print ("done reading")

# set up folders for data        
if test == 1:
    isgood = False
    while isgood == False:
        on = input("Was the AC on? Y or N\n")
        if on == 'Y' or  on == 'y':
            AC = True
            isgood = True
        elif on == 'N' or on == 'n':
            AC = False
            isgood = True
        else:
            print('Please enter Y or N')        
    if baseI == True or baseAC == True:
        isgood = False
        while isgood == False:
            ow = input("Baseline exists. Do you want to overwrite? Y or N\n")
            if ow == 'Y' or  ow == 'y':
                Over = True
                isgood = True
            elif ow == 'N' or ow == 'n':
                Over = False
                isgood = True
            else:
                print('Please enter Y or N') 
    if AC == True and baseAC == True and Over == True:
        shutil.rmtree(pathAC)           
        os.makedirs(pathAC)
        datapath = pathAC
        print("baseline replaced")
    elif AC == True and baseAC == True and Over == False:
        new = input("Enter the name for this new baseline.\n")
        pathAC = pathAC[:-1] + '' 
        datapath = pathAC + '-' + new + "/"
        os.makedirs(datapath)
    elif AC == True and baseAC == False:
        os.makedirs(pathAC)
        datapath = pathAC
    if AC == False and baseI == True and Over == True:
        shutil.rmtree(pathI)           
        os.makedirs(pathI)
        datapath = pathI
        print("baseline replaced")
    elif AC == False and baseI == True and Over == False:
        new = input("Enter the name for this new baseline.\n")
        pathI = pathI[:-1] + '' 
        datapath = pathI + '-' + new + "/"
        os.makedirs(datapath)
    elif AC == False and baseI == False:
        os.makedirs(pathI)
        datapath = pathI
        
if test == 2:
    isgood = False
    while isgood == False:
        on = input("Was the AC on? Y or N\n")
        if on == 'Y' or  on == 'y':
            AC = True
            isgood = True
        elif on == 'N' or on == 'n':
            AC = False
            isgood = True
        else:
            print('Please enter Y or N')  
    if AC == True:
        trb = "-AC-Idle-Trbl/"
    elif AC == False:
        trb = "-Idle-Trbl-NO-AC/"
    now = '{:%Y-%b-%d %H:%M}'.format(datetime.datetime.now()) 
    pathTI = path + now + '-' + veh + trb + '/'
    os.makedirs(pathTI)
    datapath = pathTI
    
if test == 3:
    isgood = False
    while isgood == False:
        try:
            speed1 = int(input('What was the vehicle speed in miles per hour for the test?/n'))
            isgood = True
        except (ValueError):
            print('Please enter a number')
    speed = 5 *(round((speed1)/5))
    pathSS1 = pathSS + str(speed) + 'MPH/'
    if baseSS == True and os.path.exists(pathSS1):
        isgood = False
        while isgood == False:
            ow = input("Baseline exists for this speed. Do you want to overwrite? Y or N\n")
            if ow == 'Y' or  ow == 'y':
                Over = True
                isgood = True
            elif ow == 'N' or ow == 'n':
                Over = False
                isgood = True
            else:
                print('Please enter Y or N') 
        if Over == True:
            shutil.rmtree(pathSS1)           
            os.makedirs(pathSS1)
            datapath = pathSS1
            print("baseline replaced")
        elif Over == False:
            new = input("Enter the name for this new baseline.\n")
            pathSS = pathSS[:-1] + '' 
            datapath = pathSS + '-' + new + "/" + str(speed) + 'MPH/'
            os.makedirs(datapath)
    else:
        os.makedirs(pathSS1)
        datapath = pathSS1 

if test == 4:
    isgood = False
    while isgood == False:
        try:
            speed1 = int(input('What was the vehicle speed in miles per hour for the test?/n'))
            isgood = True
        except (ValueError):
            print('Please enter a number')
    speed = 5*(round((speed1)/5))
    now = '{:%Y-%b-%d %H:%M}'.format(datetime.datetime.now()) 
    pathTSS = path + now + '-' + veh + '-Stdy-Spd-Trbl' + str(speed) +'MPH/'
    os.makedirs(pathTSS)
    datapath = pathTSS

# Limit number of samples 



    





