import time, delorean, random, string, threading
from datetime import datetime, date, timedelta
import datetime as dt
# from dateutil import tz
import pytz
from tzlocal.win32 import get_localzone_name

timeZone = pytz.timezone(get_localzone_name())
# tz_string = datetime.now(dt.timezone.utc).astimezone().tzname()

def dat():
    x = datetime.now()

    print("full date and time:", x)
    print("day of the month:", x.day)
    print("month:", x.month)
    print("hour:", x.hour)
    print("minute:", x.minute)
    print("second:", x.second)
    print("min-max:", x.min, x.max)
    print("microsecond:", x.microsecond)
    print("year:", x.year)
    print("day of the week:", x.strftime("%A"), x.strftime("%a"), x.strftime("%w"))
    print("month:", x.strftime("%B"), x.strftime("%b"), x.strftime("%m"))
    print("day of the month:", x.strftime("%d"))
    print("formated date:", x.strftime("%D"))
    print("year:", x.strftime("%y"), x.strftime("%Y"))
    print("hour:", x.strftime("%H"), x.strftime("%I"))
    print("AM/PM:", x.strftime("%p"))
    print("minute:", x.strftime("%M"))
    print("second:", x.strftime("%S"))
    print("microsecond:", x.strftime("%f"))
    print("day of the year:", x.strftime("%j"))
    print("week of the year:", x.strftime("%U"), x.strftime("%W"))
    print("local date and time:", x.strftime("%c"), x.strftime("%x"), x.strftime("%X"))
    print("time:", x.strftime("%X"))
    print("date:", x.strftime("%x"))
    print("time:", x.strftime("%H:%M:%S:%f"))
    print("Format a datetime string: ", datetime(2021, 7, 12, 0, 0))
    print("Today's date:", date.today())
    print("Format a date time string from natural language:", datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p'))
    print("Tomorrow's date:", x + dt.timedelta(days=1))
    print("Yesterday's date:", x + dt.timedelta(days=-1))
    print("formated date:", x.strftime("%Y/%m/%d"))
    # print("timezone:", x.strftime("%Z"))
    # print("UTC Offset:", x.strftime("%z"))
    # print("weekday:", x.weekday)
    # print(x.strftime("%C"))
    # print("time:", x.time)
    # print("date:", x.date)
    # print(timedelta())

def delo():
    datetime_strings = ["Thu July 12 2021", "June 5th, 2021", "April 28th, 2052", "25th of May, 2010", "9:00 on November 30th, 2021", "4th of may 2011", 'january 2022', "2022-08-23 19:01:35.407382"]

    for date in datetime_strings:
        delorean_object = delorean.parse(date, timezone='UTC')
        print(delorean_object)
        human_date = delorean_object.humanize()
        print(human_date)

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
      
    print('Fire in the hole!!')

def countdown2(t):
    time.sleep(t)
    print('Fire in the hole!!')

def fromNow(n = "", unit = "seconds"):
    future = delorean.parse(n, timezone=timeZone).datetime
    # print(future)
    out = None

    diff = future - datetime.now(tz=timeZone)
    # print(diff)
    sec = round(diff.total_seconds(), 2)
    min = round(sec/60)
    hour = round(sec/3600)
    day = round(sec/86400)
    week = round(sec/604800)
    month = round(day/30.4167)
    years = round(day/365.25)

    if unit == "seconds":
        out = sec
    elif unit == "minutes":
        out = min
    elif unit == "hours":
        out = hour
    elif unit == "days":
        out = day
    elif unit == "weeks":
        out = week
    elif unit == "months":
        out = month
    elif unit == "years":
        out = years

    return out

def method1():
    print('hello world')

def waitTime(methodToRun):
    time.sleep(5)
    methodToRun()

def timeToSeconds(time = {}):
    seconds = 0

    for t in time:
        if t == "seconds":
            seconds += time[t]
        elif t == "minutes":
            seconds += time[t] * 60
        elif t == "hours":
            seconds += time[t] * 3600

    return seconds

def timer1(t = 0, message = ""):
    time.sleep(t)

    print(message)
    return message

def UUID(ln = 8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k = ln))

timers = {}
def timer2(t = 60, message = ""):
    timerID = UUID(8)
    while t > 0:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        timers[timerID] = timer
        # print(t, timer, end="\r")
        time.sleep(1)
        t -= 1
      
    print(message)
    return message

class timer:
    def __init__(self, t = 0, message = "", method = None, args = ()):
        self.timeLeft = t
        self.method = method
        self.args = args
        self.message = message
        self.timerID = ''.join(random.choices(string.ascii_letters + string.digits, k = 8))
        self.stop = False
        # self.countdown()
        if self.message:
            threading.Thread(target = self.countdown).start()
        elif self.method:
            threading.Thread(target = self.countdown2).start()

    def getTimeLeft(self):
        return self.timeLeft, divmod(self.timeLeft, 60)

    def countdown(self):
        while self.timeLeft > 0 and not self.stop:
            time.sleep(1)
            self.timeLeft -= 1

        if not self.stop:
            print(self.message)# in the actual code, it would be the address function

    def countdown2(self):
        while self.timeLeft > 0 and not self.stop:
            time.sleep(1)
            self.timeLeft -= 1

        if not self.stop:
            out = self.method(*self.args)
            if out:
                print(out)
            #self.address(method(*args), self.speak)

    def stopTimer(self):
        self.stop = True

    def addTime(self, moreTime):
        self.timeLeft += moreTime

if __name__ == "__main__":
    # dat()
    delo()

    # countdown(int(input("Enter the time in seconds: ")))
    # countdown2(int(input("Enter the time in seconds: ")))

    # print(fromNow("December 25, 2021", "days"))
    # print(fromNow("11:00 December 12, 2021", "minutes"))
    # print(fromNow("December 13, 2021", "seconds"))
    # print(fromNow("2030", "years"))
    # print(fromNow("December 10, 2021", "days"))
    # print(fromNow("thursday", "days"))
    # print(fromNow("december 1st", "days"))
    # print(fromNow("11:00", "minutes"))
    # print(fromNow("11:00 p.m.", "minutes"))
    
    # timeZone = datetime.now(dt.timezone.utc).astimezone().tzname()
    # timeZone = datetime.now(dt.timezone.utc).astimezone()
    # timeZone = datetime.now(dt.timezone.utc)
    # print(timeZone)

    # method1()
    # waitTime(method1)

    # t = {
    #     "elapsed": True,
    #     "hours": 1,
    #     "minutes": 20,
    #     "seconds": 5
    # }
    # print(timeToSeconds(t))

    # timer2(30, "Happy Birthday!!!")
    # testTimer = threading.Thread(target=timer2, args=(30, "Happy Birthday!!!",))
    # testTimer.start()

    # testTimer2 = threading.Thread(target=timer2, args=(45, "Happy Birthday!!!",))
    # testTimer2.start()

    # print(timers)
    # while testTimer.is_alive() or testTimer2.is_alive():
    #     print(timers)
    #     input('> ')

    # test = timer(t = 30, message = "Happy Birthday!!!")
    # # print(test.t, test.message)
    # print(test.getTimeLeft())
    # while True:
    #     m = input('> ')
    #     if m == "stop":
    #         test.stopTimer()
    #         del test
    #         break
    #     elif m.isdigit():
    #         test.addTime(int(m))
    #     print(test.getTimeLeft())

    # timers = []
    # timers.append(timer(t = 15, method=method1, args=()))
    # for i in range(5):
    #     timers.append(timer(t = random.randint(5, 120), message = ''.join(random.choices(string.ascii_letters + string.digits, k = random.randint(2, 50)))))

    # print([x.getTimeLeft() for x in timers])
    # # print(timers[3].message)

    # while True:
    #     m = input('> ')
    #     if m == "stop":
    #         [x.stopTimer() for x in timers]# need to remember to have something that goes through and stops each timer when the thing is closed
    #         break

    #     print([x.getTimeLeft() for x in timers])

    # # test = timer(t = 30, method=print, args=("toot",))
    # test = timer(t = 15, method=method1, args=())
    # # print(test.t, test.message)
    # print(test.getTimeLeft())
    # while True:
    #     m = input('> ')
    #     if m == "stop":
    #         test.stopTimer()
    #         del test
    #         break
    #     print(test.getTimeLeft())

'''
https://stackoverflow.com/questions/466345/converting-string-into-datetime
https://stackoverflow.com/questions/16156597/how-can-i-convert-windows-timezones-to-timezones-pytz-understands

for the timer, i might want to be able to check the time left
    it would have to run in a separate thread
    perhaps i could make it run reccursively? probably is a bad idea

    i could have a while loop that sets a variable each time it goes, kind of like the 'countdown' thing but it would set a variable instead of print
        maybe instead of setting a variable it could set a key/value in a dictionary?
        perhaps each timer could have a UUID? so that when you have multiple going at the same time you can ping a specific one
        or maybe they should use their specified messages as an ID
            that wouldn't work because that would require a message for every timer, you wouldn't be able to have a timer without a message

    i could try making something with oop
        this would allow me to set it up where each one has an ID and can be pinged for its remaining time, and maybe even ended
        this seems to work pretty well
        
        i could also try making a similar one(or modifying this one so) that can take functions as inputs and run them at the end of the timer
        this would be great as it would have the same checkTimeLeft() and stopTimer() functions and would be a step up from the simple functions I made a while back
'''