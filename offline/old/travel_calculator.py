import random as rdm
"""Calculates the parameters of a journey"""

    
#Calculates the duration of the journey in days
def calcDuration(pace, distance):
    raise NotImplementedError
    
#Determines whether there is an encounter - returning True or False
def calcEncounter(pace, duration, terrain, region):
    raise NotImplementedError
    
#Calculates the difficulty of the journey
def calcDifficulty(pace, distance, terrain):
    raise NotImplementedError
    
#Calculates the nature of the travel - outputs the travel time, difficulty and whether there is an encounter
def calcTravel(pace, distance, terrain, region):
    raise NotImplementedError
    
rdm.choices([True,False], [1,9])[0]
# rdm.choice([Encounters])