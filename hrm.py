#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tags: hrm, HRM2101, USB, HID, Heart, Rate, OBS
#
"""
Handling raw data inputs example transformed in Heart Rate Monitor reader.
"""
import time
import datetime
from time import sleep
from msvcrt import kbhit
import pywinusb.hid as hid

## Change the values bellow to fit your needs
# Device to search for:
hrmvendor_id = "1130"
hrmproduct_id = "6837"
# How many past values to use for the Average calculation
calcLast = 10
## Change the values above to fit your needs

# When was the max BPM measured and what was the value
maxBPM = 0
maxBPMTime = time.time()
stressTime = time.time()
stressStr = " "

# How many measurments have we made
index = 0

# Initialize the array for the last values
lastValues = []
for x in range(0, calcLast):
    lastValues.insert(x,50)

progressSymbol = ['.',':']
lastTime = time.time()

def hrm_handler(data):
    global lastTime, maxBPM, maxBPMTime, stressTime, stressStr, index, lastValues
    # If you need to debug, uncomment the next row to see the raw data
    # print("Raw: {0}".format(data))
    # The 4th column /data[3]/ gives me a value which I use to determine the pulse type. Seems like 2 and above are reliable.
    # But when I speak and my ears move /yes I have big ears/ it detects it and sends events with 0 and 1. So I gues high numbers is reliable and low - not. We have to filter out > 0.
    if data[3] > 0:
        index+= 1
        diffTime = time.time() - lastTime
        #print(diffTime)
        lastTime = time.time()
        # Ok, so we have the time difference between two beats. 
        # Calculate the beats per minute:
        perSecond = 1/diffTime
        perMinute = int(round(perSecond*60,0))
        # If you moved a lot and lots of events were filtered the calculated BPM would be too low. 
        # Also the new measured BPM will be much higher than the last.
        # So filter:
        averageIndex = index % calcLast
        if perMinute > 50:
            lastValues[averageIndex] = perMinute
            perMinuteAvg = int(sum(lastValues)/len(lastValues))
            if perMinuteAvg >  maxBPM and index > calcLast*2 and perMinute < perMinuteAvg*2:
                maxBPM = perMinute
                maxBPMTime = time.time()
            # The diff between these two columns, in my case, stays normally at 44. When I breath heavy or stop it goed upto 200 and back to 44.
            # So, I'll read this as some kind of a stress
            if abs(data[4]-data[5]) > 100:
                stressTime = time.time()
                stressStr = "!"
            else:
                stressStr = " "
            secondsAgoStress = int(time.time() - stressTime)
            secondsAgoMax = int(time.time() - maxBPMTime)
            #m, s = divmod(secondsAgo, 60)
            #h, m = divmod(m, 60)
            timeAgoStress = str(datetime.timedelta(seconds=secondsAgoStress))
            timeAgoMax = str(datetime.timedelta(seconds=secondsAgoMax))
            # I also print the 5th and 6th values... some day I will figure out what are those :D
            print(progressSymbol[index%len(progressSymbol)], perMinuteAvg, "BPM Avg, Current:", perMinute, "Max BPM:", maxBPM, ",", timeAgoMax, "ago. Last stress was", timeAgoStress, "ago. RAW data: ", data[3], data[4], data[5], abs(data[4]-data[5]), "                                  ", end='\r')
            sys.stdout.flush()
            
            # Put this to text files so we can use OBS
            # Current BPM
            obsFile = open("hrmNow.txt","w")
            obsFile.write(str(perMinuteAvg))
            obsFile.close
            # Max measured BPM
            obsFile = open("hrmMax.txt","w")
            obsFile.write(str(maxBPM))
            obsFile.close
            # When was the max BPM measuered
            obsFile = open("hrmMaxTimeAgo.txt","w")
            obsFile.write(str(timeAgoMax))
            obsFile.close
            # Indicate stress so we can visualize it in OBS
            obsFile = open("hrmStress.txt","w")
            obsFile.write(str(stressStr))
            obsFile.close
            # When was the stress measuered
            obsFile = open("hrmStressTimeAgo.txt","w")
            obsFile.write(str(timeAgoStress))
            obsFile.close
            # Some moving symbos to know if the measurment is going on
            obsFile = open("hrmTickAnimation.txt","w")
            obsFile.write(str(progressSymbol[index%len(progressSymbol)]))
            obsFile.close
            # Histrory data
            obsFile = open("hrmHistory.csv","a")
            colData = [time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time())), str(perMinuteAvg), str(data[3]), str(data[4]), str(data[5]), str(abs(data[4]-data[5]))]
            rowData = ','.join(map(str, colData))
            obsFile.write(str(rowData) + "\n")
            obsFile.close
            
            # It would be also nice to serve this via some http port... so we can combine the Heart rates of several players in one output and put it online.
    
    

def raw_test():
    # simple test
    # browse devices...
    all_hids = hid.find_all_hid_devices()
    if all_hids:
        while True:
            print("Choose a device to monitor:\n")
            print("0 => Exit")
            for index, device in enumerate(all_hids):
                device_name = unicode("{0.vendor_name} {0.product_name}" \
                        "(vID=0x{1:04x}, pID=0x{2:04x})"\
                        "".format(device, device.vendor_id, device.product_id))
                vID = hex(device.vendor_id).split('x')[1]
                pID = hex(device.product_id).split('x')[1]
                try:
                    # Uncomment the next raw to print the list of defices
                    print("{0} => {1}".format(index+1, device_name))
                    if vID == hrmvendor_id and pID == hrmproduct_id:
                        found_option = index+1
                        found_device = device_name
                except:
                    print("Error parsing the name", device.vendor_id, device.product_id )
            print("\n\tDevice ('0' to '%d', '0' to exit?) " \
                    "[press enter after number]:" % len(all_hids))
            if found_option:
                #print("We have found the device")
                index_option = str(found_option)
            else:
                print("Didn't find the vendor and product id. Plug in the device or edit the script and write the correct values")
                index_option = raw_input()
            if index_option.isdigit() and int(index_option) <= len(all_hids):
                # invalid
                break;
        int_option = int(index_option)
        if int_option:
            device = all_hids[int_option-1]
            try:
                device.open()
                #set custom raw data handler
                device.set_raw_data_handler(hrm_handler)
                print("\nWaiting for data...\nPress any (system keyboard) key to stop...")
                while not kbhit() and device.is_plugged():
                    #just keep the device opened to receive events
                    sleep(0.5)
                return
            finally:
                device.close()
    else:
        print("There's not any non system HID class device available")
#
if __name__ == '__main__':
    # first be kind with local encodings
    import sys
    if sys.version_info >= (3,):
        # as is, don't handle unicodes
        unicode = str
        raw_input = input
    else:
        # allow to show encoded strings
        import codecs
        sys.stdout = codecs.getwriter('mbcs')(sys.stdout)
    raw_test()
