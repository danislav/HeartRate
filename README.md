# HeartRate monitor HRM2101 USB python script

## Why would you need this

I wanted to try a cheap heart rate monitor which is usb connected.
After some digging I found one on the ali express site: "Computer Earlobe Finger Clip USB Heart Rate Monitor" or "IR Finger Clip Sensor USB Heart Rate Monitor"
Just search and you'll find them in many sites. /Links at the end/
It is a simple ear/finger clip which is connected to a small box, which is connected to your computer via usb.
It measures your blood flow difference with an infra-red sensor.

I bought one and was dissapointed from the HRM2101.exe software... not good at all.

Using pywinusb.hid was very easy to write a very simple script which show the heart rate and also outputs to a text file so we can use it in OBS when streaming.  
I just edited the raw_hid example.  
**You need pywinusb**  
Home page: https://github.com/rene-aguirre/pywinusb  
Pypi info page: https://pypi.python.org/pypi/pywinusb/  


## How to use it

Start the script `py hrm.py`  
The script will try to scan for all the available HID devices and find the vID and pID.  
Edit the script to fit your needs.  
In my case it is: `FITCARE RC700(vID=0x1130, pID=0x6837)`.  
The output is on the screen and also in a text file called hrm.txt  
Use the text file when you stream with OBS your cool gaming sessions and show the world how your heart goes wild when you do the play of the game :)  

Press any key while the app window is focused to quit.

**Edit the script to fit your needs**

**Tell me if you find what are those numbers in columns 5 and 6 :)**

## To do

I have to figure out what exactly mean all the values in the output.
Here is an example:  
`[0, 4, 209, 3, 241, 197, 0, 64, 243, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`  
The columns 1, 2 and 3 never changed in my tests.  
Column 4 was 2, 3 and 4 when the clip was reading and I was not disturbing. When you move the clip/put headphones/ the value goes to 0 or sometimes 1. So I decided to use this column to filter bad values.  
Columns 5 and 6 change constantly and would be nice to find out what do they mean.  
Then the next columns also never changed.

## Search engine key words:

HRM2101, Zencro, `USB\VID_1130&PID_6837&REV_0100`, `VID_1130&PID_6837`, FITCARE RC700, usb heart rate, OBS

## Referral

If you find this useful and you will buys something soon, please use the referral links so I can earn some points and buy gadgets :)  
Thank you!  
- AliExpress referral link: http://s.click.aliexpress.com/e/jiI66M3
- Amazon.com referral link: https://www.amazon.com/b?_encoding=UTF8&tag=kostenurka-20&linkCode=ur2&linkId=408218eac4ebd2edd28b9e25128647b5&camp=1789&creative=9325&node=172282
- Amazon.es enlace: https://www.amazon.es/b?_encoding=UTF8&camp=3626&creative=24790&linkCode=ur2&node=599370031&site-redirect=&tag=danislaughblo-21
