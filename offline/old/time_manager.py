import math as mt
"""Keeps Track of the Day, Date, and Time"""

#The Calendar
dNames = ['Orgilion', 'Oranor', 'Orithil', 'Orgalad', 'Ormenel', 'Oraearo', 'Orbelain']
dpMonth = [1,30,30,30,30,30,31,1,31,30,30,30,30,30,1]
mNames = ['Yestarë', 'Narwain', 'Nínui', 'Gwaeron', 'Gwirith', 'Lothron', 'Nórui', 'Loëndë', 'Cerveth', 'Urui', 'Ivanneth', 'Narbeleth', 'Hithui', 'Girithron', 'Mettarë']

#Converts date from short to long format
def stlConvert(day, shortDate):
    dDate, mDate, yDate = shortDate
    
    mIndex = mDate
    if mDate > 6:
        mIndex = mt.floor(mIndex)
        mIndex += 1
    if mDate > 12:
        mIndex += 1 
    
    month = mNames[mIndex]
    return [day, dDate, month, yDate]

#Converts date from long to short format
def ltsConvert(longDate):
    day, dDate, month, yDate = longDate
    
    mDate = mNames.index(month)
    if mDate == 7:
        mDate -= 0.5
    if mDate > 7:
        mDate -= 1
    if mDate == 14:
        mDate -= 0.5
    
    shortDate = [dDate, mDate, yDate]
    return [day, shortDate]

#Checks if the date is valid
def checkDate(date):
    
    #Check for form of date
    if len(date) == 4:
        longDate = date
    elif len(date) == 2:
        longDate = stlConvert(date[0], date[1])
    else:
        print('Invalid Date Format')
        return True
    
    #Checks date
    if dpMonth[mNames.index(longDate[2])] < longDate[1]:
        print('Invalid Date')
        return True
    if not longDate[0] in dNames:
        print('Invalid Day')
        return True
    
    return False

def checkTime(time):
    
    if len(time) != 2:
        print('Invalid Time Format')
        return True
    if time[0] > 23:
        print('Invalid Hour')
        return True
    if time[1] > 59:
        print('Invalid Minute')
        return True
    
    return False
    
    
#Increments a time and date by amount specified
def incrementTime(increment, currentTime, date):
    
    #Check date and time are valid
    if checkDate(date) or checkTime(currentTime):
        return currentTime, date
    
    currentDay, currentDate, currentMonth, currentYear = date
    #Date Conversion to Indices
    dIndex = dNames.index(currentDay)
    mIndex = mNames.index(currentMonth)
    
    #Split Time
    tHour = currentTime[0]
    tMin = currentTime[1]
    
    #Move fractions of a day into hours
    increment[0] += (increment[1]-mt.floor(increment[1]))*24
    increment[1] = mt.floor(increment[1])
    
    #Increment Time
    tMin += 15*round((increment[0]-mt.floor(increment[0]))/0.25)
    hIncrement = mt.floor(increment[0])+mt.floor(tMin/60)
    tMin = tMin%60
    tHour += hIncrement
    
    dIncrement = mt.floor(tHour/24) + increment[1]
    
    tHour = tHour%24
    currentTime = [tHour, tMin]
    
    #Increment Day
    currentDay = dNames[(dIndex + dIncrement)%7]
    
    currentDate += dIncrement
    
    #Increment Month with Day
    mIndex += increment[2]
    while currentDate > dpMonth[mIndex%15]:
        currentDate -= dpMonth[mIndex%15]
        mIndex += 1
    
    yIncrement = mt.floor(mIndex/15) + increment[3]
    currentMonth = mNames[mIndex%15]
    
    #Increment Year
    currentYear += yIncrement
    
    #Place back into list
    date = [currentDay, currentDate, currentMonth, currentYear]
    
    return currentTime, date
    