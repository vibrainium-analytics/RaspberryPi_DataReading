#!/usr/bin/env python

import urllib.request
import datetime
import os
import shutil
import math
import numpy
from scipy import signal


# Initialize Variables
freq = 500                  # mkr sample frequency in Hz
n = 256                     # number of points in fft
runav = 20                  # number of points in fft running average
path = "/home/pi/"          # path name for file location on Raspberry Pi       
fname = 'Three Axes'        # permanent file name where vibration data is stored    
xo = 2090                   # Approximate x-axis zero vibration value            
yo = 2010                   # Approximate y-axis zero vibration value
zo = 2500                   # Approximate z-axis zero vibration value
 
# Start program.
print ("Starting...\n")
input(
    ("Turn on Wi-fi and connect to wifi101-network.\n"
     "Press enter when done\n")
    )

# Run connection test and sensor self test.
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

# Get vehicle name. Set directories.
veh = input("Enter the name of the vehicle (ex: Steve-Toyota).\n")
pathI = path + veh + "-BaseIdle/"
pathAC = path + veh + "-BaseACIdle/"
pathSS = path + veh + "-BaseStdySpd/"
temp = path + "temp/"
temp1 = path + 'temp1/' 

# Check for baseline data and report to user.
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
os.makedirs(temp1)
for j in range(0, samples):
    name = fname + str(j+1)
    num = str(j+1)
    print ('sample #' + num)                                                
    mkr = urllib.request.urlopen("http://192.168.1.1/A")
    accl = mkr.read().decode()
    mkr.close()
    filenam = temp1 + name + '.txt'
    f = open(filenam,"w")
    f.write(accl)
    f.close
print ("done reading")

# Calculate magnitude of the 3-axis vibrations and reduce DC component
os.makedirs(temp)
for j in range(0, samples):
    fname1 = temp1 + fname + str(j+1) + '.txt'
    f=open(fname1,'r')
    data=f.readlines()
    f.close
    fname2 = temp + fname + str(j+1) + '.txt'
    f=open(fname2,'w')
    for i in range(0, len(data)-1):
        row = data[i]
        col = row.split()
        x = float(col[0]) - xo
        y = float(col[1]) - yo
        z = float(col[2]) - zo
        mag = int(math.sqrt(math.pow(x,2)+math.pow(y,2)+math.pow(z,2)))
        data1 = str(col[0]) + ' ' + str(col[1]) + ' ' + str(col[2]) + ' ' + str(mag) + '\n'
        f.write(data1)
    f.close 
shutil.rmtree(temp1)
    
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
            speed1 = int(input('What was the vehicle speed in miles per hour for the test?\n'))
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
            speed1 = int(input('What was the vehicle speed in miles per hour for the test?\n'))
            isgood = True
        except (ValueError):
            print('Please enter a number')
    speed = 5*(round((speed1)/5))
    now = '{:%Y-%b-%d %H:%M}'.format(datetime.datetime.now()) 
    pathTSS = path + now + '-' + veh + '-Stdy-Spd-Trbl' + str(speed) +'MPH/'
    os.makedirs(pathTSS)
    datapath = pathTSS

# Remove samples that did not match test parameters (user determined) 
isgood = False
while isgood == False:
    bdata = input(
        ('Were there samples that did not match the desired conditions?\n'
         '(For example the vehicle slowed down or sped up) Y or N\n')
        )
    if bdata == 'Y' or  bdata == 'y':
        remv = True
        isgood = True
    elif bdata == 'N' or bdata == 'n':
        remv = False
        isgood = True
    else:
        print('Please enter Y or N')
if remv == True:
    bsmpl = input(
        ('Which samples should be removed?\n'
         '(place space between numbers ex: 1 3 4)\n')
        )
    for j in range(1, samples+1):
        if len(bsmpl) == 1:
            k = str(j)
            l = k
        else:
            k = str(j) + ' '
            l = ' ' + str(j)
        if k in bsmpl or bsmpl[-2:] == l:
            rm = 'Sample ' + str(j) + ' removed.'
            print(rm)
            fnmr = temp + fnm + str(j) + '.txt'
            os.remove(fnmr)

# Move remaining files from temp folder and delete temp folder
count = 0
for j in range(1, samples+1):
    fnmt = temp + fname + str(j) + '.txt'
    if  os.path.exists(fnmt)==True:
        count = count + 1
        newfnm = datapath + fname + str(count) + '.txt'
        os.rename(fnmt, newfnm)
os.rmdir(temp)

# read magnitude values from all files into array
mag = numpy.zeros(0)
m = mag
for j in range(0, count):
    filename = datapath + fname + str(j+1) + '.txt'
    f=open(filename,'r')
    data=f.readlines()
    f.close()
    m = numpy.zeros(len(data)-1)
    for i in range(0, len(data)-1):
        row = data[i]        
        col = row.split()
        m[i] = col[2]
    mag = numpy.append(mag,m)
    
# calculate running average of fft
strt = 1
fnsh = n 
smpl = mag[strt:fnsh]
fq=numpy.absolute(numpy.fft.rfft(smpl))
fq[0] = 0
for j in range(1, runav):
    strt = fnsh+1
    fnsh = fnsh+n
    smpl = mag[strt:fnsh]
    fq1=numpy.absolute(numpy.fft.rfft(smpl))
    fq1[0] = 0
    fq = ((fq*j) + fq1)/(j+1)
while (fnsh+n) < len(mag):
    strt = fnsh+1
    fnsh = fnsh+n
    smpl = mag[strt:fnsh]
    fq1=numpy.absolute(numpy.fft.rfft(smpl))
    fq1[0] = 0
    fq = ((fq*runav) + fq1)/(runav+1)
    
# normalize fft
s = numpy.sum(fq)
norm = s/(len(fq))
fq = fq / norm

# write output to file
filename2 = datapath + 'fft' + str(freq/2) + 'Hz.txt'
for i in range(0, int(n/2)):
    hz = float("{0:.1f}".format(i * freq/n))
    enrg = str(hz) + ' ' + str(float("{0:.2f}".format(fq[i]))) + '\n'
    with open(filename2, 'a') as out:
        out.write(enrg)
f.close
freq = freq/2
k=2
while k < 4:
    b, a = signal.butter(20, .5)
    mag1 = signal.filtfilt(b, a, mag)
    stp = (int((len(mag)/k)-runav))
    mag = numpy.zeros(0)
    for i in range(1, stp):
        mag = numpy.append(mag,mag1[(2*i)-1])
    
    # calculate running average of fft
    strt = runav
    fnsh = n + runav-1
    smpl = mag[strt:fnsh]
    fq=numpy.absolute(numpy.fft.rfft(smpl))
    fq[0] = 0
    for j in range(1, runav):
        strt = fnsh+1
        fnsh = fnsh+n
        smpl = mag[strt:fnsh]
        fq1=numpy.absolute(numpy.fft.rfft(smpl))
        fq1[0] = 0
        fq = ((fq*j) + fq1)/(j+1)
    while (fnsh+n) < len(mag):
        strt = fnsh+1
        fnsh = fnsh+n
        smpl = mag[strt:fnsh]
        fq1=numpy.absolute(numpy.fft.rfft(smpl))
        fq1[0] = 0
        fq = ((fq*runav) + fq1)/(runav+1)

    # normalize fft
    s = numpy.sum(fq)
    norm = s/(len(fq))
    fq = fq / norm  

    # write output to file
    filename2 = datapath + 'fft' +str(freq/2) + 'Hz.txt'
    for i in range(0, int(n/2)):
        hz = float("{0:.1f}".format(i * freq/n))
        enrg = str(hz) + ' ' + str(float("{0:.2f}".format(fq[i]))) + '\n'
        with open(filename2, 'a') as out:
            out.write(enrg)
    f.close
    freq = freq/(2)
    k = k+1        

        
    


    





