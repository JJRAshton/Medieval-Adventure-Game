import time_manager as tm
# import travel_calculator as tc
# import combat_calculator as cc
"""Runs all Seperate DM Functionalities"""

#Initial Date
startDay = 'Ormenel'
startTime = [15,00]
startDate = [14,12,1967]

#Current Date
currentTime, currentDate = startTime, tm.stlConvert(startDay, startDate)

currentTime, currentDate = tm.incrementTime([0,0,0,0], currentTime, currentDate)