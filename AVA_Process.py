#!/usr/bin/env python

import urllib.request
import datetime
import csv
import os
import shutil


print ("Starting...\n")
input(
    ("Turn on Wi-fi and connect to wifi101-network.\n"
     "Press enter when done\n")
    )

# Run connection test and sensor self test
p = False
while p == False:
    try:
        self = urllib.request.urlopen("http://192.168.1.1/S", timeout=30).read()
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
            p = True

# Get vehicle info
veh = input("Enter the name of the vehicle (ex: Steve's Toyota).\n")

# Check for baseline data
path = "/home/owner/"
pathI = path + veh + "BI"
pathAC = path + veh + "ACI"
pathSS = path + veh + "BSS"
baseI = False
baseAC = False
baseSS = False

if os.path.exists(pathI):
    baseI = True
if os.path.exists(pathAC):
    baseAC = True    
if os.path.exists(pathSS):
    baseSS = True
    print ('Steady Speed baseline exists')

# Get test type
rt = True
while rt == True:
    test = input(
        ("Enter type of test to run:"
         "For baseline at idle enter 1\n"
         "For suspected trouble at idle enter 2\n"
         "For baseline at steady speed enter 3\n"
         "For trouble at steady speed enter 4\n")
        )
    if test == '1':
        AC = input("Will the AC be on Y or N")
        if AC == "Y" and baseAC == True:
            ov = input("Baseline exists. Do you want to overwrite? Y or N")
            if ov == "Y":
                shutil.rmtree(pathAC)
                print("baseline removed")
                os.makedirs(pathAC)
                datapath = pathAC
                rt = False
            else:
                rt = True
        elif AC == "Y":
            os.makedirs(pathAC)
            datapath = pathAC
            rt = False
        if AC == "N" and baseI == True:
            ov = input("Baseline exists. Do you want to overwrite? Y or N")
            if ov == "Y":
                shutil.rmtree(pathI)
                print("baseline removed")
                os.makedirs(pathI)
                datapath = pathI
                rt = False
            else:
                rt = True
        elif AC == "N":
            os.makedirs(pathI)
            datapath = pathI
            rt = False
    if test == '2':
        now = '{:%Y-%b-%d %H:%M}'.format(datetime.datetime.now()) 
        pathTI = path + veh + " Idle Trouble/" + now
        os.makedirs(pathTI)
        datapath = pathTI
        rt = False
    if test == '3':
        SS = True
        pathtemp = path + 'tempSS/'
        os.makedirs(pathtemp)
        datapath = pathtemp
        rt = False
    if test == '4':
        now = '{:%Y-%b-%d %H:%M}'.format(datetime.datetime.now()) 
        pathTSS = path + veh + " Steady Speed Trouble/" + now
        os.makedirs(pathTSS)
        datapath = pathTSS
        rt = False

# How long to sample and delay
samples = int(input("How many samples (one minute each)?\n"))
wait = input("Do you want a delay before sampling begins Y or N\n")
if wait == 'Y':
    pause = int(input("How many minutes to delay?\n"))
    print ('waiting...')
    for i in range(0, pause):
        print ('minute ' + str(i+1))
        delay = urllib.request.urlopen("http://192.168.1.1/D")
        count = delay.read()
        delay.close()

print ('sampling...')
for j in range(0, samples):
        name = "Three Axes" + ' ' + str(j) # file name is the type of data and loop number
        print (name)        #debugging step. displays name of file to be created
        mkr = urllib.request.urlopen("http://192.168.1.1/A")
        accl = mkr.read().decode()
        mkr.close()
        filenam = datapath + '/' + name + '.txt'
        f = open(filenam,"w")
        f.write(accl)
        f.close
print ("done reading")
        

        





