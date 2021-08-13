###########################
# plague game for 15-112 tp
# Nirmay Bhanderi (nbhander)
# Saved on github.com
###########################
##############
# data on weekly restaurant visits: https://www.thesimpledollar.com/save-money/dont-eat-out-as-often/#:~:text=The%20average%20American%20eats%20an,month%20eaten%20outside%20the%20home.
# study modelling human intra urban movement : https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0132576
# research on R0 and incubation times: https://web.stanford.edu/~jhj1/teachingdocs/Jones-on-R0.pdf
##############
import math, copy, random

#Carnegie Mellon graphics file created by CMU students/staff for use in 15-112 course
from cmu_112_graphics import *
class School(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.numPeople = 0
        self.people = []


class Park(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col 
        self.numPeople = 0
        self.people = []

class Restaurant(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.numPeople = 0
        self.people = []

class WorkPlace(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.numPeople = 0
        self.people = []

class House(object):
    def __init__(self, row, column):
        #top left row and column coordinates
        self.row = row
        self.col = column
        self.numberPeople = random.choice([1,2,3,4])
        self.numPeople = self.numberPeople
        self.peoples = []
        self.people = []

        if(self.numberPeople == 1 or self.numberPeople == 2):
            for x in range(self.numPeople):
                personality = random.choice(['social', 'isolated', 'safe'])
                self.peoples.append(Person(personality, 'worker', self.row , self.col + x, self))
                self.people.append(Person(personality, 'worker', self.row , self.col + x, self))
        else:
            for x in range(2):
                personality = random.choice(['social', 'isolated', 'safe'])
                self.peoples.append(Person(personality, 'worker', self.row , self.col + x, self))
                self.people.append(Person(personality, 'worker', self.row , self.col + x, self))
            for y in range(self.numberPeople - 2):
                personality = random.choice(['social', 'isolated', 'safe'])
                self.peoples.append(Person(personality, 'student', self.row + 1, self.col + y, self))
                self.people.append(Person(personality, 'student', self.row + 1, self.col + y, self))


class Person(object):

    def __init__(self, personality, job, row ,col, house):
        self.personality = personality
        self.house = house
        self.job = job
        self.infected = False
        self.stongerImmunity = random.choice(['strong', 'weak'])
        self.row = row
        self.col = col
        self.homeRow = row
        self.homeCol = col
        self.workPlace = None
        self.school = None
        self.placesVisited = []
        
        self.incubationTime = None
        self.R0 = None
        self.dailyInfectionAverage = None
        self.parkVisits = 0
        self.restaurantVisits = 0
        self.color = 'light green'
        self.daysSinceInfected = None
        
    def goHome(self):
        self.row = self.homeRow
        self.col = self.homeCol
        #self.house.numPeople += 1

    def goToSchool(self):
        self.row = self.school.row
        self.col = self.school.col
        self.school.numPeople += 1

    def goToWork(self):
        self.row = self.workPlace.row
        self.col = self.workPlace.col
        self.workPlace.numPeople += 1
    
    def goToPark(self, park):
        self.row = park.row
        self.col = park.col
        park.numPeople += 1
    def goToRestaurant(self, restaurant):
        self.row = restaurant.row
        self.col = restaurant.col
        restaurant.numPeople += 1
        
    def initializeR0andIncubationTime(self, R0Low, R0High, incubationTimeLow, incubationTimeHigh):
        self.R0 = random.randint(R0Low, R0High)
        self.incubationTime = random.randint(incubationTimeLow, incubationTimeHigh)
        self.dailyInfectionAverage = self.R0 / self.incubationTime
    def initWorkPlace(self, workPlacesList):
        self.workPlace = random.choice(workPlacesList)
    def initSchool(self, schoolList):
        self.school = random.choice(schoolList)


        
def appStarted(app):
    app.board = []
    for row in range(40):
        temp = []
        for col in range(40):
            temp.append('white')
        app.board.append(temp)
    app.boardCovered = []
    for row in range(40):
        temp = []
        for col in range(40):
            temp.append(False)
        app.boardCovered.append(temp)
    app.house = [
        [True, True],
        [True, True]
    ]

    app.school = [
        [True, True, True],
        [True, True, True]
    ]

    app.park = [
       [True, True, True],
       [True, True, True],
       [True, True, True]
    ]
    app.workPlace = [
       [True, True, True],
       [True, True, True],
       [True, True, True]
    ]
    app.restaurant = [
       [True, True, True],
       [True, True, True],
       [True, True, True]
    ]
    app.buildingList = [app.house, app.school, app.park, app.restaurant, app.workPlace]
    app.buildingName = ['house', 'school', 'park', 'restaurant', 'workPlace']
    app.houses = []
    app.schools = []
    app.parks = []
    app.restaurants = []
    app.workPlaces = []
    app.pieceSelected = None
    app.selectedName = None
    #approximate number of people infected by one person
    #user will input a range of R0 
    app.R0Low = None
    app.R0High = None
    app.incubationTimeLow = None
    app.incubationTimeHigh = None
    #average length of infection, user will input a range here as well
    app.infectivity = None
    #chance of deathz
    app.severity = 0
    #chance of random mutations which could either make the disease more/less severe or infective
    app.mutability = 0

    #0 - Monday, 1 - Tuesday, 2 - Wednesday, 3 - Thursday, 4 - Friday, 5 - Saturday, 6 - Sunday
    app.currDay = 0

    #can be 0 for day or 1 for afternoon or 2 for evening, people go to work/school during 0 
    # and return home at 1 and go to restaurants/park at 2
    #on weekends, people can go to restaurants or parks at either 0 or 1 or 2
    # at time 3, everyone comes home
    app.dayTime = 0
    app.margin = 100
    app.mode1 = True
    app.mode2 = False
    app.mode3 = False
    app.mode4 = False
    app.timeLapse = False
    if not app.timeLapse:
        app.timerDelay = 2000
    else:
        app.timerDelay = 100
    app.pause = False
    app.totalDays = 0
    app.x = None
    app.modeY = False
    app.modeZ = False
    
def initializeSchoolsandWorkplaces(app):
    for house in app.houses:
        for person in house.peoples:
            if(person.job == 'worker'):
                person.initWorkPlace(app.workPlaces)
            else:
                person.initSchool(app.schools)

def initializeR0andIncubation(app):
    for house in app.houses:
        for person in house.peoples:
            person.initializeR0andIncubationTime(app.R0Low, app.R0High, app.incubationTimeLow, app.incubationTimeHigh)
#every second, moves dots and does all of the differnet infection and death things
def timerFired(app):
    if app.pause:
        return
    if not app.mode4:
        return
    
    if(app.dayTime == 3):
       
        app.dayTime = 0
        app.currDay += 1
        app.totalDays += 1
    
    else:app.dayTime += 1
    oneMovement(app)
    
#algorithm to simulate movement for each person each day
def oneMovement(app):
    '''
    algorithmic plan: separate day into 4 times where people can move
    0: people go to school/work, it is assumed that all people go to work/school every weekday, randomly assigned workplace
    1: everyone comes home
    2   : people decide whether they want to go to a restaurant, park, friends house, or stay home
   max amount of times to go to restaurant is 4 a week since that is the average in reality, max park visits is 2
    3: everyone comes home (this is where family spread is calculated)
    '''
    if(app.dayTime == 1):
        for workPlace in app.workPlaces:
            infectionCalculation(app, workPlace)
        for school in app.schools:
            infectionCalculation(app, school)
    
    if(app.dayTime == 3):
        for restaurant in app.restaurants:
            infectionCalculation(app, restaurant)
        for park in app.parks:
            infectionCalculation(app, park)
    if(app.currDay % 7 == 0):
        for house in app.houses:
            for person in house.peoples:
                person.restaurantVisits = 0
                person.parkVisits = 0

    for house in app.houses:
        numGoingOut = 0
        for person in house.peoples:
            
            if(app.currDay % 7 < 5):
                if(app.dayTime == 0):
                #if a person is a student, they MUST go to school and come home every weekday
                    if(person.job == 'student'):
                        person.goToSchool()
                        person.atHome = False
                        person.house.people.remove(person)
                        person.school.people.append(person)
                        
                        
                    #workers must go to work every weekday
                    elif(person.job == 'worker'):
                        person.goToWork()
                        person.house.people.remove(person)
                        person.workPlace.people.append(person)
                        person.atHome = False
                        
                       
                    for House in app.houses:
                        House.numPeople = 0
                        
                #everyone goes home
                elif(app.dayTime == 1):
                    for school in app.schools:
                        if person in school.people:
                            school.people.remove(person)
                    for work in app.workPlaces:
                        if person in work.people:
                            work.people.remove(person)
                    person.goHome()
                    person.house.people.append(person)
                    for house in app.houses:
                        house.numPeople = house.numberPeople
                    person.atHome = True
                    for workPlace in app.workPlaces:
                        workPlace.numPeople = 0
                    for school in app.schools:
                        school.numPeople = 0

                #determines who goes out and who stays in
                elif(app.dayTime == 2):
                    if(person.personality == 'social'):
                        chanceOfGoingOut = 90
                    elif(person.personality == 'isolated'):
                        chanceOfGoingOut = 30
                    elif(person.personality == 'safe'):
                        chanceOfGoingOut = 60
                    randomNum = random.randint(0,100)
                    if(randomNum < chanceOfGoingOut):
                        placeToGo = random.choice(['park', 'restaurant'])
                        numGoingOut += 1
                        if(person.parkVisits <= 1 and placeToGo == 'park'):
                            parkToGo = random.choice(app.parks)
                            person.goToPark(parkToGo)
                            person.parkVisits +=1
                            parkToGo.people.append(person)
                            person.house.people.remove(person)
                        #average american eats out 4 times a week, this model makes that the max
                        elif(person.restaurantVisits <= 4 and placeToGo == 'restaurant'):
                            restToGo = random.choice(app.restaurants)
                            person.goToRestaurant(restToGo)
                            person.restaurantVisits += 1
                            restToGo.people.append(person)
                            person.house.people.remove(person)
                        
                        person.atHome = False
                    
                        
                        
                elif(app.dayTime == 3):
                    for restaurant in app.restaurants:
                        
                        if person in restaurant.people:
                            restaurant.people.remove(person)
                    for park in app.parks:
                       
                        if person in park.people:
                            park.people.remove(person)
                    person.house.people.append(person)
                    person.goHome()
                    person.atHome = True
                    for house in app.houses:
                        house.numPeople = house.numberPeople
                    
                  
                    for restaurant in app.restaurants:
                        restaurant.numPeople = 0
                    for park in app.parks:
                        park.numPeople = 0
                    allInfected = True
                    for house in app.houses:
                        for person in house.peoples:
                            if ( not person.infected):
                                allInfected = False
                    if(allInfected):
                        app.pause = True
                    
            else:
                if(app.dayTime == 0):
                    if(person.personality == 'social'):
                        chanceOfGoingOut = 80
                    elif(person.personality == 'isolated'):
                        chanceOfGoingOut = 30
                    elif(person.personality == 'safe'):
                        chanceOfGoingOut = 50
                    randomNum = random.randint(0,100)
                    if(randomNum < chanceOfGoingOut):
                        placeToGo = random.choice(['park', 'restaurant'])
                        if(person.parkVisits <= 1 and placeToGo == 'park'):
                            parkToGo = random.choice(app.parks)
                            person.goToPark(parkToGo)
                            person.parkVisits +=1
                            parkToGo.people.append(person)
                            person.house.people.remove(person)
                        #average american eats out 4 times a week, this model makes that the max
                        elif(person.restaurantVisits <= 4 and placeToGo == 'restaurant'):
                            restToGo = random.choice(app.restaurants)
                            person.goToRestaurant(restToGo)
                            person.restaurantVisits += 1
                            restToGo.people.append(person)
                            person.house.people.remove(person)
                        person.atHome = False
                        
                elif(app.dayTime == 3):
                    for restaurant in app.restaurants:
                        
                        if person in restaurant.people:
                            restaurant.people.remove(person)
                    for park in app.parks:
                       
                        if person in park.people:
                            park.people.remove(person)
                   
                    person.goHome()
                    person.atHome = True
                    
                    person.house.people.append(person)
                    for restaurant in app.restaurants:
                        restaurant.numPeople = 0
                    for park in app.parks:
                        park.numPeople = 0
                    allInfected = True
                    for house in app.houses:
                        for person in house.peoples:
                            if ( not person.infected):
                                allInfected = False
                    if(allInfected):
                        app.totalDays += 1
                        app.pause = True
        if(app.dayTime == 2):
            house.numPeople = house.numberPeople - numGoingOut          

   
#example : R0: 5 incubation period of 14, infection number of .35, 35% chance of this person spreading the disease on this day, 
# add up the infection numbers and then use random number simulator to determine how many are infected
def infectionCalculation(app,place):

    #given two dots and the infectivity statistics, determines whether one dot will infect another
    #variables considered will be R0, infectivity period(how long the disease is infectious), and the amount of people at a certain place
    numPeopleTotal = place.numPeople
    numInfected = 0
    totalToBeInfected = 0
    infectedList = []
    for person in place.people:
        if person.infected:
            infectedList.append(person)
    totalInfectionAverage = 0
    for person in infectedList:
        totalInfectionAverage += person.dailyInfectionAverage
    
    randNum = random.randint(0,100)
    temp = (totalInfectionAverage % 1)
    if isinstance(place, Park):
        temp /= 2
    if(app.currDay % 7 >= 5):
        temp *= 1.2
    if(randNum < temp * 100):
        totalToBeInfected = int(totalInfectionAverage) + 1
    else: totalToBeInfected = int(totalInfectionAverage)
    
    for person in place.people: 
        if(numInfected == totalToBeInfected):
            break
        if not person.infected:
            person.infected = True
            numInfected += 1
        





    
        
def drawDayTimeandCurrDay(app, canvas):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dayTimes = ['Morning', 'Afternoon', 'Evening', 'Night']
    if not app.mode4:
        return
    canvas.create_text(app.width/2, 50, text = f'It is {days[app.currDay % 7]} {dayTimes[app.dayTime]} ')   
    infectedCount = 0
    totalPeople = 0
    for house in app.houses:
        for person in house.peoples:
            if(person.infected):
                infectedCount += 1  
            totalPeople += 1 
    canvas.create_text(app.width/1.2, 50, text = f'Number of Infected People: {infectedCount}')
    canvas.create_text(70, 50, text = f'Total People = {totalPeople}')
    canvas.create_text(app.width/1.2, 950, text = f'Days Elapsed: {app.totalDays}')


def runCovidPreset(app):
    for x in range(13):
        app.houses.append(House(0, 3 * x))
    for x in range(13):
        app.houses.append(House(3, 3 * x))
    for x in range(3):
        app.schools.append(School(6, 4 * x))
    for x in range(7):
        app.workPlaces.append(WorkPlace(9, 4 * x))
    for x in range(5):
        app.restaurants.append(Restaurant(13, 4 * x))
    for x in range(5):
        app.parks.append(Park(17, 4*x))
    app.houses[0].peoples[0].infected = True
    app.R0Low = 2
    app.R0High = 7
    app.incubationTimeLow = 2
    app.incubationTimeHigh =  14
    initializeR0andIncubation(app)

def mousePressed(app, event):
    if(app.mode1 and event.x >= 100 and event.y <= 300 and event.y >= 100 and event.x <= 300):
        runCovidPreset(app)
        app.mode1 = False
        app.mode4 = True
        initializeSchoolsandWorkplaces(app)
    if app.mode1 and event.x >= 100 and event.x <= 300 and event.y >= 700 and event.y <= 900:
        app.timeLapse = not app.timeLapse
        if(app.timeLapse):
            app.timerDelay = 100
    if app.mode1 and event.x >= 700 and event.x <= 900 and event.y >= 700 and event.y<= 900:
        
        app.mode1 = False
        runMultipleSims(app)
    if(app.mode1 and event.x>= 700 and event.x <= 900 and event.y <= 300 and event.y >= 100):
        app.mode1 = False
        app.mode2 = True
    if not app.mode2:
        return
    if(event.y <= 50):
        squareSelected = event.x//200
        app.pieceSelected = app.buildingList[squareSelected]
        app.selectedName = app.buildingName[squareSelected]
    elif(app.pieceSelected != None):
        if(validSelection(app, app.pieceSelected,event.x, event.y)):
            col, row = getCell(app,event.x,event.y)
            if(app.pieceSelected is app.house):
                app.houses.append(House(row, col))
                for r in range(len(app.house)):
                    for c in range(len(app.house[r])):
                        
                        app.boardCovered[r + col][c + row] = True
                
            
            if(app.pieceSelected is app.park):
                app.parks.append(Park(row,col))
                for r in range(len(app.park)):
                    for c in range(len(app.park[r])):
                        app.boardCovered[r + row][c + col] = True
               
            if(app.pieceSelected is app.restaurant):
                app.restaurants.append(Restaurant(row,col))
                for r in range(len(app.restaurant)):
                    for c in range(len(app.restaurant[r])):
                        app.boardCovered[r + row][c + col] = True
                
            if(app.pieceSelected is app.workPlace):
                app.workPlaces.append(WorkPlace(row,col))
                for r in range(len(app.workPlace)):
                    for c in range(len(app.workPlace[r])):
                        app.boardCovered[r + row][c + col] = True
                
            if(app.pieceSelected is app.school):
                app.schools.append(School(row,col))
                for r in range(len(app.school)):
                    for c in range(len(app.school[r])):
                        app.boardCovered[r + row][c + col] = True
                
            app.pieceSelected = None
            app.selectedName = None
       
def countPerBuilding(app, canvas):
    if not app.mode4:
        return
    for House in app.houses:
        (x0, y0, x1, y1) = getPersonBounds(app, House.row, House.col)
        canvas.create_text(x0 - 20, y0 - 20, text = House.numPeople)
    for workPlace in app.workPlaces:
        (x0, y0, x1, y1) = getPersonBounds(app, workPlace.row, workPlace.col)
        canvas.create_text(x0 - 20, y0 - 20, text = workPlace.numPeople)
    for park in app.parks:
        (x0, y0, x1, y1) = getPersonBounds(app, park.row, park.col)
        canvas.create_text(x0 - 20, y0 - 20, text = park.numPeople)
    for restaurant in app.restaurants:
        (x0, y0, x1, y1) = getPersonBounds(app, restaurant.row, restaurant.col)
        canvas.create_text(x0 - 20, y0 - 20, text = restaurant.numPeople)
    for school in app.schools:
        (x0, y0, x1, y1) = getPersonBounds(app, school.row, school.col)
        canvas.create_text(x0 - 20, y0 - 20, text = school.numPeople)

    return True
def getCell(app, x, y):
    currCol = (x - 100)//20
    currRow = (y - 100)//20
    return (currCol, currRow)

def validSelection(app, piece, x, y):
    
    row, column = getCell(app,x,y)
    
    
    if(column + len(piece[0]) > 40 or row + len(piece) > 40 ):
        return False
    if row < 0 or column < 0:
        return False
    
    """for r in range(len(piece)):
       
        for c in range(len(piece[r])):
            print(r+ row, c + column, app.boardCovered[row + r][column + c])
            
            if(app.boardCovered[row + r ][column + c]):
                return False 
    return True"""
    return True
    
 

def getCellBounds(app, row,col,piece):
    
    x0 = col * 20 + app.margin
    y0 = row * 20 + app.margin 
    x1 = ((col + len(piece[0])) * 20) + app.margin
    y1 = ((row + len(piece)) *20) + app.margin
    return (x0,y0,x1,y1)
def getPersonBounds(app, row, col):
    x0 = col * 20 + app.margin
    y0 = row * 20 + app.margin
    x1 = (col + 1) * 20 + app.margin
    y1 = (row + 1) * 20 + app.margin
    return (x0,y0,x1,y1)
"""def createNewPiece(app, canvas, piece, x, y):
    startRow, startCol = getCell(app,x,y)
    x0,y0,x1,y1 = getCellBounds(app, startRow, startCol, piece)
    canvas.create_rectangle(x0,y0,x1,y1, fill = 'red', width = 0)
    return """
        


def drawHouses(app, canvas):
    if app.mode2 or app.mode4:
        for house in app.houses:
            x0,y0,x1,y1 = getCellBounds(app, house.row, house.col, app.house)
            canvas.create_rectangle(x0,y0,x1,y1, fill = 'light blue')
            canvas.create_text((x0 + x1)/2, (y0 + y1)/2, text = f'House: {house.numPeople}', font = 'Times 10')

def drawSchools(app,canvas):
    if app.mode2 or app.mode4:
        for school in app.schools:
            x0,y0,x1,y1 = getCellBounds(app, school.row, school.col, app.school)
            canvas.create_rectangle(x0,y0,x1,y1, fill = 'IndianRed1')
            canvas.create_text((x0 + x1)/2, (y0 + y1)/2, text = f'School: {school.numPeople}', font = 'Times 10')

def drawWorkPlaces(app,canvas):
    if app.mode2 or app.mode4:
        for work in app.workPlaces:
            x0,y0,x1,y1 = getCellBounds(app, work.row, work.col, app.workPlace)
            canvas.create_rectangle(x0,y0,x1,y1, fill = 'light grey')
            canvas.create_text((x0 + x1)/2, (y0 + y1)/2, text = f'Workplace: {work.numPeople}', font = 'Times 10')

def drawParks(app,canvas):
    if app.mode2 or app.mode4:
        for park in app.parks:
            x0,y0,x1,y1 = getCellBounds(app, park.row, park.col, app.park)
            canvas.create_rectangle(x0,y0,x1,y1, fill = 'light green')
            canvas.create_text((x0 + x1)/2, (y0 + y1)/2, text = f'Park: {park.numPeople}', font = 'Times 10')


def drawRestaurants(app, canvas):
    if app.mode2 or app.mode4:
        for restaurant in app.restaurants:
            x0,y0,x1,y1 = getCellBounds(app, restaurant.row, restaurant.col, app.restaurant)
            canvas.create_rectangle(x0,y0,x1,y1, fill = 'RoyalBlue1')
            canvas.create_text((x0 + x1)/2, (y0 + y1)/2, text = f'Restaurant: {restaurant.numPeople}', font = 'Times 10')

def keyPressed(app, event):
    if(event.key == 'r'):
        app.houses = []
        app.schools = []
        app.parks = []
        app.restaurants = []
        app.workPlaces = []
        app.currDay = 0
        app.dayTime = 0
        app.modeY = False
        app.modeZ = False
        app.mode1 = True
        app.mode2 = False
        app.mode3 = False
        app.mode4 = False
        app.timerDelay = 2000
        app.timeLapse = False
        app.totalDays = 0
        app.R0Low = None
        app.R0High = None
        app.incubationTimeLow = None
        app.incubationTimeHigh = None
        app.pause = False
        app.totalDaysToInfect = None
        app.numSimsToRun = None
        
    if(event.key == 'p'):
        app.pause = not app.pause
    if(app.mode1 and event.key == 's' ):
        app.mode1 = False
        app.mode2 = True
    elif(app.mode2 and event.key == 's' and len(app.workPlaces)>0 and len(app.schools) > 0 and len(app.houses)> 0 and len(app.restaurants)> 0 and len(app.parks) > 0):
        app.mode2 = False
        app.mode3 = True
        
        initializeSchoolsandWorkplaces(app)
        app.R0Low = int(app.getUserInput('Enter the lower bound of your disease\'s R0'))
        if(app.R0Low != None):
            app.R0High = int(app.getUserInput('Enter the upper bound of your disease\'s R0'))
        if(app.R0High != None):
            app.incubationTimeLow = int(app.getUserInput('Enter the lower bound of your disease\'s incubation period'))
        if(app.incubationTimeLow != None):
            app.incubationTimeHigh = int(app.getUserInput('Enter the upper bound of your disease\'s incubation period'))
            initializeR0andIncubation(app)
            app.houses[0].peoples[0].infected = True
            app.mode3 = False
            app.mode4 = True
        
        
           
            
    
    
    
    

        
def drawGrid(app, canvas, topMargins,rows, cols):
    cellSize = 20
    for row in range(rows):
        for col in range(cols):
            canvas.create_rectangle(topMargins + cellSize * row, topMargins + cellSize * col,
            topMargins + cellSize * (row + 1), topMargins + cellSize * (col + 1)
            ,fill = app.board[row][col])

def initializeHumans(app, canvas):
    if not app.mode4:
        return
    for house in app.houses:
        for person in house.peoples:
            (x0,y0,x1,y1) = getPersonBounds(app, person.row, person.col)
            color = 'light green'
            if person.infected:
                color = 'white'
            canvas.create_oval(x0 + 5, y0 + 5, x1 -5, y1-5, fill = color )
def drawCityBuilder(app, canvas):
    if(app.mode2):
        canvas.create_rectangle(0,0,200,50)
        canvas.create_text(100,25, text = 'house')
        canvas.create_rectangle(200,0,400,50)
        canvas.create_text(300,25, text = 'school')
        canvas.create_rectangle(400,0,600,50)
        canvas.create_text(500,25, text = 'park')
        canvas.create_rectangle(600,0,800,50)
        canvas.create_text(700,25, text = 'restaurant')
        canvas.create_rectangle(800,0,1000,50)
        canvas.create_text(900,25, text = 'workplace')
        canvas.create_text(200,75, text = f'Piece Currently Selected: {app.selectedName}')
        canvas.create_text(app.width/2 + 100, 75, text = 'Press s to move to disease creator if one of each building has been placed')
        drawGrid(app, canvas, 100, 40, 40)
def runSim(app):
    runCovidPreset(app)
    initializeSchoolsandWorkplaces(app)
    while not app.pause:
        if(app.dayTime == 3):
       
            app.dayTime = 0
            app.currDay += 1
            app.totalDays += 1
    
        else:app.dayTime += 1
        oneMovement(app)
    numDaysToInfect = app.totalDays
    app.houses = []
    app.schools = []
    app.parks = []
    app.restaurants = []
    app.workPlaces = []
    app.currDay = 0
    app.dayTime = 0
    app.mode1 = True
    app.mode2 = False
    app.mode3 = False
    app.mode4 = False
    app.timerDelay = 2000
    app.timeLapse = False
    app.totalDays = 0
    app.R0Low = None
    app.R0High = None
    app.incubationTimeLow = None
    app.incubationTimeHigh = None
    app.pause = False
    app.x = None
    return numDaysToInfect

def runMultipleSims(app):
    app.modeY = True
    app.numSimsToRun = int(app.getUserInput('Enter an Integer Number of Simulations to Run'))

    app.totalDaysToInfect = 0
    for x in range(app.numSimsToRun):
        app.x = x
        numDaysToInfect = runSim(app)
        app.totalDaysToInfect += numDaysToInfect
    app.modeY = False
    app.mode1 = False
    app.modeZ = True
def drawResultPage(app, canvas):
    if not app.modeZ:
        return
    if app.modeZ:
        averageNumDayToInfect = app.totalDaysToInfect/app.numSimsToRun
        canvas.create_text(app.width/2, app.height/2, text = f'In {app.numSimsToRun} simulations,', font = 'Times 32 bold')
        canvas.create_text(app.width/2, app.height/2 + 25, text = f'the average number of days to infect the whole population was {averageNumDayToInfect}', font = 'Times 32 bold')
        
def drawWaitingPage(app, canvas):
    if not app.modeY:
        return
    canvas.create_rectangle(app.width/2 - 300, app.height/2 - 300, app.width/2 + 300, app.height/2 + 300, fill = 'NavyBlue')
    canvas.create_text(app.width/2, app.height/2, text = 'Currently Running Simulation', font = 'Times 32 bold')
def startScreen(app, canvas):

    if(app.mode1):
        canvas.create_rectangle(app.width/2 - 200, app.height/2 - 100, app.width/2 + 200, app.height/2 + 100, fill = 'RoyalBlue1')
        canvas.create_text(app.width/2, app.height/2 - 40, text = 'Welcome to Infectious Disease Simulation')
        canvas.create_text(app.width/2, app.height/2 , text = 'Press s or Click Turqoise Box to Enter City Building Mode ')
        canvas.create_text(app.width/2, app.height/2 + 40, text =  'Press Pink Box to Simulate Using Preset')
        canvas.create_rectangle(100, 100, 300, 300, fill = 'pink')
        canvas.create_text(200,200, text = 'COVID PRESET')
        canvas.create_rectangle(700, 100, 900, 300, fill = 'Turquoise')
        canvas.create_text(800, 200, text = 'Build your own city and disease')
        canvas.create_rectangle(100, 700, 300, 900, fill = 'Black')
        canvas.create_text(200, 787.5, text = 'Click to Change Timelapse', fill = 'white')
        canvas.create_text(200, 812.5, text = f'Timelapse On = {app.timeLapse}', fill = 'white')
        canvas.create_rectangle(700, 700, 900, 900, fill = 'ivory')
        canvas.create_text(800, 800, text = 'Run Multiple Preset Simulations')
        
        
    
def redrawAll(app, canvas):
    if not app.mode4:
        canvas.create_rectangle(0, 0,  app.width, app.height, fill = 'light green' )
    else: canvas.create_rectangle(0,0,app.width, app.height, fill = 'azure')
    startScreen(app, canvas)
    drawCityBuilder(app, canvas)
    drawHouses(app, canvas)
    drawSchools(app,canvas)
    drawRestaurants(app,canvas)
    drawWorkPlaces(app,canvas)
    drawParks(app, canvas)
    initializeHumans(app, canvas)
    drawDayTimeandCurrDay(app, canvas)
    drawResultPage(app, canvas)
    drawWaitingPage(app,canvas)
def main():
    runApp(width = 1000, height = 1000)

if __name__ == '__main__':
    main()
   