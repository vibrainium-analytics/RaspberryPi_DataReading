#!/usr/bin/env python

import urllib.request
import time
import csv
import os


print ("Starting...\n")
input(
    ("Turn on Wi-fi and connect to wifi101-network.\n"
     "Press enter when done\n")
    )

# Run sensor self test
p = False
while p == False:
    self = urllib.request.urlopen("http://192.168.1.1/S").read()
    selftest = self.decode('ascii')
    if 'pass' not in selftest:
        if 'fail' in selftest:
            input(
                ("Self test failed. Check sensor for damage or low battery./n"
                 "Press enter to exit\n")
                )
            quit()
        else:
            input(
                ("Not connected. Reset Wi-Fi connection and try again.\n"
                 "Press enter when done.\n")
                )
    elif 'pass' in selftest:
        p = True

# Get vehicle info
veh = input("Enter the name of the vehicle (ex: Steve's Toyota).\n")

# Check for baseline data
path = "/home/owner/"
pathI = path + veh + "BI"
pathSS = path + veh + "BSS"
if os.path.exists(pathI):
    baseI = True
if os.path.exists(pathSS):
    baseSS = True

# Get test type
test = input(
    ("Enter type of test to run:\n"
     "For baseline at idle enter 1\n"
     "For suspected trouble at idle enter 2\n"
     "For baseline at steady speed enter 3\n"
     "For trouble at steady speed enter 4\n")
    )

if test == 1 and baseI == True:
    ov = input ("Baseline at idle exists for this vehicle. Overwrite? Y or N\n")

os.makedirs(pathI)


    

        
        
    

##fold = raw_input("What is the name of the folder to store the data?\n")
##path = "/home/pi/" + fold
##new = 'N'
##
##while os.path.exists(path) and new == 'N':
##    new = raw_input("That folder already exists. Use it anyway? Y or N\n")
##    if new == "N":
##        fold = raw_input("What is the name of the folder to store the data?\n")
##        path = "/home/pi/" + fold
##        
##if not os.path.exists(path):
##    os.makedirs(path)
##
##choice = raw_input(
##("For three individual axes values (X,Y,Z) enter A\n"
##"For X-axis values enter X\n"
##"For Y-axis values enter Y\n"
##"For Z-axis values enter Z\n")
##)
##samples = input("How many samples (one minute each)?\n")
##
##wait = raw_input("Do you want a delay before sampling begins Y or N\n")
##
##if wait == 'Y':
##    pause = input("How many minutes to delay?\n")
##    print ('waiting...')
##    for i in range(0, pause):
##        print ('minute ' + str(i+1))
##        delay = urllib2.urlopen("http://192.168.1.1/D")
##        count = delay.read()
##        delay.close()
##
##print ('sampling...')        
##
##for j in range(0, samples):
##    W = 0                   #determines if the data will be written to file
##    if choice == 'A':
##        name = choice + ' ' + str(j) # file name is the type of data and loop number
##        print (name)        #debugging step. displays name of file to be created
##        mkr = urllib2.urlopen("http://192.168.1.1/A")
##        accl = mkr.read()
##        mkr.close()
##        W = 1               #data was recieved so a write will be performed
##    elif choice == 'X':
##        name = choice + ' ' + str(j) # file name is the type of data and loop number
##        print (name)
##        mkr = urllib2.urlopen("http://192.168.1.1/X")
##        accl = mkr.read()
##        mkr.close()
##        W = 1
##    elif choice == 'Y':
##        name = choice + ' ' + str(j) # file name is the type of data and loop number
##        print (name)
##        mkr = urllib2.urlopen("http://192.168.1.1/Y")
##        accl = mkr.read()
##        mkr.close()
##        W = 1
##    elif choice == 'Z':
##        name = choice + ' ' + str(j) # file name is the type of data and loop number
##        print (name)
##        mkr = urllib2.urlopen("http://192.168.1.1/Z")
##        accl = mkr.read()
##        mkr.close()
##        W = 1
##        
##    #if user made a valid choice data will be written to text file    
##
##    if W == 1:
##        filenam = path + '/' + name + '.txt'
##        f = open(filenam,"w")
##        f.write(accl)
##        f.close
##
###if invalid choice was entered user is notified
##        
##if W == 0:
##    print ("invalid entry")
##
##print ("done reading")          #file has been written
