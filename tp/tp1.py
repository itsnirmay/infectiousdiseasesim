###########################
# plague game for 15-112 tp
# Nirmay Bhanderi (nbhander)
###########################
##############
# data on weekly restaurant visits: https://www.thesimpledollar.com/save-money/dont-eat-out-as-often/#:~:text=The%20average%20American%20eats%20an,month%20eaten%20outside%20the%20home.
# study modelling human intra urban movement : https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0132576

##############
import math, copy, random

#Carnegie Mellon graphics file created by CMU students/staff for use in 15-112 course
from cmu_112_graphics import *
class School(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Park(object):
    def __init__(self, x, y):
        self.x =x 
        self.y =y 

class Restaurant(object):
    def __init__(self, x, y):
        self.x = x
        self.y =y 

class WorkPlace(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class House(object):
    def __init__(self, x, y):
        #top left (x,y) coordinates
        self.x = x
        self.y = y
        self.numPeople = random.randchoice(1,2,3,4)
        self.people = []
        if(self.numPeople == 1 or self.numPeople == 2):
            for x in range(self.numPeople):
                personality = random.randchoice('social', 'isolated', 'safe')
                self.people.append(Person(personality, 'worker'))
        else:
            for x in range(2):
                personality = random.randchoice('social', 'isolated', 'safe')
                self.people.append(Person(personality, 'worker', self.x, self.y))
            for y in range(2):
                personality = random.randchoice('social', 'isolated', 'safe')
                self.people.append(Person(personality, 'student', self.x, self.y))


class Person(object):

    def __init__(self, personality, job,x ,y):
        self.personality = personality
        self.job = job
        self.infected = False
        self.stongerImmunity = random.randchoice('strong', 'weak')
        self.x = x
        self.y = y
        self.homeX = x
        self.homeY = y
        if(self.job == 'worker'):
            self.workPlace = random.randchoice(app.workPlaces)
        if(self.job == 'student'):
            self.school = random.randchoice(app.schools)
        self.placesVisited = []

    def goHome(self):
        self.x = homeX
        self.y = homeY

    def goToSchool(self):
        self.x = self.school.x
        self.y = self.school.y

    def goToWork(self):
        self.x = self.workPlace.x
        self.y = self.workPlace.y
    
    def goToPark(self, Park):
        self.x = park.x
        self.y = park.y
    def goToRestaurant(self, restaurant):
        self.x = restaurant.x
        self.y = restaurant.y

        
def appStarted(app):
    app.gameStarted = False
    app.board = []
    for row in range(40):
        temp = []
        for col in range(40):
            temp.append('white')
        app.board.append(temp)
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
    #chance of infecting others
    app.infectivity = 0
    #chance of death
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



#every second, moves dots and does all of the differnet infection and death things
def timerFired(app):
    pass
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
    for house in app.houses:
        for person in house.people:
            if(app.currDay % 7 < 5):
                if(app.dayTime == 0):
                #if a person is a student, they MUST go to school and come home every weekday
                    if(person.job == 'student'):
                        person.goToSchool()
                        person.atHome = False
                    #workers must go to work every weekday
                    elif(person.job == 'worker'):
                        person.goToWork()
                        person.atHome = False
                #everyone goes home
                elif(app.dayTime == 1):
                    person.goHome()
                    person.atHome = True

                #determines who goes out and who stays in
                elif(app.dayTime == 2):
                    if(person.personality == 'social'):
                        chanceOfGoingOut = 75
                    elif(person.personality == 'isolated'):
                        chanceOfGoingOut = 10
                    elif(person.personality == 'safe'):
                        chanceOfGoingOut = 40
                    randomNum = random.randInt(0,100)
                    if(randomNum < chanceOfGoingOut):
                        placeToGo = random.randchoice('park', 'restaurant', 'friendhouse')
                        if(person.parkVisits <= 1 and 
                           person.notStayingHome and placeToGo == 'Park'):
                            parkToGo = random.randchoice(app.parks)
                            person.goToPark(parkToGo)
                        
                        #average american eats out 4 times a week, this model makes that the max
                        elif(person.restaurantVisits <= 4 and person.notStayingHome 
                            and placeToGo == 'restaurant'):
                            restToGo = random.randchoice(app.restaurants)
                            person.goToRestaurant(restToGo)
                        else:
                            #need to implement some way of forcing that person to stay home
                            placeToGo = person.friendsHouse
                            person.goToFriendsHouse()
                        person.atHome = False
                elif(app.dayTime == 3):
                    person.goHome()
                    person.atHome = True
                        

   

def infect(app, dot1, dot2):
    #given two dots and the infectivity statistics, determines whether one dot will infect another
    pass

def mutations(app):
    #new screen which allows user to pick mutations
    pass
def attributes(app):
    #allow users to edit behaviors of the population
    #both good and bad changes
    pass

def getCellBounds(app, x, y):
    pass
def mousePressed(app, event):
    print(getCell(app, event.x, event.y))
    if(event.y <= 50):
        squareSelected = event.x//200
        print(squareSelected)
        app.pieceSelected = app.buildingList[squareSelected]
        app.selectedName = app.buildingName[squareSelected]
    if(app.pieceSelected != None):
        if(validSelection(app, app.pieceSelected,event.x, event.y)):
            createNewPiece(app,app.pieceSelected, event.x, event.y)
        app.pieceSelected = None
def getCell(app, x, y):
    currCol = (x - 100)//20
    currRow = (y - 100)//20
    return (currCol, currRow)
def validSelection(app, piece, x, y):
    pass
def createNewPiece(app, pieceType, x, y):
    pass




def keyPressed(app, event):
    if(not app.gameStarted):
        app.gameStarted = True
def drawGrid(app, canvas, topMargins,rows, cols):
    cellSize = 20
    for row in range(rows):
        for col in range(cols):
            canvas.create_rectangle(topMargins + cellSize * row, topMargins + cellSize * col,
            topMargins + cellSize * (row + 1), topMargins + cellSize * (col + 1)
            ,fill = app.board[row][col])
def drawCityBuilder(app, canvas):
    if(app.gameStarted):
        canvas.create_rectangle(0,0,200,50, fill = 'blue')
        canvas.create_text(100,25, text = 'house')
        canvas.create_rectangle(200,0,400,50, fill = 'blue')
        canvas.create_text(300,25, text = 'school')
        canvas.create_rectangle(400,0,600,50, fill = 'blue')
        canvas.create_text(500,25, text = 'park')
        canvas.create_rectangle(600,0,800,50, fill = 'blue')
        canvas.create_text(700,25, text = 'restuarant')
        canvas.create_rectangle(800,0,1000,50, fill = 'blue')
        canvas.create_text(900,25, text = 'workplace')
        canvas.create_text(app.width/2,75, text = f'Piece Currently Selected: {app.selectedName}')
        drawGrid(app, canvas, 100, 40, 40)

def startScreen(app, canvas):
    if(not app.gameStarted):
        canvas.create_text(app.width/2, app.height/2, text = 'welcome to disease simulator 1.0')
        canvas.create_text(app.width/2, app.height/2 + 20, text = 'click any key to enter city building mode')
    
def redrawAll(app, canvas):
    startScreen(app, canvas)
    drawCityBuilder(app, canvas)
def main():
    runApp(width = 1000, height = 1000)

if __name__ == '__main__':
    main()