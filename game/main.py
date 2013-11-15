'''
Created on Apr 8, 2013

@author: redw0lf
'''
import pygame, sys, os, random, time
from pygame.locals import *
import random
import time

def getCurrentFolder():
    return os.path.dirname(sys.argv[0])

def AAfilledRoundedRect(surface,rect,color,radius=0.4):

    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = Rect(rect)
    color        = Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size,SRCALPHA)

    circle       = pygame.Surface([min(rect.size)*3]*2,SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)

class MenuItem (pygame.font.Font):
    '''
    The Menu Item should be derived from the pygame Font class
    '''
    def __init__(self, text, position, fontSize=36, antialias=1, color=(255, 255, 255), background=None):
        pygame.font.Font.__init__(self, None, fontSize)
        self.text = text
        if background == None:
            self.textSurface = self.render(self.text, antialias, color)
        else:
            self.textSurface = self.render(self.text, antialias, color, background)

        self.position = self.textSurface.get_rect(centerx=position[0], centery=position[1])
    def get_pos(self):
        return self.position
    def get_text(self):
        return self.text
    def get_surface(self):
        return self.textSurface    

class Menu:
    '''
    The Menu should be initalized with a list of menu entries
    it then creates a menu accordingly and manages the different
    print Settings needed
    '''
    
    MENUCLICKEDEVENT = USEREVENT + 1
    
    def __init__(self, menuEntries, menuCenter=None):
        '''
        The constructer uses a list of string for the menu entries,
        which need  to be created
        and a menu center if non is defined, the center of the screen is used
        '''
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.background = pygame.Surface(screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.active = False

        self.blink = 0
        
        if pygame.font:
            fontSize = 36
            fontSpace = 4
            # loads the standard font with a size of 36 pixels
            # font = pygame.font.Font(None, fontSize)
            
            # calculate the height and startpoint of the menu
            # leave a space between each menu entry
            menuHeight = (fontSize + fontSpace) * len(menuEntries)
            startY = self.background.get_height() / 2 - menuHeight / 2  
            
            # listOfTextPositions=list()
            self.menuEntries = list()
            for menuEntry in menuEntries:
                centerX = self.background.get_width() / 2
                centerY = startY + fontSize + fontSpace
                newEnty = MenuItem(menuEntry, (centerX, centerY))
                self.menuEntries.append(newEnty)
                self.background.blit(newEnty.get_surface(), newEnty.get_pos())
                startY = startY + fontSize + fontSpace

            self.bgStars = list()
            w,d = screen.get_size()            
            for i in range(random.randint(6,12)):
                pos = (random.randint(0,w),random.randint(0,d))
                if pos not in self.bgStars:
                    self.bgStars.append(pos)
        
            
    def drawMenu(self):
        self.active = True            
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))
        if self.isActive():
            x,y= pygame.mouse.get_pos()
            for menuItem in self.menuEntries:
                textPos = menuItem.get_pos()
                if x > textPos.left and x < textPos.right and y > textPos.top and y < textPos.bottom:                    
                    f_surce = menuItem.render(menuItem.get_text(),True,(0, 0, 0))
                    self.background.blit(f_surce,menuItem.get_pos())

                    f_surce = menuItem.render(menuItem.get_text(),True,(117, 152, 231))
                    self.background.blit(f_surce,menuItem.get_pos())
                else:                    
                    f_surce = menuItem.render(menuItem.get_text(),True,(255, 255, 255))
                    self.background.blit(f_surce,menuItem.get_pos())
            for i in self.bgStars:
                pygame.draw.circle(screen,(255,255,255),i,(1+(self.blink%60)/25))
            self.blink+=1
            if self.blink> 300:
                self.blink = 0                    
        
    def isActive(self):
        return self.active
    def activate(self,):
        self.active = True
    def deactivate(self):
        self.active = False
    def handleEvent(self, event):
        # only send the event if menu is active
        if event.type == MOUSEBUTTONDOWN and self.isActive():
            # initiate with menu Item 0
            curItem = 0
            # get x and y of the current event 
            eventX = event.pos[0]
            eventY = event.pos[1]
            # for each text position 
            for menuItem in self.menuEntries:
                textPos = menuItem.get_pos()
                # check if current event is in the text area 
                if eventX > textPos.left and eventX < textPos.right \
                and eventY > textPos.top and eventY < textPos.bottom:
                    # if so fire new event, which states which menu item was clicked                        
                    menuEvent = pygame.event.Event(self.MENUCLICKEDEVENT, item=curItem, text=menuItem.get_text())
                    pygame.event.post(menuEvent)
                curItem = curItem + 1
class Game15:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()

        self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","game_15.jpg"))
        self.background = self.background.convert()

        self.screen.blit(self.background,(0,0))

        self.question_answer_dict = {'At an altitude of 30 miles, the shuttle will be travelling at Mach 20. To what does a "Mach" number refer?':['Multiples of the speed of sound','Rate of descent','Rate of acceleration'],
                                     'Discovery is banking 70 degrees to starboard. Brad checks with his computer which tells him that the shuttle now has to bank 40 degrees to port. How long, at 10 degrees per second, will this maneuver take to complete?':['11 seconds','3 seconds','9 seconds','10 seconds'],
                                     'Brad is told to turn towards Edwards AFB. He\'s heading southwest over the desert towards Los Angeles. Which way do you think he should turn?':['Starboard','Port','Continue straight ahead'],
                                     'If Discovery hits tubulence, Brad may be able to do something about it. What causes turbulence?':['Difference in air pressure','Density of clouds','Hot air rising from the land'],
                                     'During the shallow descent towards the base, Discovery passes through a front of clouds. Which have the highest altitude?':['Cirrus','Cumulus','Nimbus'],
                                     'Collision with the stricken A-7 is imminent! Which course of action should Brad take?':['Push control stick forward and turn port','Fire nose retro rockets and turn port','Pull control stick back and turn starboard'],
                                     'Brad now has one last chance to get back on course. He is 1000 feet too high and on a heading of 40 degrees to the right of the runway. What should he do?':['Stick back and left rudder','Stick forward and right rudder','Stick forward and left rudder','Stick back and right rudder'],
                                     'Touchdown! Discovery is thundering along the wet runway. The braking ''chutes open; Brad feels the tug as they slow the shuttle down. Shuddenly the \'chutes fail. Brad now has to brake to stop. To soon and he could skid, too late and he\'ll overshoot. Choose at which distance in feet he should brake!':['500','1000','3000']
                                     }
        self.questions_dict = {}
        self.correct_answers = []
        
        for question in self.question_answer_dict.keys():
            answers = self.question_answer_dict[question]
            self.correct_answers.append(answers[0])
                
            random.shuffle(answers)
            self.questions_dict[question] = answers


        self.question_list = self.question_answer_dict.keys()

        random.shuffle(self.question_list)            

        self.myfont = pygame.font.SysFont('MS Comic Sans',30)

        self.answer_boxes = {}

        self.qPos = 1

        self.current_question = self.question_list[self.qPos-1]

        self.attempts = 0
        self.maxAttempts = 2
        self.success = False

    def isSuccess(self):
        return self.success 
    def isActive(self):
        return self.active
    def activate(self):
        self.active = True        
        
    def deactivate(self):
        self.active = False        
    def drawPart(self):
        self.activate()
        
    def draw(self):
        self.screen.blit(self.background,(0,0))
        if self.attempts < self.maxAttempts:
            line = str(self.qPos) + '. ' + self.current_question
            maxPerLine = 103
            currentY = 35
            x,y = pygame.mouse.get_pos()
            for i in range(1+(len(line)/maxPerLine)):
                trimLine = line[(i*maxPerLine):((i*maxPerLine)+maxPerLine)]
                trimLine = trimLine.strip()
                if len(trimLine) > 1:
                    label = self.myfont.render(trimLine,1,(10,10,15))
                    cX = 10
                    if i > 0:
                        cX = 30
                    self.screen.blit(label,(cX,currentY))
                    currentY+=35

            answerX = 35
            for answer in self.questions_dict[self.current_question]:
                label = self.myfont.render(answer,1,(10,10,15))
                self.screen.blit(label,(answerX,currentY))
                if x > answerX-3 and y > currentY-3 and x < 1000 and y < currentY+30:
                    AAfilledRoundedRect(self.screen,(answerX-3,currentY-3,1000,30),(51,40,40,100))
                    self.answer_boxes[answer] = [answerX-3,currentY-3,answerX+1000,currentY+30]
                currentY+=35

            attemptLine = 'Attempts : ' + str(self.attempts)
            label = self.myfont.render(attemptLine,1,(20,10,255))
            self.screen.blit(label,(50,currentY+35))
        else:
            line = 'Failed Mission'
            mybigfont = pygame.font.SysFont('MS Comic Sans',100)
            label = mybigfont.render(line,1,(255,0,0))
            self.screen.blit(label,(250,500))
            self.deactivate()
                             
            

    def handleEvent(self,event):
        if event.type == MOUSEBUTTONDOWN and self.isActive():
            eventX = event.pos[0]
            eventY = event.pos[1]
            for answer in self.answer_boxes.keys():
                if self.answer_boxes.has_key(answer):
                    rect = self.answer_boxes[answer]
                    if eventX > rect[0] and eventY > rect[1] and eventX < rect[2] and eventY < rect[3]:
                        if answer in self.correct_answers:
                            self.moveToNextQuestion()
                        else:
                            if self.attempts < self.maxAttempts:
                                self.attempts+=1

    def moveToNextQuestion(self):        
        if self.qPos < len(self.question_list) :
            self.qPos+=1
            self.current_question = self.question_list[self.qPos-1]
            self.answer_boxes = {}
        elif self.attempts < self.maxAttempts:
            self.success = True
            mybigfont = pygame.font.SysFont('MS Comic Sans',100)
            label = mybigfont.render('SUCCESS',1,(5,255,255))
            self.screen.blit(label,(250,500))
    
class Game14:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()

        self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","game_14.jpg"))
        self.background = self.background.convert()

        self.screen.blit(self.background,(0,0))

        self.question_answer_dict = {'Discovery will pass through the ozone layer of the Earth\'s atmosphere. This later is important in ...':['Protecting the Earth from ultra-violet light','Burning up meteorites and other debris','Preventing leakage of oxygen molecules'],
                                     'What causes this incredible heating?':['Friction with the atmosphere','Waste heat from motors','A chemical reaction','The Earth\'s magnetic field'],
                                     'All Brad\'s skills as a pilot will be needed to keep the shuttle from overheating. How hot do you think the outer surfaces will get?':['about 2500 C','About 5000 C','About 1500 C'],
                                     'As Discovery starts her descent, Brad notices a flashing light. It is a warning that cabin temperature is going to rise to 81 degrees Farenheit. Will that be a great danger?':['No','Yes','Only for a long period'],
                                     'Brad can see a massive range of mountains 60 miles below that pass through many North American states. What are these?':['The Rocky Mountains','The Great Mountains','The Andes','The Nevada Mountains'],
                                     'Suddenly a computer fails. Brad has to time the final retro firing himself. The shuttle has to slow her speed from 20000 feet per second to 17500 feet per second. Slowing at a rate of 100 feet per second, how long should they fire?':['25 seconds','45 seconds','35 seconds','15 seconds']                                     
                                     }

        self.questions_dict = {}
        self.correct_answers = []
        
        for question in self.question_answer_dict.keys():
            answers = self.question_answer_dict[question]
            self.correct_answers.append(answers[0])
                
            random.shuffle(answers)
            self.questions_dict[question] = answers


        self.question_list = self.question_answer_dict.keys()

        random.shuffle(self.question_list)            

        self.myfont = pygame.font.SysFont('MS Comic Sans',30)

        self.answer_boxes = {}

        self.qPos = 1

        self.current_question = self.question_list[self.qPos-1]

        self.startTime = None       
        self.success = False

    def isSuccess(self):
        return self.success 
    def isActive(self):
        return self.active
    def activate(self):
        self.active = True        
        
    def deactivate(self):
        self.active = False        
    def drawPart(self):
        self.activate()
        if self.startTime == None:
            self.startTime = time.time() 
        
    def draw(self):
        self.screen.blit(self.background,(0,0))
        if self.startTime != None:
            line = str(self.qPos) + '. ' + self.current_question
            maxPerLine = 103
            currentY = 35
            x,y = pygame.mouse.get_pos()
            for i in range(1+(len(line)/maxPerLine)):
                trimLine = line[(i*maxPerLine):((i*maxPerLine)+maxPerLine)]
                trimLine = trimLine.strip()
                if len(trimLine) > 1:
                    label = self.myfont.render(trimLine,1,(0,0,0))
                    cX = 10
                    if i > 0:
                        cX = 30
                    self.screen.blit(label,(cX,currentY))
                    currentY+=35

            answerX = 35
            for answer in self.questions_dict[self.current_question]:
                label = self.myfont.render(answer,1,(0,10,0))
                self.screen.blit(label,(answerX,currentY))
                if x > answerX-3 and y > currentY-3 and x < 1000 and y < currentY+30:
                    AAfilledRoundedRect(self.screen,(answerX-3,currentY-3,1000,30),(251,240,240,100))
                    self.answer_boxes[answer] = [answerX-3,currentY-3,answerX+1000,currentY+30]
                currentY+=35
            
            delta = time.time() - self.startTime
            if delta < 30:
                label = self.myfont.render('Time left',1,(250,100,0))
                self.screen.blit(label,(660,380))
                label = self.myfont.render(str(30-int(delta))+' s',1,(250,100,0))
                self.screen.blit(label,(660,420))
            else:
                self.startTime == None                
                self.deactivate()
                
        else:
            line = 'Failed mission'
            mybigfont = pygame.font.SysFont('MS Comic Sans',100)
            label = mybigfont.render(line,1,(255,0,0))
            self.screen.blit(label,(250,500))            
            self.deactivate()
            

    def handleEvent(self,event):
        if event.type == MOUSEBUTTONDOWN and self.isActive():
            eventX = event.pos[0]
            eventY = event.pos[1]
            for answer in self.answer_boxes.keys():
                if self.answer_boxes.has_key(answer):
                    rect = self.answer_boxes[answer]
                    if eventX > rect[0] and eventY > rect[1] and eventX < rect[2] and eventY < rect[3]:
                        if answer in self.correct_answers:
                            self.moveToNextQuestion()


    def moveToNextQuestion(self):        
        if self.qPos < len(self.question_list) :
            self.qPos+=1
            self.current_question = self.question_list[self.qPos-1]
            self.answer_boxes = {}
        else:
            if self.startTime != None:
                delta = time.time() - self.startTime
                if delta < 30:
                    self.success = True
                    mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                    label = mybigfont.render('SUCCESS',1,(5,255,255))
                    self.screen.blit(label,(250,500))                    
                    self.deactivate()

                
class Game13:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()        
        
        self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","game_11.jpg"))
        self.background = self.background.convert()

        self.screen.blit(self.background,(0,0))

        self.mLayer = pygame.Surface(self.screen.get_size())
        self.mLayer = self.mLayer.convert_alpha() # give it some alpha values
        self.mLayer.fill((0,0,0,0))

        self.myfont = pygame.font.SysFont('MS Comic Sans',30)

        self.sLayer = pygame.Surface(self.screen.get_size())
        self.sLayer = self.mLayer.convert_alpha() # give it some alpha values
        self.sLayer.fill((0,0,0,0))

        self.mazeArray = []
        self.state = 'create'
        for y in xrange(10):
            pygame.draw.line(self.mLayer, (0,250,50,255),(0,y*100),(1000,y*100))
            for x in xrange(10):
                self.mazeArray.append(0x0000)
                if (y==0):                    
                    pygame.draw.line(self.mLayer,(0,250,50,255),(x*100,0),(x*100,1000))

        self.currentCell = 49

        x = (self.currentCell % 10)*100
        y = (self.currentCell / 10)*100
        pygame.draw.rect(self.mLayer, (0,0,95,127), Rect(x+4,y+4,100-4,100-4))
        
        self.endCell = 40
        x = (self.endCell % 10)*100
        y = (self.endCell / 10)*100
        
        pygame.draw.rect(self.mLayer, (255,0,255,127), Rect(x+4,y+4,100-4,100-4))        
        
        self.totalCells = 10*10
        self.cellStack = []

        self.currentCell = random.randint(0,self.totalCells-1)
        self.visitedCells = 1

        self.compass = [(-1,0),(0,1),(1,0),(0,-1)]  #[ West, South, East, North ]
        #self.screen.blit(self.background,(0,0))
        self.startTime = None
        self.success = False

    def isSuccess(self):
        return self.success         
        
    def isActive(self):
        return self.active
    def activate(self):
        self.active = True        
        
    def deactivate(self):
        self.active = False        
    def drawPart(self):
        self.activate()
        
    def update(self):
        if self.state == 'create':
            if self.visitedCells >= self.totalCells:
                self.currentCell = 49 # set current to top-left
                self.cellStack = []
                self.state = 'solve'
                return
            moved = False
            while (self.visitedCells < self.totalCells):            
                x = self.currentCell % 10
                y = self.currentCell / 10
                neighbors = []
                for i in xrange(4):
                    nx = x + self.compass[i][0]
                    ny = y + self.compass[i][1]

                    #check the borders

                    if ((nx >= 0) and (ny >= 0) and (nx < 10) and (ny < 10)):
                        #has it been visited?
                        if (self.mazeArray[(ny*10+nx)] & 0x000F) == 0:
                            nidx = ny * 10 + nx
                            neighbors.append((nidx,1<<i))
                if len(neighbors) > 0:
                    idx = random.randint(0,len(neighbors)-1)
                    nidx,direction = neighbors[idx]
                    dx = x*100
                    dy = y*100
                    if direction & 1:
                        self.mazeArray[nidx] |= (4)
                        pygame.draw.line(self.mLayer,(0,250,50,0), (dx,dy+1),(dx,dy+99))
                    elif direction & 2:
                        self.mazeArray[nidx] |= (8)
                        pygame.draw.line(self.mLayer,(0,250,50,0), (dx+1,dy+100),(dx+99,dy+100))
                    elif direction & 4:
                        self.mazeArray[nidx] |= (1)
                        pygame.draw.line(self.mLayer,(0,250,50,0), (dx+100,dy+1),(dx+100,dy+99))
                    elif direction & 8:
                        self.mazeArray[nidx] |= (2)
                        pygame.draw.line(self.mLayer,(0,250,50,0), (dx+1,dy),(dx+99,dy))
                    pygame.draw.line(self.mLayer,(0,250,50,255),(1000,0),(1000,1000))
                    self.mazeArray[self.currentCell] |= direction
                    self.cellStack.append(self.currentCell)
                    self.currentCell = nidx
                    self.visitedCells = self.visitedCells +1
                    moved = True
                else:
                    self.currentCell=self.cellStack.pop()
        elif self.state == 'solve':
            if self.startTime == None:
                self.startTime = time.time() 
            if self.currentCell == self.endCell: #(self.totalCells-1):
                self.state = 'done'                
                self.success = True
                self.deactivate()
                mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                label = mybigfont.render('SUCCESS',1,(5,255,255))
                self.mLayer.blit(label,(250,500))
                
            if self.currentCell != 49:
                x = (self.currentCell % 10)*100
                y = (self.currentCell / 10)*100
                self.sLayer.fill((0,0,0,0))
                pygame.draw.rect(self.sLayer, (155,100,255,100), Rect(x+4,y+4,100-4,100-4))
            
    def draw(self):
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.mLayer,(0,0))
        self.screen.blit(self.sLayer,(0,0))
        if self.startTime != None:
            pygame.draw.rect(self.mLayer,(0,0,0,0),Rect(1004,30,200,200))
            delta = time.time() - self.startTime
            if delta < 35:
                label = self.myfont.render('Time left',1,(250,100,0))
                self.mLayer.blit(label,(1004,30))
                label = self.myfont.render(str(35-int(delta))+' s',1,(250,100,0))
                self.mLayer.blit(label,(1020,60))
            else:
                self.startTime == None
                self.state = 'd'
                self.deactivate()
                mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                label = mybigfont.render('FAILED',1,(255,0,0))
                self.mLayer.blit(label,(250,500))                
                

    def moveUp(self):
        if self.currentCell > 9:
            if self.mazeArray[self.currentCell] & 8:
                self.currentCell-=10

    def moveDown(self):
        if self.currentCell < (len(self.mazeArray)-10):            
            if self.mazeArray[self.currentCell] & 2:
                self.currentCell+=10


    def moveRight(self):
        if (self.currentCell+1) %10 != 0 :
            if self.mazeArray[self.currentCell] & 4:
                self.currentCell+=1


    def checkMovement(self):
        avl = []
        if self.mazeArray[self.currentCell] & 1:
            avl.append('Left')
        if self.mazeArray[self.currentCell] & 2:
            avl.append('Down')
        if self.mazeArray[self.currentCell] & 4:
            avl.append('Right')
        if self.mazeArray[self.currentCell] & 8:
            avl.append('Up')
                            

    def moveLeft(self):
        if (self.currentCell%10) != 0:
            if self.mazeArray[self.currentCell] & 1:
                self.currentCell-=1
            
    def handleEvent(self,event):
        if self.isActive():            
            if event.type == KEYDOWN:                
                if event.key == pygame.K_UP:
                    self.moveUp()
                elif event.key == pygame.K_DOWN:
                    self.moveDown()
                elif event.key == pygame.K_LEFT:
                    self.moveLeft()
                elif event.key == pygame.K_RIGHT:
                    self.moveRight()    
       
    
    
    
class Game12:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()

        self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","game_12.jpg"))
        self.background = self.background.convert()

        self.screen.blit(self.background,(0,0))

        self.spannerRects = [[289,858,350,961],
                             [378,862,439,965],
                             [469,863,530,966],
                             [288,746,349,849],
                             [380,750,441,853],
                             [472,752,533,855],
                             [565,755,626,858],
                             [778,609,839,712]
                             ]
        self.valveRects = [[266,49,324,105],
                           [450,63,508,119],
                           [556,114,614,170],
                           [746,68,804,124],
                           [355,132,413,188],
                           [255,193,313,249],
                           [549,212,607,268],
                           [331,318,389,374],
                           [777,313,835,369],
                           [516,389,574,445],
                           [445,426,503,482],
                           [607,462,665,518],
                           [762,503,820,559],
                           [264,556,322,612],
                           [485,564,543,620],
                           [558,545,616,601],
                           [660,571,718,627],
                           [256,656,314,712],
                           [444,661,502,717],
                           [1098,998,1100,1000]
                           ]

        self.spannerValveSolution = [[0,13],
                                  [1,3],
                                  [2,8],
                                  [3,4],
                                  [4,18],
                                  [5,15],
                                  [6,1],
                                  [7,6]
                                  ]

        self.selectedSpanner = None
        self.selectedValve = None

        self.correctInputs = []

        self.attempts = 0
        self.maxAttempts = 3

        self.myfont = pygame.font.SysFont('MS Comic Sans',30)
        self.success = False

    def isSuccess(self):
        return self.success         

    def isActive(self):
        return self.active
    def activate(self):
        self.active = True        
        
    def deactivate(self):
        self.active = False        
    def drawPart(self):
        self.activate()

    def draw(self):
        self.screen.blit(self.background,(0,0))
        x,y = pygame.mouse.get_pos()
        if self.attempts < self.maxAttempts:
            for rect in self.spannerRects+self.valveRects:
                if x > rect[0] and y > rect[1] and x < rect[2] and y < rect[3]:
                    AAfilledRoundedRect(self.screen,(rect[0],rect[1],rect[2]-rect[0],rect[3]-rect[1]),(51,40,40,100))

            if self.selectedSpanner:
                pygame.draw.rect(self.screen,(255,25,25),(self.selectedSpanner[0],self.selectedSpanner[1],self.selectedSpanner[2]-self.selectedSpanner[0],self.selectedSpanner[3]-self.selectedSpanner[1]),2)
            if self.selectedValve:
                pygame.draw.rect(self.screen,(255,25,25),(self.selectedValve[0],self.selectedValve[1],self.selectedValve[2]-self.selectedValve[0],self.selectedValve[3]-self.selectedValve[1]),2)

            for idx in self.correctInputs:
                spannerRect = self.spannerRects[idx[0]]
                valveRect = self.valveRects[idx[1]]

                pygame.draw.rect(self.screen,(25,25,255),(spannerRect[0],spannerRect[1],spannerRect[2]-spannerRect[0],spannerRect[3]-spannerRect[1]),2)
                pygame.draw.rect(self.screen,(25,25,255),(valveRect[0],valveRect[1],valveRect[2]-valveRect[0],valveRect[3]-valveRect[1]),2)

            if len(self.correctInputs) == len(self.spannerValveSolution):                
                self.success = False
                self.deactivate()
                mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                label = mybigfont.render('SUCCESS',1,(5,255,255))
                self.screen.blit(label,(250,500))                

            attemptLine = 'Attempts : ' + str(self.attempts)
            label = self.myfont.render(attemptLine,1,(250,100,155))
            self.screen.blit(label,(50,35))
        else:
            line = 'Failed mission'            
            mybigfont = pygame.font.SysFont('MS Comic Sans',100)
            label = mybigfont.render(line,1,(255,0,0))
            self.screen.blit(label,(250,500))
            self.deactivate()
            

    def handleEvent(self,event):
        if event.type == MOUSEBUTTONDOWN and self.isActive():
            x = event.pos[0]
            y = event.pos[1]
            for rect in self.spannerRects:
                if x > rect[0] and y > rect[1] and x < rect[2] and y < rect[3]:
                    self.selectedSpanner = rect
            for rect in self.valveRects:
                if x > rect[0] and y > rect[1] and x < rect[2] and y < rect[3]:
                    self.selectedValve = rect

                    if self.selectedSpanner and self.selectedValve:
                        idx = [self.spannerRects.index(self.selectedSpanner),self.valveRects.index(self.selectedValve)]
                        if idx in self.spannerValveSolution:
                            if idx not in self.correctInputs:
                                self.correctInputs.append(idx)
                                self.selectedSpanner = None
                                self.selectedValve = None
                        else:
                            self.attempts+=1
                                
                
                
class Game11:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()

        self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","game_11.jpg"))
        self.background = self.background.convert()

        self.screen.blit(self.background,(0,0))

        self.mLayer = pygame.Surface(self.screen.get_size())
        self.mLayer = self.mLayer.convert_alpha() # give it some alpha values
        self.mLayer.fill((0,0,0,0))

        self.myfont = pygame.font.SysFont('MS Comic Sans',30)

        self.sLayer = pygame.Surface(self.screen.get_size())
        self.sLayer = self.mLayer.convert_alpha() # give it some alpha values
        self.sLayer.fill((0,0,0,0))

        
        for y in xrange(10):
            pygame.draw.line(self.mLayer, (0,50,50,255),(0,y*100),(1000,y*100))
            for x in xrange(10):
                
                if (y==0):                    
                    pygame.draw.line(self.mLayer,(0,50,50,255),(x*100,0),(x*100,1000))


        self.currentCell = 40

        x = (self.currentCell % 10)*100
        y = (self.currentCell / 10)*100
        pygame.draw.rect(self.mLayer, (0,0,95,127), Rect(x+4,y+4,100-4,100-4))
        
        self.endCell = 49
        x = (self.endCell % 10)*100
        y = (self.endCell / 10)*100
        
        pygame.draw.rect(self.mLayer, (255,0,255,127), Rect(x+4,y+4,100-4,100-4))

        self.totalCells = 10*10

        self.spanners =[]
        for i in range(8):
            done = False
            while not done:
                spanner = random.randint(0,self.totalCells-1)
                if spanner not in self.spanners and spanner != self.currentCell and spanner != self.endCell:
                    self.spanners.append(spanner)
                    done = True


        self.collectedSpanners = []        
        

        self.startTime = None
        self.success = False

    def isSuccess(self):
        return self.success         
    def isActive(self):
        return self.active
    def activate(self):
        self.active = True        
        
    def deactivate(self):
        self.active = False        
    def drawPart(self):
        self.activate()
        
    def update(self):
        if self.startTime == None:
            self.startTime = time.time() 
        if self.currentCell == self.endCell:
            if len(self.collectedSpanners) == len(self.spanners):                
                self.success = True
                mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                label = mybigfont.render('SUCCESS',1,(5,255,255))
                self.mLayer.blit(label,(250,500))                
            else:
                line = 'Failed'
                mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                label = mybigfont.render(line,1,(255,0,0))
                self.mLayer.blit(label,(250,500))
            self.deactivate()
        if self.currentCell != 0:
            x = (self.currentCell % 10)*100
            y = (self.currentCell / 10)*100
            self.sLayer.fill((0,0,0,0))
            pygame.draw.rect(self.sLayer, (155,100,255,100), Rect(x+4,y+4,100-4,100-4))
            if self.currentCell in self.spanners:
                if self.currentCell not in self.collectedSpanners:
                    self.collectedSpanners.append(self.currentCell)
            
    def draw(self):
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.mLayer,(0,0))        
        for spanner in self.spanners:
            spannerImg = pygame.image.load(os.path.join(getCurrentFolder(),"img","spanner.png"))
            spannerImg = spannerImg.convert_alpha()
            x = (spanner % 10) *100
            y = (spanner / 10) *100
            self.screen.blit(spannerImg,(x,y))
            if spanner in self.collectedSpanners:
                pygame.draw.rect(self.sLayer, (100,100,255,100), Rect(x+4,y+4,100-4,100-4))
        self.screen.blit(self.sLayer,(0,0))
        if self.startTime != None:
            pygame.draw.rect(self.mLayer,(0,0,0,0),Rect(1004,30,200,200))
            delta = time.time() - self.startTime
            if delta < 30:
                label = self.myfont.render('Time left',1,(250,100,0))
                self.mLayer.blit(label,(1004,30))
                label = self.myfont.render(str(30-int(delta))+' s',1,(250,100,0))
                self.mLayer.blit(label,(1020,60))
            else:
                self.startTime == None
                self.state = 'd'
                self.deactivate()                
                line = 'Failed misssion'
                mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                label = mybigfont.render(line,1,(255,0,0))
                self.mLayer.blit(label,(250,500))

    def moveUp(self):
        if self.currentCell > 9:            
            self.currentCell-=10

    def moveDown(self):
        if self.currentCell < (self.totalCells-10):                        
            self.currentCell+=10


    def moveRight(self):
        if (self.currentCell+1) %10 != 0 :            
            self.currentCell+=1            

    def moveLeft(self):
        if (self.currentCell%10) != 0:            
            self.currentCell-=1
            
    def handleEvent(self,event):
        if self.isActive():            
            if event.type == KEYDOWN:                
                if event.key == pygame.K_UP:
                    self.moveUp()
                elif event.key == pygame.K_DOWN:
                    self.moveDown()
                elif event.key == pygame.K_LEFT:
                    self.moveLeft()
                elif event.key == pygame.K_RIGHT:
                    self.moveRight()

        
class Game10:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()

        self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","game_10.jpg"))
        self.background = self.background.convert()

        self.screen.blit(self.background,(0,0))

        self.question_answer_dict = {'Brad\'s going on EVA. What does that stand for?':['Extra Vehicular Activity','Egressive Vernacular Automation'],
                                     'A gauge on the suit is reading 0.5 atmospheres. What does this stand for?':['Pressure','Composition','Moisture'],
                                     'The suit helmet has a transceiver within it. What does this allow Brad to do?':['Communicate','Control the back-pack','Eat and drink'],
                                     'The inner suit has small tubes connected to a water tank in the pack. What for?':['To cool the body','To clean the body'],
                                     'The suit back-pack contains gasses. Which should be selected for breathing?':['Oxygen and nitrogen','Argon and oxygen'],
                                     'The six-piece suit is divided into lower, upper and helmet section. What are the other three pieces?':['Back-pack, gloves and boots','back-pack and gloves'],
                                     'Brad has four hours of air. The repairs will take 75 percent of that time. How long has he got to do the repairs and get back?':['3 hours','1 hour','2 hours','4 hours'],
                                     'The visor is coated with gold in order to protect Brad\'s eyes. From what?':['Ultra-violet light','micro-meteorites','sparks'],
                                     'Brad is now ready and heads for the airlock. Why doesn\'t he use the side hatch?':['it will let the air out','it is too small','it is facing the sun'],
                                     'The 2000 liter airlock can be emptied of air at the rate of 25 liters a second. How long will it take to empty?':['80 seconds','60 seconds','50 seconds','25 seconds'],
                                     }
        self.questions_dict = {}
        self.correct_answers = []
        
        for question in self.question_answer_dict.keys():
            answers = self.question_answer_dict[question]
            self.correct_answers.append(answers[0])
                
            random.shuffle(answers)
            self.questions_dict[question] = answers


        self.question_list = self.question_answer_dict.keys()

        random.shuffle(self.question_list)            

        self.myfont = pygame.font.SysFont('MS Comic Sans',30)

        self.answer_boxes = {}

        self.qPos = 1

        self.current_question = self.question_list[self.qPos-1]

        self.attempts = 0
        self.maxAttempts = 2
        self.success = False

    def isSuccess(self):
        return self.success
    
    def isActive(self):
        return self.active
    def activate(self):
        self.active = True        
        
    def deactivate(self):
        self.active = False        
    def drawPart(self):
        self.activate()
        
    def draw(self):
        self.screen.blit(self.background,(0,0))
        if self.attempts < self.maxAttempts:
            line = str(self.qPos) + '. ' + self.current_question
            maxPerLine = 103
            currentY = 35
            x,y = pygame.mouse.get_pos()
            for i in range(1+(len(line)/maxPerLine)):
                trimLine = line[(i*maxPerLine):((i*maxPerLine)+maxPerLine)]
                trimLine = trimLine.strip()
                if len(trimLine) > 1:
                    label = self.myfont.render(trimLine,1,(50,50,5))
                    cX = 10
                    if i > 0:
                        cX = 30
                    self.screen.blit(label,(cX,currentY))
                    currentY+=35

            answerX = 35
            for answer in self.questions_dict[self.current_question]:
                label = self.myfont.render(answer,1,(50,50,5))
                self.screen.blit(label,(answerX,currentY))
                if x > answerX-3 and y > currentY-3 and x < 1000 and y < currentY+30:
                    AAfilledRoundedRect(self.screen,(answerX-3,currentY-3,1000,30),(51,40,40,100))
                    self.answer_boxes[answer] = [answerX-3,currentY-3,answerX+1000,currentY+30]
                currentY+=35

            attemptLine = 'Attempts : ' + str(self.attempts)
            label = self.myfont.render(attemptLine,1,(250,100,155))
            self.screen.blit(label,(50,currentY+35))
        else:
            line = 'Failed mission'
            mybigfont = pygame.font.SysFont('MS Comic Sans',100)
            label = mybigfont.render(line,1,(255,0,0))
            self.screen.blit(label,(250,500))
            self.deactivate()
            

    def handleEvent(self,event):
        if event.type == MOUSEBUTTONDOWN and self.isActive():
            eventX = event.pos[0]
            eventY = event.pos[1]
            for answer in self.answer_boxes.keys():
                if self.answer_boxes.has_key(answer):
                    rect = self.answer_boxes[answer]
                    if eventX > rect[0] and eventY > rect[1] and eventX < rect[2] and eventY < rect[3]:
                        if answer in self.correct_answers:
                            self.moveToNextQuestion()
                        else:
                            if self.attempts < self.maxAttempts:
                                self.attempts+=1

    def moveToNextQuestion(self):        
        if self.qPos < len(self.question_list) :
            self.qPos+=1
            self.current_question = self.question_list[self.qPos-1]
            self.answer_boxes = {}
        elif self.attempts < self.maxAttempts:            
            self.success = True            
            self.deactivate()
            mybigfont = pygame.font.SysFont('MS Comic Sans',100)
            label = mybigfont.render('SUCCESS',1,(5,255,255))
            self.screen.blit(label,(250,500))
                                     
                                     
class Game9:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()        
        
        self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","game_09.jpg"))
        self.background = self.background.convert()

        #self.screen.blit(self.background,(0,0))

        self.mLayer = pygame.Surface(self.screen.get_size())
        self.mLayer = self.mLayer.convert_alpha() # give it some alpha values
        self.mLayer.fill((0,0,0,0))

        self.myfont = pygame.font.SysFont('MS Comic Sans',30)

        self.sLayer = pygame.Surface(self.screen.get_size())
        self.sLayer = self.mLayer.convert_alpha() # give it some alpha values
        self.sLayer.fill((0,0,0,0))

        self.mazeArray = []
        self.state = 'create'
        for y in xrange(10):
            pygame.draw.line(self.mLayer, (0,50,50,255),(0,y*100),(1000,y*100))
            for x in xrange(10):
                self.mazeArray.append(0x0000)
                if (y==0):                    
                    pygame.draw.line(self.mLayer,(0,50,50,255),(x*100,0),(x*100,1000))

        pygame.draw.rect(self.mLayer, (0,0,95,127), Rect(0+4,0+4,100-4,100-4))
        pygame.draw.rect(self.mLayer, (255,0,255,127), Rect((1000-100)+4,(1000-100)+4,100-4,100-4))
        
        self.totalCells = 10*10
        self.cellStack = []

        self.currentCell = random.randint(0,self.totalCells-1)
        self.visitedCells = 1

        self.compass = [(-1,0),(0,1),(1,0),(0,-1)]  #[ West, South, East, North ]
        #self.screen.blit(self.background,(0,0))
        self.startTime = None
        self.success = False

    def isSuccess(self):
        return self.success         
        
    def isActive(self):
        return self.active
    def activate(self):
        self.active = True        
        
    def deactivate(self):
        self.active = False        
    def drawPart(self):
        self.activate()
        
    def update(self):
        if self.state == 'create':
            if self.visitedCells >= self.totalCells:
                self.currentCell = 0 # set current to top-left
                self.cellStack = []
                self.state = 'solve'
                return
            moved = False
            while (self.visitedCells < self.totalCells):            
                x = self.currentCell % 10
                y = self.currentCell / 10
                neighbors = []
                for i in xrange(4):
                    nx = x + self.compass[i][0]
                    ny = y + self.compass[i][1]

                    #check the borders

                    if ((nx >= 0) and (ny >= 0) and (nx < 10) and (ny < 10)):
                        #has it been visited?
                        if (self.mazeArray[(ny*10+nx)] & 0x000F) == 0:
                            nidx = ny * 10 + nx
                            neighbors.append((nidx,1<<i))
                if len(neighbors) > 0:
                    idx = random.randint(0,len(neighbors)-1)
                    nidx,direction = neighbors[idx]
                    dx = x*100
                    dy = y*100
                    if direction & 1:
                        self.mazeArray[nidx] |= (4)
                        pygame.draw.line(self.mLayer,(0,50,50,0), (dx,dy+1),(dx,dy+99))
                    elif direction & 2:
                        self.mazeArray[nidx] |= (8)
                        pygame.draw.line(self.mLayer,(0,50,50,0), (dx+1,dy+100),(dx+99,dy+100))
                    elif direction & 4:
                        self.mazeArray[nidx] |= (1)
                        pygame.draw.line(self.mLayer,(0,50,50,0), (dx+100,dy+1),(dx+100,dy+99))
                    elif direction & 8:
                        self.mazeArray[nidx] |= (2)
                        pygame.draw.line(self.mLayer,(0,50,50,0), (dx+1,dy),(dx+99,dy))
                    pygame.draw.line(self.mLayer,(0,50,50,255),(1000,0),(1000,1000))
                    self.mazeArray[self.currentCell] |= direction
                    self.cellStack.append(self.currentCell)
                    self.currentCell = nidx
                    self.visitedCells = self.visitedCells +1
                    moved = True
                else:
                    self.currentCell=self.cellStack.pop()
        elif self.state == 'solve':
            if self.startTime == None:
                self.startTime = time.time() 
            if self.currentCell == (self.totalCells-1):
                self.state = 'done'                
                self.success = True
                self.deactivate()
                mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                label = mybigfont.render('SUCCESS',1,(5,255,255))
                self.mLayer.blit(label,(250,500))
                
            if self.currentCell != 0:
                x = (self.currentCell % 10)*100
                y = (self.currentCell / 10)*100
                self.sLayer.fill((0,0,0,0))
                pygame.draw.rect(self.sLayer, (155,100,255,100), Rect(x+4,y+4,100-4,100-4))
            
    def draw(self):
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.mLayer,(0,0))
        self.screen.blit(self.sLayer,(0,0))
        if self.startTime != None:
            pygame.draw.rect(self.mLayer,(0,0,0,0),Rect(1004,30,200,200))
            delta = time.time() - self.startTime
            if delta < 30:
                label = self.myfont.render('Time left',1,(250,100,0))
                self.mLayer.blit(label,(1004,30))
                label = self.myfont.render(str(30-int(delta))+' s',1,(250,100,0))
                self.mLayer.blit(label,(1020,60))
            else:
                self.startTime == None
                self.state = 'd'
                self.deactivate()
                mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                label = mybigfont.render('Failed Mission',1,(255,0,0))
                self.mLayer.blit(label,(250,500))

    def moveUp(self):
        if self.currentCell > 9:
            if self.mazeArray[self.currentCell] & 8:
                self.currentCell-=10

    def moveDown(self):
        if self.currentCell < (len(self.mazeArray)-10):            
            if self.mazeArray[self.currentCell] & 2:
                self.currentCell+=10


    def moveRight(self):
        if (self.currentCell+1) %10 != 0 :
            if self.mazeArray[self.currentCell] & 4:
                self.currentCell+=1


    def checkMovement(self):
        avl = []
        if self.mazeArray[self.currentCell] & 1:
            avl.append('Left')
        if self.mazeArray[self.currentCell] & 2:
            avl.append('Down')
        if self.mazeArray[self.currentCell] & 4:
            avl.append('Right')
        if self.mazeArray[self.currentCell] & 8:
            avl.append('Up')
                            

    def moveLeft(self):
        if (self.currentCell%10) != 0:
            if self.mazeArray[self.currentCell] & 1:
                self.currentCell-=1
            
    def handleEvent(self,event):
        if self.isActive():            
            if event.type == KEYDOWN:                
                if event.key == pygame.K_UP:
                    self.moveUp()
                elif event.key == pygame.K_DOWN:
                    self.moveDown()
                elif event.key == pygame.K_LEFT:
                    self.moveLeft()
                elif event.key == pygame.K_RIGHT:
                    self.moveRight()    
class Game8:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()        
        
        self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","game_08.jpg"))
        self.background = self.background.convert()

        #self.screen.blit(self.background,(0,0))

        self.mLayer = pygame.Surface(self.screen.get_size())
        self.mLayer = self.mLayer.convert_alpha() # give it some alpha values
        self.mLayer.fill((0,0,0,0))

        self.myfont = pygame.font.SysFont('MS Comic Sans',30)

        self.sLayer = pygame.Surface(self.screen.get_size())
        self.sLayer = self.mLayer.convert_alpha() # give it some alpha values
        self.sLayer.fill((0,0,0,0))

        self.mazeArray = []
        self.state = 'create'
        for y in xrange(10):
            pygame.draw.line(self.mLayer, (255,255,250,255),(0,y*100),(1000,y*100))
            for x in xrange(10):
                self.mazeArray.append(0x0000)
                if (y==0):                    
                    pygame.draw.line(self.mLayer,(255,255,250,255),(x*100,0),(x*100,1000))

        pygame.draw.rect(self.mLayer, (0,0,255,127), Rect(0+4,0+4,100-4,100-4))
        pygame.draw.rect(self.mLayer, (255,0,255,127), Rect((1000-100)+4,(1000-100)+4,100-4,100-4))
        
        self.totalCells = 10*10
        self.cellStack = []

        self.currentCell = random.randint(0,self.totalCells-1)
        self.visitedCells = 1

        self.compass = [(-1,0),(0,1),(1,0),(0,-1)]  #[ West, South, East, North ]
        #self.screen.blit(self.background,(0,0))
        self.startTime = None
        self.success = False

    def isSuccess(self):
        return self.success         
    def isActive(self):
        return self.active
    def activate(self):
        self.active = True        
        
    def deactivate(self):
        self.active = False        
    def drawPart(self):
        self.activate()
        
    def update(self):
        if self.state == 'create':
            if self.visitedCells >= self.totalCells:
                self.currentCell = 0 # set current to top-left
                self.cellStack = []
                self.state = 'solve'
                return
            moved = False
            while (self.visitedCells < self.totalCells):            
                x = self.currentCell % 10
                y = self.currentCell / 10
                neighbors = []
                for i in xrange(4):
                    nx = x + self.compass[i][0]
                    ny = y + self.compass[i][1]

                    #check the borders

                    if ((nx >= 0) and (ny >= 0) and (nx < 10) and (ny < 10)):
                        #has it been visited?
                        if (self.mazeArray[(ny*10+nx)] & 0x000F) == 0:
                            nidx = ny * 10 + nx
                            neighbors.append((nidx,1<<i))
                if len(neighbors) > 0:
                    idx = random.randint(0,len(neighbors)-1)
                    nidx,direction = neighbors[idx]
                    dx = x*100
                    dy = y*100
                    if direction & 1:
                        self.mazeArray[nidx] |= (4)
                        pygame.draw.line(self.mLayer,(0,0,0,0), (dx,dy+1),(dx,dy+99))
                    elif direction & 2:
                        self.mazeArray[nidx] |= (8)
                        pygame.draw.line(self.mLayer,(0,0,0,0), (dx+1,dy+100),(dx+99,dy+100))
                    elif direction & 4:
                        self.mazeArray[nidx] |= (1)
                        pygame.draw.line(self.mLayer,(0,0,0,0), (dx+100,dy+1),(dx+100,dy+99))
                    elif direction & 8:
                        self.mazeArray[nidx] |= (2)
                        pygame.draw.line(self.mLayer,(0,0,0,0), (dx+1,dy),(dx+99,dy))
                    pygame.draw.line(self.mLayer,(255,255,250,255),(1000,0),(1000,1000))
                    self.mazeArray[self.currentCell] |= direction
                    self.cellStack.append(self.currentCell)
                    self.currentCell = nidx
                    self.visitedCells = self.visitedCells +1
                    moved = True
                else:
                    self.currentCell=self.cellStack.pop()
        elif self.state == 'solve':
            if self.startTime == None:
                self.startTime = time.time() 
            if self.currentCell == (self.totalCells-1):
                self.state = 'done'                
                self.success = True
                self.deactivate()
                mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                label = mybigfont.render('SUCCESS',1,(5,255,255))
                self.mLayer.blit(label,(250,500))
                
            if self.currentCell != 0:
                x = (self.currentCell % 10)*100
                y = (self.currentCell / 10)*100
                self.sLayer.fill((0,0,0,0))
                pygame.draw.rect(self.sLayer, (155,100,255,100), Rect(x+4,y+4,100-4,100-4))
            
    def draw(self):
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.mLayer,(0,0))
        self.screen.blit(self.sLayer,(0,0))
        if self.startTime != None:
            pygame.draw.rect(self.mLayer,(0,0,0,0),Rect(1004,30,200,200))
            delta = time.time() - self.startTime
            if delta < 35:
                label = self.myfont.render('Time left',1,(250,100,0))
                self.mLayer.blit(label,(1004,30))
                label = self.myfont.render(str(35-int(delta))+' s',1,(250,100,0))
                self.mLayer.blit(label,(1020,60))
            else:
                self.startTime == None
                self.state = 'd'
                self.deactivate()
                mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                label = mybigfont.render('Failed Mission',1,(255,0,0))
                self.mLayer.blit(label,(250,500))

    def moveUp(self):
        if self.currentCell > 9:
            if self.mazeArray[self.currentCell] & 8:
                self.currentCell-=10

    def moveDown(self):
        if self.currentCell < (len(self.mazeArray)-10):            
            if self.mazeArray[self.currentCell] & 2:
                self.currentCell+=10


    def moveRight(self):
        if (self.currentCell+1) %10 != 0 :
            if self.mazeArray[self.currentCell] & 4:
                self.currentCell+=1


    def checkMovement(self):
        avl = []
        if self.mazeArray[self.currentCell] & 1:
            avl.append('Left')
        if self.mazeArray[self.currentCell] & 2:
            avl.append('Down')
        if self.mazeArray[self.currentCell] & 4:
            avl.append('Right')
        if self.mazeArray[self.currentCell] & 8:
            avl.append('Up')
                            

    def moveLeft(self):
        if (self.currentCell%10) != 0:
            if self.mazeArray[self.currentCell] & 1:
                self.currentCell-=1

            
    def handleEvent(self,event):
        if self.isActive():            
            if event.type == KEYDOWN:                
                if event.key == pygame.K_UP:
                    self.moveUp()
                elif event.key == pygame.K_DOWN:
                    self.moveDown()
                elif event.key == pygame.K_LEFT:
                    self.moveLeft()
                elif event.key == pygame.K_RIGHT:
                    self.moveRight()
                
                
        
class Game7:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()

        self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","game_07.jpg"))
        self.background = self.background.convert()

        self.screen.blit(self.background,(0,0))

        self.parts = [
                      'Rudder',                      
                      'Thruster Pods',
                      'Launchpad',                      
                      'Air Lock',
                      'Altimeter',
                      'Ejector Seats',
                      'Flame Deflector System',                      
                      'Throttle',
                      'Centrifuge',
                      'Laserbeam',
                      'Gyro',                      
                      'Electrical Generator',                      
                      'Pedestals',
                      'Space Telescope',                      
                      'Artificual Gravity',
                      'Antenna',
                      'Mast',
                      'Clutch',
                      'Indicators',
                      'Gears',
                      'Fuel Coils',
                      'Headlights'
                      ]

        self.solution_parts = self.parts[:7]

        self.inputs = []

        random.shuffle(self.parts)
        
        self.myfont = pygame.font.SysFont('MS Comic Sans',30)

        self.attempts = 0
        self.maxAttempts = 3        
        self.success = False

    def isSuccess(self):
        return self.success 
    def isActive(self):
        return self.active
    def activate(self):
        self.active = True        
        
    def deactivate(self):
        self.active = False        
    def drawPart(self):
        self.activate()
        
    def draw(self):
        self.screen.blit(self.background,(0,0))
        if self.attempts < self.maxAttempts:
            pos = 1
            currentY = 35
            x,y = pygame.mouse.get_pos()
            for part in self.parts:
                line = str(pos) + '. '+ part
                label = self.myfont.render(line,1,(250,255,255))
                self.screen.blit(label,(10,currentY))
                if x > 10-3 and y > currentY-3 and x < 1000 and y < currentY + 30:
                    AAfilledRoundedRect(self.screen,(10-3,currentY-3,1000,30),(251,240,240,100))
                if part in self.inputs:
                    AAfilledRoundedRect(self.screen,(10-3,currentY-3,1000,30),(251,200,200,100))
                currentY+=35
                pos+=1

            attemptLine = 'Attempts : ' + str(self.attempts)
            label = self.myfont.render(attemptLine,1,(250,100,155))
            self.screen.blit(label,(50,currentY+35))
                

        else:
            line = 'Failed mission'
            mybigfont = pygame.font.SysFont('MS Comic Sans',100)
            label = mybigfont.render(line,1,(255,0,0))
            self.screen.blit(label,(250,500))            
            self.deactivate()
            

    def handleEvent(self,event):
        if event.type == MOUSEBUTTONDOWN and self.isActive():
            x = event.pos[0]
            y = event.pos[1]
            currentY = 35
            for part in self.parts:
                if x > 10-3 and y > currentY-3 and x < 1000 and y < currentY + 30:
                    if part in self.solution_parts:
                        if part not in self.inputs:
                            self.inputs.append(part)
                    else:
                        if self.attempts < self.maxAttempts:
                            self.attempts+=1
                currentY+=35
            if self.attempts < self.maxAttempts:
                success = True
                for part in self.solution_parts:
                    if part not in self.inputs:
                        success = False
                if success :                    
                    self.success = True
                    self.deactivate()
                    mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                    label = mybigfont.render('SUCCESS',1,(5,255,255))
                    self.screen.blit(label,(250,500))
        
class Game6:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()

        self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","game_06.jpg"))
        self.background = self.background.convert()

        self.screen.blit(self.background,(0,0))
        self.mLayer = pygame.Surface(self.screen.get_size())
        self.mLayer = self.mLayer.convert_alpha()
        self.mLayer.fill((0, 0, 0, 0))
        self.sLayer = pygame.Surface(self.screen.get_size())
        self.sLayer = self.sLayer.convert_alpha()
        self.sLayer.fill((0, 0, 0, 0))

        self.screen.blit(self.background,(0,0))

        self.mazeArray = []
        self.state = 'c'  # c = creating, p = playing, d = done , s = success, f= failed
        self.myfont = pygame.font.SysFont('MS Comic Sans',30)

        for y in xrange(10): 
            pygame.draw.line(self.mLayer, (255,255,255,255), (0, y*100), (1000, y*100))
            for x in xrange(10):
                self.mazeArray.append(0)
                if ( y == 0 ):
                    pygame.draw.line(self.mLayer, (255,255,255,255), (x*100,0), (x*100,1000))
        pygame.draw.rect(self.sLayer, (0,0,255,127), Rect(0,0,100,100))
        pygame.draw.rect(self.sLayer, (255,0,255,127), Rect((1000-100),(1000-100),100,100))        
        self.totalCells = 100
        self.currentCell = 0
        self.visitedCells = 1
        self.cellStack = []
        self.compass = [(-1,0),(0,1),(1,0),(0,-1)]

        self.bad_elem = ['O','O2','N','SO2','CO','PbO','H']

        self.good_elem = ['Al','Pb','Ag','Au','Pl','Me','Zn']
        self.solution = []
        for n in range(30):
            self.solution.append(random.choice(self.good_elem))         
        
        self.cells = [-1]*100
        self.cells[self.currentCell] = self.solution[self.currentCell]

        self.startTime = None
        self.endTime = None
        
        done = False
        while not done:
            pos = -1
            for i in self.solution[1:]:
                pos+=1

                if (self.currentCell+1)%10 == 0:
                    done = True                    
                    for j in range(self.currentCell,100,10):                        
                        self.cells[j] = self.solution[pos]
                        if len(self.solution) > pos:
                            pos+=1                    
                    break
                    
                
                directions = ['up','down','left','right']                
                if self.currentCell < 10 or self.currentCell >=30:
                    if 'up' in directions:
                        directions.remove('up')
                else:
                    nextCell = self.currentCell-10                
                    if self.cells[nextCell] != -1 and 'up' in directions:
                        directions.remove('up')
                if self.currentCell >= 80:
                    if 'down' in directions:
                        directions.remove('down')
                else:
                    nextCell = self.currentCell+10
                    if self.cells[nextCell] != -1 and 'down' in directions:
                        directions.remove('down')
                    
                if (self.currentCell % 10) == 0 :
                    if 'left' in directions:
                        directions.remove('left')
                else:
                    nextCell = self.currentCell - 1
                    if self.cells[nextCell] != -1 and 'left' in directions:
                        directions.remove('left')
                    
                if (self.currentCell+1) % 10 == 0:
                    if 'right' in directions:
                        directions.remove('right')
                else:
                    nextCell = self.currentCell +1
                    if self.cells[nextCell] != -1 and 'right' in directions:
                        directions.remove('right')
                
                if directions == []:                    
                    break
                direction = random.choice(directions)             
                                
                if direction == 'up':
                    nextCell = self.currentCell-10
                    if self.cells[nextCell] == -1:
                        self.currentCell = nextCell
                        self.cells[nextCell] = i
                if direction == 'down':
                    nextCell = self.currentCell+10
                    if self.cells[nextCell] == -1:
                        self.currentCell = nextCell
                        self.cells[nextCell] = i
                if direction == 'left':
                    nextCell = self.currentCell-1
                    if self.cells[nextCell] == -1:
                        self.currentCell = nextCell
                        self.cells[nextCell] = i
                if direction == 'right':
                    nextCell = self.currentCell+1
                    if self.cells[nextCell] == -1:
                        self.currentCell = nextCell
                        self.cells[nextCell] = i
            if self.cells[-1] in self.solution:
                done = True
            else:
                self.currentCell = 0
                self.cells = [-1]*100
                self.cells[self.currentCell] = self.solution[self.currentCell]                
                
        for ci in range(len(self.cells)):
            if self.cells[ci] == -1:                
                n = random.choice(self.bad_elem)                             
                self.cells[ci] = n                        
        
        self.success = False

    def isSuccess(self):
        return self.success
    
    def handleEvent(self,event):
        if self.isActive():
            if event.type == KEYDOWN:
                if event.key == pygame.K_UP:
                    self.moveUp()
                elif event.key == pygame.K_DOWN:
                    self.moveDown()
                elif event.key == pygame.K_LEFT:
                    self.moveLeft()
                elif event.key == pygame.K_RIGHT:
                    self.moveRight()

    def draw(self):
        if self.state == 'c':
            self.visitedCells = 1
            pos = 0            
            posList = []
            for a in range(10):
                for b in range(10):
                    xpos = self.cells[pos]
                    y = 100*a
                    x = 100*b                            
                    #label = self.myfont.render(str(xpos)+","+str(pos),1,(0,0,0))
                    label = self.myfont.render(str(xpos),1,(250,250,250))
                    self.mLayer.blit(label,(x+30,y+30))
                    pos+=1
            self.state = 'p'
            self.currentCell = 0
            self.visitedCells = [0]
        elif self.state == 'p':
            if self.startTime == None:
                self.startTime = time.time()                           
            for visitedCell in self.visitedCells:
                if visitedCell != 0 and visitedCell != self.currentCell:
                    x = (visitedCell % 10)*100
                    y = (visitedCell / 10)*100
                    if self.cells[visitedCell] in self.solution:                        
                        pygame.draw.rect(self.sLayer, (0,100,255,127), Rect(x,y,100,100))
                    else:
                        pygame.draw.rect(self.sLayer, (255,0,10,127), Rect(x,y,100,100))
            if self.currentCell != 0 and (len(self.cells)-1) != self.currentCell:
                x = (self.currentCell % 10)*100
                y = (self.currentCell / 10)*100
                pygame.draw.rect(self.sLayer, (155,100,255,255), Rect(x,y,100,100))
            elif (len(self.cells)-1) == self.currentCell:
                self.state = 'd'                
        elif self.state == 'd':
            success = True
            pos = 0
            solutionCells = []
            for cell in self.cells:
                if cell in self.good_elem:
                    solutionCells.append(pos)
                    if pos not in self.visitedCells:
                        success = False
                pos+=1
            if success:
                mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                label = mybigfont.render('SUCCESS',1,(5,255,255))
                self.mLayer.blit(label,(250,500))
                self.state = 's'
                self.success = True
                self.deactivate()
            else:
                mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                label = mybigfont.render('FAILED',1,(255,0,0))
                self.mLayer.blit(label,(250,500))
                self.state = 'f'
                self.deactivate()

    
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.sLayer, (0,0))
        self.screen.blit(self.mLayer, (0,0))        
        if self.startTime != None:
            pygame.draw.rect(self.mLayer,(0,0,0,0),Rect(1000,30,200,200))
            delta = time.time() - self.startTime
            if delta < 40:
                label = self.myfont.render('Time left',1,(250,100,0))
                self.mLayer.blit(label,(1000,30))
                label = self.myfont.render(str(40-int(delta))+' s',1,(250,100,0))
                self.mLayer.blit(label,(1020,60))
            else:
                self.startTime == None
                self.state = 'd'
                self.deactivate()

    def moveUp(self):
        if self.currentCell > 9:
            self.currentCell-=10
            self.updateMovement()
    def moveDown(self):
        if self.currentCell < 90:
            self.currentCell+=10
            self.updateMovement()
    def moveLeft(self):
        if (self.currentCell%10) != 0:
            self.currentCell-=1
            self.updateMovement()
    def moveRight(self):
        if (self.currentCell+1)%10 != 0:
            self.currentCell+=1
            self.updateMovement()
            
    def updateMovement(self):
        if self.currentCell not in self.visitedCells:
            self.visitedCells.append(self.currentCell)
        

    def isActive(self):
        return self.active
    def activate(self):
        self.active = True
    def deactivate(self):
        self.active = False
    def drawPart(self):
        self.active = True
            
        
class Game5:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()

        self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","game_05.jpg"))
        self.background = self.background.convert()

        self.screen.blit(self.background,(0,0))

        self.question_answer_dict = {'Brad keeps the bay doors open. They have built in radiators that:':['Cool the payload','Help heat the air','Shed waste heat','Collect radiation'],
                                     'As the two spacecraft close, Jeanne has to maneuver Discovery. She can cause her to roll, pitch and':['Yaw','Decline','Tilt'],
                                     'Now, with the payload bay doors open, Victor has to maneuver the module into the bay using a remote-cotrol "arm". Although the shuttle is just about out of fuel, the arm should be all right, as it uses ...':['Hydraulics','Dynamics','Cryogenics','Laconics'],
                                     'The module needs to match velocity with the shuttle. It\'s on a parallel course, travelling at 17,970 miles an hour. Discovery\'s doing 17,520 mph. It takes the module six minutes to slow down to the shuttle\'s speed. At what rate a minute?':['75 mph','90 mph','105 mph'],
                                     'The module contains a combination of chemicals. In order to allow fuel to burn in space it requires:':['An oxidizer','An energizer','A diluter','An initiator'],
                                     'Along its 240,000-mile straight course from the Moon, Discovery will rendezvous with the module 72,000 miles from Earth. How far is that from the moon?':['168,000 miles','156,000 miles','132,000 miles','108,000 miles'],
                                     'Signals are passed from the shuttle to the module via laser. LASER stands for:':['Light Amplification by Stimulated Emission of Radiation','Light Amplification by Simulated Electrical Radiation'],
                                     'Jeanne notices it\'s getting stuffy in the cabin. What\'s causing it? An increase of:':['Carbon dioxide','Carbon monoxide','Oxygen','Nitrogen'],
                                     'The shuttle uses radar. What sort of radiation does it emit?':['Eletromagnetic','Interatomic','Photonic','Geonic'],
                                     'With Rendezvous imminent, accurate navigation is important. From where was the fuel module launched?':['French Guiana','Kuwait','France','Edwards']}

        self.questions_dict = {}
        self.correct_answers = []
        
        for question in self.question_answer_dict.keys():
            answers = self.question_answer_dict[question]
            self.correct_answers.append(answers[0])
                
            random.shuffle(answers)
            self.questions_dict[question] = answers


        self.question_list = self.question_answer_dict.keys()

        random.shuffle(self.question_list)            

        self.myfont = pygame.font.SysFont('MS Comic Sans',30)

        self.answer_boxes = {}

        self.qPos = 1

        self.current_question = self.question_list[self.qPos-1]

        self.attempts = 0
        self.maxAttempts = 3

        self.success = False

    def isSuccess(self):
        return self.success         

    def isActive(self):
        return self.active
    def activate(self):
        self.active = True        
        
    def deactivate(self):
        self.active = False        
    def drawPart(self):
        self.activate()
        
    def draw(self):
        self.screen.blit(self.background,(0,0))
        if self.attempts < self.maxAttempts:
            line = str(self.qPos) + '. ' + self.current_question
            maxPerLine = 103
            currentY = 35
            x,y = pygame.mouse.get_pos()
            for i in range(1+(len(line)/maxPerLine)):
                trimLine = line[(i*maxPerLine):((i*maxPerLine)+maxPerLine)]
                trimLine = trimLine.strip()
                if len(trimLine) > 1:
                    label = self.myfont.render(trimLine,1,(250,255,255))
                    cX = 10
                    if i > 0:
                        cX = 30
                    self.screen.blit(label,(cX,currentY))
                    currentY+=35

            answerX = 35
            for answer in self.questions_dict[self.current_question]:
                label = self.myfont.render(answer,1,(250,250,255))
                self.screen.blit(label,(answerX,currentY))
                if x > answerX-3 and y > currentY-3 and x < 1000 and y < currentY+30:
                    AAfilledRoundedRect(self.screen,(answerX-3,currentY-3,1000,30),(251,240,240,100))
                    self.answer_boxes[answer] = [answerX-3,currentY-3,answerX+1000,currentY+30]
                currentY+=35

            attemptLine = 'Attempts : ' + str(self.attempts)
            label = self.myfont.render(attemptLine,1,(250,100,155))
            self.screen.blit(label,(50,currentY+35))
        else:
            line = 'Failed mission'
            mybigfont = pygame.font.SysFont('MS Comic Sans',100)
            label = mybigfont.render(line,1,(255,0,0))
            self.screen.blit(label,(250,500))            
            self.deactivate()
            

    def handleEvent(self,event):
        if event.type == MOUSEBUTTONDOWN and self.isActive():
            eventX = event.pos[0]
            eventY = event.pos[1]
            for answer in self.answer_boxes.keys():
                if self.answer_boxes.has_key(answer):
                    rect = self.answer_boxes[answer]
                    if eventX > rect[0] and eventY > rect[1] and eventX < rect[2] and eventY < rect[3]:
                        if answer in self.correct_answers:
                            self.moveToNextQuestion()
                        else:
                            if self.attempts < self.maxAttempts:
                                self.attempts+=1

    def moveToNextQuestion(self):        
        if self.qPos < len(self.question_list) :
            self.qPos+=1
            self.current_question = self.question_list[self.qPos-1]
            self.answer_boxes = {}
        elif self.attempts < self.maxAttempts:            
            self.success = True            
            self.deactivate()
            mybigfont = pygame.font.SysFont('MS Comic Sans',100)
            label = mybigfont.render('SUCCESS',1,(5,255,255))
            self.screen.blit(label,(250,500))
        
        
class Game4:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()

        self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","game_04.jpg"))
        self.background = self.background.convert()

        self.screen.blit(self.background,(0,0))

        self.inputs = []

        self.myfont = pygame.font.SysFont('MS Comic Sans',30)

        self.attempts = 0

        self.status = 'Status : '

        self.solution_parts = [[132,203,339,234],
                               [70,333,247,497],
                               [77,749,244,882],
                               [312,398,480,609],
                               [562,142,691,217],
                               [852,82,1051,209],
                               [818,255,936,308],
                               [1008,350,1098,465]
                                ]

        self.parts = [[78,54,265,174],
                      [360,65,450,100],
                      [680,4,763,86],
                      [424,271,533,410],
                      [619,437,752,521],
                      [738,333,794,409],
                      [20,523,80,566],
                      [123,909,294,961],
                      [880,888,1016,978],
                      [1048,704,1100,848]
                      ]

        self.startTime = None

        self.success = False

    def isSuccess(self):
        return self.success 

    def isActive(self):
        return self.active
    def activate(self):
        self.active = True
        self.startTime = time.time()
        
    def deactivate(self):
        self.active = False        
    def drawPart(self):
        self.activate()
        
    def draw(self):
        self.screen.blit(self.background,(0,0))
        if self.startTime != None:            
            delta = time.time() - self.startTime
            if delta < 60:
                label = self.myfont.render('Time left',1,(250,100,0))
                self.screen.blit(label,(1000,30))
                label = self.myfont.render(str(60-int(delta))+' s',1,(250,100,0))
                self.screen.blit(label,(1020,60))
            else:
                self.startTime == None                    
                self.deactivate()        
        eventX,eventY = pygame.mouse.get_pos()
        for rect in self.parts+self.solution_parts:
            x1,y1,x2,y2 = rect
            if eventX > x1 and eventY > y1 and eventX < x2 and eventY < y2:                
                AAfilledRoundedRect(self.screen,(x1,y1,x2-x1,y2-y1),(251,240,240,100))
##        for rect in self.solution_parts:
##            x1,y1,x2,y2 = rect
##            AAfilledRoundedRect(self.screen,(x1,y1,x2-x1,y2-y1),(51,40,40,100))                
                    
    def handleEvent(self,event):
        if event.type == MOUSEBUTTONDOWN and self.isActive():
            eventX = event.pos[0]
            eventY = event.pos[1]

            if len(self.inputs) != len(self.solution_parts):
                for rect in self.parts+self.solution_parts:
                    x1,y1,x2,y2 = rect
                    if eventX > x1 and eventY > y1 and eventX < x2 and eventY < y2:
                        if rect not in self.inputs:
                            self.inputs.append(rect)
            else:
                correct = True
                for inputRect in self.inputs:
                    if inputRect not in self.solution_parts:
                        correct = False
                if correct :                    
                    self.success = True
                    self.deactivate()
                    mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                    label = mybigfont.render('SUCCESS',1,(5,255,255))
                    self.screen.blit(label,(250,500))
                    
                else:
                    line= 'Failed Mission'
                    self.deactivate()
                    mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                    label = mybigfont.render(line,1,(255,0,0))
                    self.screen.blit(label,(250,500))
                    
            
class Game3:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()

        self.background = pygame.Surface(self.screen.get_size())        
        self.background = self.background.convert()
        self.background.fill((205, 205, 205))

        self.screen.blit(self.background,(0,0))

        self.myfont = pygame.font.SysFont('MS Comic Sans',30)

        self.fuel_types = ['MMH','N204']

        self.inputs = []

        self.success = False

        self.fuel_parts = [1500,2300]
        self.buttons = [-1] * 15

        self.fuel_part_a = [0,0,0]
        self.fuel_part_b = [0,0,0,0]

        self.fuel_part_a[0] = random.randint(1,(self.fuel_parts[0]/100)-1)
        self.fuel_part_a[0]*=100

        print self.fuel_part_a
        
        self.fuel_part_a[1] = random.randint(1,((self.fuel_parts[0]-self.fuel_part_a[0])/50)-2)
        self.fuel_part_a[1]*=50

        print self.fuel_part_a
        
        self.fuel_part_a[2] = self.fuel_parts[0]-self.fuel_part_a[0]-self.fuel_part_a[1]

        print self.fuel_part_a

        self.fuel_part_b[0] = random.randint(1,(self.fuel_parts[1]/100)-2)
        self.fuel_part_b[0]*=100

        print self.fuel_part_b

        self.fuel_part_b[1] = random.randint(1,((self.fuel_parts[1]-self.fuel_part_b[0])/100)-2)
        self.fuel_part_b[1]*=100

        print self.fuel_part_b

        self.fuel_part_b[2] = random.randint(1,((self.fuel_parts[1]-self.fuel_part_b[0]-self.fuel_part_b[1])/50)-2)
        self.fuel_part_b[2]*=50

        print self.fuel_part_b

        self.fuel_part_b[3]=self.fuel_parts[1]-self.fuel_part_b[0]-self.fuel_part_b[1]-self.fuel_part_b[2]

        print self.fuel_part_b
        
        self.buttons[0:3] = self.fuel_part_a
        for i in range(3):
            self.buttons[i] = str(self.buttons[i]) + ' '+self.fuel_types[0]

        self.buttons[3:7] = self.fuel_part_b

        for i in range(3,7):
            self.buttons[i] = str(self.buttons[i]) + ' '+self.fuel_types[1]

        for i in range(len(self.buttons)):
            done = False
            while not done:            
                if self.buttons[i] == -1:
                    p = random.randint(1,random.choice(self.fuel_parts)/50)
                    p*=50
                    pStr = str(p) + ' '+ random.choice(self.fuel_types)
                    if pStr not in self.buttons:
                        self.buttons[i] = pStr
                        done = True
                else:
                    done = True

        random.shuffle(self.buttons)
        self.startTime = None

        
    def isActive(self):
        return self.active
    def activate(self):
        self.active = True
        self.startTime = time.time()
        
    def deactivate(self):
        self.active = False        
    def drawPart(self):
        self.activate()
    def isSuccess(self):
        return self.success         
        
    def draw(self):
        self.screen.blit(self.background,(0,0))
        if self.startTime != None:
            pygame.draw.rect(self.screen,(205, 205, 205),Rect(1000,30,200,200))
            delta = time.time() - self.startTime
            if delta < 60:
                label = self.myfont.render('Time left',1,(250,100,0))
                self.screen.blit(label,(1000,30))
                label = self.myfont.render(str(60-int(delta))+' s',1,(250,100,0))
                self.screen.blit(label,(1020,60))
            else:
                self.startTime == None                    
                self.deactivate()
                
        mouseX,mouseY= pygame.mouse.get_pos()
        for rectPos in range(len(self.buttons)):
            x = 40+(200*(rectPos%5))
            y = 50+(200*(rectPos/5))
            AAfilledRoundedRect(self.screen,(x,y,150,150),(231,225,225,255)) #E7 E1 E1
            if mouseX > x and mouseY > y and mouseX < (x+150) and mouseY < (y+150):
                AAfilledRoundedRect(self.screen,(x,y,150,150),(251,240,240,255))
            label = self.myfont.render(self.buttons[rectPos],1,(0,0,0))
            self.screen.blit(label,(x+20,y+70))

        lb = ['OMU','MUO','UOM']

        for r in range(len(lb)):
            x = 100+(200*(r%5))
            y = 100+(200*3)
            AAfilledRoundedRect(self.screen,(x,y,150,150),(231,225,225,255)) #E7 E1 E1
            if mouseX > x and mouseY > y and mouseX < (x+150) and mouseY < (y+150):
                AAfilledRoundedRect(self.screen,(x,y,150,150),(251,240,240,255))
            label = self.myfont.render(lb[r],1,(0,0,0))
            self.screen.blit(label,(x+20,y+70))
            
                     

    def handleEvent(self,event):
        if event.type == MOUSEBUTTONDOWN and self.isActive():
            eventX = event.pos[0]
            eventY = event.pos[1]
            if len(self.inputs) < 7:
                for rectPos in range(len(self.buttons)):
                    x = 100+(200*(rectPos%5))
                    y = 50+(200*(rectPos/5))
                    if eventX > x and eventY > y and eventX < (x+150) and eventY < (y+150):
                        if self.buttons[rectPos] not in self.inputs:
                            self.inputs.append(self.buttons[rectPos])            
            if eventX > 100 and eventY > 100+(200*3) and eventX < (100+150) and eventY < (100+(200*3)+150):
                #print self.inputs
                total_fuel_a = 0
                total_fuel_b = 0
                cell_a = 0
                cell_b = 0
                for i in self.inputs:
                    if i.find(' MMH') > -1:
                        total_fuel_a+= int(i.split(' M')[0])
                        cell_a+=1
                    if i.find(' N204') > -1:
                        total_fuel_b+= int(i.split(' N')[0])
                        cell_b+=1
                if cell_a == 3 and total_fuel_a == self.fuel_parts[0] and cell_b == 4 and total_fuel_b == self.fuel_parts[1]:                    
                    self.success = True
                    self.deactivate()
                    mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                    label = mybigfont.render('SUCCESS',1,(5,255,255))
                    self.screen.blit(label,(250,500))
                else:
                    line= 'Failed'
                    self.deactivate()
                    mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                    label = mybigfont.render(line,1,(255,0,0))
                    self.screen.blit(label,(250,500))
        
class Game2:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()

        self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","game_02.jpg"))
        self.background = self.background.convert()

        self.screen.blit(self.background,(0,0))

        self.maxAttempts = 3
        self.maxSequenceLength = 20

        self.myfont = pygame.font.SysFont('MS Comic Sans',30)

        self.attempts = 0

        self.status = 'Status : '

        self.resetVars()

        self.leftRect = (29,876,180,989)

        self.rightRect = (642,876,792,989)

        self.upRect = (241,876,382,989)

        self.downRect = (443,876,592,989)

        self.enterRect = (852,921,1038,974)

        self.activate()

        self.success = False

    def isSuccess(self):
        return self.success         

    def resetVars(self):
        self.commands = []
        self.debrisArray = [-1]*30
        self.debris = [7,9,21,28]
        for j in self.debris:
            self.debrisArray[j] = 0

        self.radiationArray = [-1] * 30
        self.radiationArray[27] = 0
        self.radiationArray[24] = 0

        self.currentPos = 1
            
    def draw(self):
        self.screen.blit(self.background,(0,0))
        if self.isActive():           
            x,y= pygame.mouse.get_pos()            
            for rect in [self.leftRect,self.rightRect,self.upRect,self.downRect,self.enterRect]:
                if x > rect[0] and y > rect[1] and x < rect[2] and y < rect[3]:
                    #pygame.draw.rect(self.screen,(255,25,25),(rect[0],rect[1],rect[2]-rect[0],rect[3]-rect[1]),2)
                    AAfilledRoundedRect(self.screen,(rect[0],rect[1],rect[2]-rect[0],rect[3]-rect[1]),(255,25,25,50))
            cmdStatus = [] 
            for command in self.commands:
                if command == 'left':
                    cmdStatus.append('Lft')
                if command == 'right':
                    cmdStatus.append('Rgt')
                if command == 'up':
                    cmdStatus.append('Up')
                if command == 'down':
                    cmdStatus.append('Dwn')
            pygame.draw.rect(self.background,(235,233,196,0),Rect(40,795,1000,50)) #EB E9 C4
            
            cmdStatusStr = 'Commands :' + ",".join(cmdStatus)
            label = self.myfont.render(cmdStatusStr,1,(0,0,0))
            self.background.blit(label,(40,795))

            if self.status != '':                
                label = self.myfont.render(self.status,1,(0,0,0))
                self.background.blit(label,(40,820))
                    
                    
    def isActive(self):
        return self.active
    def activate(self):
        self.active = True
    def deactivate(self):
        self.active = False        
    def drawPart(self):
        self.active = True

    def moveDebris(self):
        self.moveItem(self.debrisArray)

    def moveRadiation(self):
        self.moveItem(self.radiationArray)

    def moveItem(self,array):
        newArray = [-1] * len(array)
        pos = 0
        for j in array:
            if j != -1:
                if pos-3 >= 0:
                    newArray[pos-3] = j
            pos+=1        
        return newArray

    def moveShuttle(self,pos):
        direction = self.commands[pos]
        if direction == 'left':
            if self.currentPos > 0 :
                self.currentPos-=1
        if direction == 'right':
            if self.currentPos < 29:
                self.currentPos+=1
        if direction == 'up':
            if self.currentPos >= 3:
                self.currentPos-=3
        if direction == 'down':
            if self.currentPos < 27:
                self.currentPos+=3
                    
    def calculateAutopilot(self):        
        colided = False
        for commandPos in range(len(self.commands)):            
            self.moveDebris()
            if commandPos != 0 and (commandPos%5) == 0:
                self.moveRadiation()
            self.moveShuttle(commandPos)
            if self.debrisArray[self.currentPos] == 0 or self.radiationArray[self.currentPos] == 0:
                colided = True
                break
        if colided:
            self.attempts+=1
            self.resetVars()
            self.status = 'Status : Failed at attempt ' + str(self.attempts)
            mybigfont = pygame.font.SysFont('MS Comic Sans',100)
            label = mybigfont.render(self.status,1,(255,0,0))
            self.screen.blit(label,(250,500))
        else:
            self.status = 'Status : Success'
            self.success = True
            self.deactivate()

            mybigfont = pygame.font.SysFont('MS Comic Sans',100)
            label = mybigfont.render(self.status,1,(5,255,255))
            self.mLayer.blit(label,(250,500))

            

    def handleEvent(self,event):
        if event.type == MOUSEBUTTONDOWN and self.isActive():
            eventX = event.pos[0]
            eventY = event.pos[1]            
            if len(self.commands) < self.maxSequenceLength and self.attempts <= self.maxAttempts:
                if eventX > self.leftRect[0] and eventY > self.leftRect[1] and eventX < self.leftRect[2] and eventY < self.leftRect[3]:                    
                    self.commands.append('left')
                if eventX > self.rightRect[0] and eventY > self.rightRect[1] and eventX < self.rightRect[2] and eventY < self.rightRect[3]:                    
                    self.commands.append('right')
                if eventX > self.upRect[0] and eventY > self.upRect[1] and eventX < self.upRect[2] and eventY < self.upRect[3]:                    
                    self.commands.append('up')
                if eventX > self.downRect[0] and eventY > self.downRect[1] and eventX < self.downRect[2] and eventY < self.downRect[3]:                    
                    self.commands.append('down')
            if eventX > self.enterRect[0] and eventY > self.enterRect[1] and eventX < self.enterRect[2] and eventY < self.enterRect[3]:
                if self.attempts < self.maxAttempts:                 
                    colision = self.calculateAutopilot()
                else:
                    self.status = 'Status : Failed. Maximum attempts reached'
                    mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                    label = mybigfont.render(self.status,1,(255,0,0))
                    self.screen.blit(label,(250,500))
                    
                
        
class Game1:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()

        self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","game_01.jpg"))
        self.background = self.background.convert()

        self.mLayer = pygame.Surface(self.screen.get_size())
        self.mLayer = self.mLayer.convert_alpha()
        self.mLayer.fill((0, 0, 0, 0))
        self.sLayer = pygame.Surface(self.screen.get_size())
        self.sLayer = self.sLayer.convert_alpha()
        self.sLayer.fill((0, 0, 0, 0))

        self.screen.blit(self.background,(0,0))

        self.mazeArray = []
        self.state = 'c'  # c = creating, p = playing, d = done , s = success, f= failed
        self.myfont = pygame.font.SysFont('MS Comic Sans',30)

        for y in xrange(10): 
            pygame.draw.line(self.mLayer, (255,255,255,255), (0, y*100), (1000, y*100))
            for x in xrange(10):
                self.mazeArray.append(0)
                if ( y == 0 ):
                    pygame.draw.line(self.mLayer, (255,255,255,255), (x*100,0), (x*100,1000))
        pygame.draw.rect(self.sLayer, (0,0,255,127), Rect(0,0,100,100))
        pygame.draw.rect(self.sLayer, (255,0,255,127), Rect((1000-100),(1000-100),100,100))        
        self.totalCells = 100
        self.currentCell = 0
        self.visitedCells = 1
        self.cellStack = []
        self.compass = [(-1,0),(0,1),(1,0),(0,-1)]
        self.solution = range(108,0,-3)
        
        self.cells = [-1]*100
        self.cells[self.currentCell] = self.solution[self.currentCell]
        #self.cells[-1] = self.solution[-1]
        self.startTime = None
        self.endTime = None

        self.success = False
        
        done = False
        while not done:
            pos = -1
            for i in self.solution[1:]:
                pos+=1
##                if self.currentCell >=90:
##                    done = True
##                    for j in range(self.currentCell,100):
##                        self.cells[j]=self.solution[pos]
##                        if len(self.solution) <= pos:
##                            pos+=1
##                    break

                if (self.currentCell+1)%10 == 0:
                    done = True                    
                    for j in range(self.currentCell,100,10):                        
                        self.cells[j] = self.solution[pos]
                        if len(self.solution) > pos:
                            pos+=1                    
                    break
                    
                
                directions = ['up','down','left','right']                
                if self.currentCell < 10 or self.currentCell >=30:
                    if 'up' in directions:
                        directions.remove('up')
                else:
                    nextCell = self.currentCell-10                
                    if self.cells[nextCell] != -1 and 'up' in directions:
                        directions.remove('up')
                if self.currentCell >= 80:
                    if 'down' in directions:
                        directions.remove('down')
                else:
                    nextCell = self.currentCell+10
                    if self.cells[nextCell] != -1 and 'down' in directions:
                        directions.remove('down')
                    
                if (self.currentCell % 10) == 0 :
                    if 'left' in directions:
                        directions.remove('left')
                else:
                    nextCell = self.currentCell - 1
                    if self.cells[nextCell] != -1 and 'left' in directions:
                        directions.remove('left')
                    
                if (self.currentCell+1) % 10 == 0:
                    if 'right' in directions:
                        directions.remove('right')
                else:
                    nextCell = self.currentCell +1
                    if self.cells[nextCell] != -1 and 'right' in directions:
                        directions.remove('right')
                
                if directions == []:                    
                    break
                direction = random.choice(directions)             
                                
                if direction == 'up':
                    nextCell = self.currentCell-10
                    if self.cells[nextCell] == -1:
                        self.currentCell = nextCell
                        self.cells[nextCell] = i
                if direction == 'down':
                    nextCell = self.currentCell+10
                    if self.cells[nextCell] == -1:
                        self.currentCell = nextCell
                        self.cells[nextCell] = i
                if direction == 'left':
                    nextCell = self.currentCell-1
                    if self.cells[nextCell] == -1:
                        self.currentCell = nextCell
                        self.cells[nextCell] = i
                if direction == 'right':
                    nextCell = self.currentCell+1
                    if self.cells[nextCell] == -1:
                        self.currentCell = nextCell
                        self.cells[nextCell] = i
            if self.cells[-1] in self.solution:
                done = True
            else:
                self.currentCell = 0
                self.cells = [-1]*100
                self.cells[self.currentCell] = self.solution[self.currentCell]
                
        for ci in range(len(self.cells)):
            if self.cells[ci] == -1:
                done = False
                n = random.randint(1,108)
                while not done:
                    n = random.randint(1,108)
                    if n not in self.solution:
                        done = True                        
                self.cells[ci] = n                        


    def update(self):
        if self.state == 'c':
            self.visitedCells = 1
            pos = 0            
            posList = []
            for a in range(10):
                for b in range(10):
                    xpos = self.cells[pos]
                    y = 100*a
                    x = 100*b                            
                    #label = self.myfont.render(str(xpos)+","+str(pos),1,(0,0,0))
                    label = self.myfont.render(str(xpos),1,(250,250,250))
                    self.mLayer.blit(label,(x+30,y+30))
                    pos+=1
            self.state = 'p'
            self.currentCell = 0
            self.visitedCells = [0]
        elif self.state == 'p':
            if self.startTime == None:
                self.startTime = time.time()                           
            for visitedCell in self.visitedCells:
                if visitedCell != 0 and visitedCell != self.currentCell:
                    x = (visitedCell % 10)*100
                    y = (visitedCell / 10)*100
                    if self.cells[visitedCell] in self.solution:                        
                        pygame.draw.rect(self.sLayer, (0,100,255,127), Rect(x,y,100,100))
                    else:
                        pygame.draw.rect(self.sLayer, (255,0,10,127), Rect(x,y,100,100))
            if self.currentCell != 0 and (len(self.cells)-1) != self.currentCell:
                x = (self.currentCell % 10)*100
                y = (self.currentCell / 10)*100
                pygame.draw.rect(self.sLayer, (155,100,255,255), Rect(x,y,100,100))
            elif (len(self.cells)-1) == self.currentCell:
                self.state = 'd'                
        elif self.state == 'd':
            success = True
            lastSolution = self.solution.index(self.cells[-1])
            solutionCells = []
            for sol in self.solution[:lastSolution]:                
                solutionCells.append(self.cells.index(sol))
            for sol in solutionCells:
                if sol not in self.visitedCells:
                    success = False
            if success:
                mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                label = mybigfont.render('SUCCESS',1,(5,255,255))
                self.mLayer.blit(label,(250,500))
                self.state = 's'
                self.deactivate()                
                self.success = True
            else:
                mybigfont = pygame.font.SysFont('MS Comic Sans',100)
                label = mybigfont.render('FAILED',1,(255,0,0))
                self.mLayer.blit(label,(250,500))
                self.state = 'f'                
                self.deactivate()

    def draw(self):
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.sLayer, (0,0))
        self.screen.blit(self.mLayer, (0,0))        
        if self.startTime != None:
            pygame.draw.rect(self.mLayer,(0,0,0,0),Rect(1000,30,200,200))
            delta = time.time() - self.startTime
            if delta < 45:
                label = self.myfont.render('Time left',1,(250,100,0))
                self.mLayer.blit(label,(1000,30))
                label = self.myfont.render(str(45-int(delta))+' s',1,(250,100,0))
                self.mLayer.blit(label,(1020,60))
            else:
                self.startTime == None
                self.state = 'd'
                self.deactivate()

    def moveUp(self):
        if self.currentCell > 9:
            self.currentCell-=10
            self.updateMovement()
    def moveDown(self):
        if self.currentCell < 90:
            self.currentCell+=10
            self.updateMovement()
    def moveLeft(self):
        if (self.currentCell%10) != 0:
            self.currentCell-=1
            self.updateMovement()
    def moveRight(self):
        if (self.currentCell+1)%10 != 0:
            self.currentCell+=1
            self.updateMovement()
    def updateMovement(self):
        if self.currentCell not in self.visitedCells:
            self.visitedCells.append(self.currentCell)

    def isActive(self):
        return self.active
    def activate(self):
        self.active = True
    def deactivate(self):
        self.active = False
    def drawPart(self):
        self.active = True

    def isSuccess(self):
        return self.success 

class IntroGame:
    MENUCLICKEDEVENT = USEREVENT + 1
    def __init__(self,part):
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.part = part
        
        if self.part in ['1','2','3','4','5','6']:
            self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","intoPart.jpg"))
            self.background = self.background.convert()
        elif self.part in ['7','8','9']:
            self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","intoPart_02.jpg"))
            self.background = self.background.convert()
        elif self.part in ['10','11','12','13','14','15']:
            self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","intoPart_03.jpg"))
            self.background = self.background.convert()
        elif self.part in ['16']:
            self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","ending.jpg"))
            self.background = self.background.convert()
        else:
            self.background = pygame.Surface(screen.get_size())
            self.background = self.background.convert()            
            self.background.fill((0, 0, 0))
            
        self.active = False

        self.textStory = ""

        self.setText()

        self.textNext = "Start"
        if self.part in ['16']:
            self.textNext = "Finish"

        if pygame.font:
            fontSize = 25
            fontSpace = 2

            xOffset = 0
            if self.part in ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']:
                xOffset = 150
            if self.part in ['16']:
                xOffset = 10
            
            
            centerY = xOffset+(fontSize/2)
            x = fontSize*2
            y = xOffset+fontSize
            myfont = pygame.font.SysFont('MS Comic Sans',25)
            for line in self.textStory.split("\n"):                
                #nCenterX = ((len(line))*((fontSize/5)))-5
                #newEnty = MenuItem(line, (nCenterX, centerY),fontSize=fontSize)                
                #self.background.blit(newEnty.get_surface(), newEnty.get_pos())
                centerY+=fontSize+fontSpace

                label = myfont.render(line,1,(0,0,0))
                self.background.blit(label,(x,y))
                y+=fontSize+fontSpace
                
            centerX = self.background.get_width()-150
            self.nextTxt = MenuItem(self.textNext,(centerX,centerY+10),fontSize=fontSize,color=(0,0,0))
            self.background.blit(self.nextTxt.get_surface(), self.nextTxt.get_pos())

            self.centerY = centerY
           

    def setText(self):
        if self.part == '1':
            self.textStory = '''
The LTV is approaching Rook Mountain base and has to slow down using its retro rocket.
Help guide it into land by tracking across the grid to the landing pad.
Follow the course suggested by a continuation of the following sequence of numbers:
114,111,108 ...
The numbers represent speed in feet per second and the LTV
must be doing no more than 3 feet per second upon touchdown.
You now have 45 seconds worth of fuel in which to make the landing.
Move with the arrow keys.'''
        if self.part == '2':
            self.textStory = '''
Discovery is in a perilous position. Debris and radiation clouds are hurlin towards her.
Some are on a direct collision course. The shuttle must take action to avoid certain disaster!
Navigate a course through the debris from the view of the screen through to the autopilot.
Remember: both discovery and the fragments are moving towards each other at great speed.
Their velocities are given at the top of the screen. The direction of the obstacles is towards
the shuttle as indicated by arrows.
The skill is in predicting just where the debris will be after you have made each move.
Select the correct sequence of movement (max 20) using the mouse
and then click "Enter" to attempt to initiate autopilot.
You are allowed 3 attempts.
'''
        if self.part == '3':
            self.textStory = '''
This evasive action will require 1500lb of MMH and 2300lb of N204.
Press the seven fuel buttons on the panel that will divert exactly these
ammounts to the shuttle's orbital manuevering unit.
Finally, press the correct firing button to start the sequence.
You have 60 seconds.
Use the mouse to select.
'''
        if self.part == '4':
            self.textStory = '''
Follow the plans on the NASA-FAX, spot the eight components that make up the makeshift oxygen pump.
The life support system will only last a little longer.
You have just one minute to select the correct parts.
Use the mouse to select.
'''
        if self.part == '5':
            self.textStory = '''
Sure enough, the ESA has offered fuel. Discovery has to rendezvous with the ESA fuel module.
The shuttle's computer is playing up so the crew has to rely largely on its reserves of
knowledge and skill in order to achieve this.
Answer the following 10 questions. A correct answer moves you to the next question.
You can't afford to make more than three mistakes.
Use the mouse to select.
'''
        if self.part == '6':
            self.textStory = '''
The shuttle has to lift itself out of the dangerously low orbit using its critical
firing of her motors. You will have 40 seconds to follow the route to a safe orbit,
avoiding any of the chemicals commonly found in Earth's atmosphere.

Elements and compounds found in the Earth's atmosphere:
O O2 N SO2 CO PbO H
Elements not found in the Earth's atmosphere:
Al Pb Ag Au Pl Me Zn

Move with the arrow keys
'''
        if self.part == '7':
            self.textStory = '''
Study the selection of controls and parts. Select the seven that are vital in helping
Pilot Igor Minsky fly the Soviet shuttle and to ensure a successful launch
from Baikonur base. You have 3 attempts.

Use the mouse to select.
'''
        if self.part == '8':
            self.textStory = '''
Help Cosmonaut Manarov connect a line to Discovery by tracking his route from Tereshkova,
over the hurricane maze, avoiding the clouds.
Do it in 35 seconds.
Move with the arrow keys.
'''
        if self.part == '9':
            self.textStory = '''
Tereshkova has successfully re-entered the Earth's atmosphere and, following a 180-mile glide,
is just about to land on the concrete runway of Tyuratam. Suddenly, a strong gust of
wind catches Pilot Igor Minsky out. Tereshkova comes close to clipping the snowy
ground alongside the runway.
Track along the runway correctly anticipating the gusts to guide the Soviet shuttle in.
You have 30 seconds.
Move with the arrow keys.
'''
        if self.part == '10':
            self.textStory = '''
Brad is preparing for his spacewalk. Getting into his suit is a difficult and
time-consuming business. Answer the following questions with the mouse.
A correct answer moves you to the next question.
You have 2 attempts at mistakes.
Use the mouse to select.
'''
        if self.part == '11':
            self.textStory = '''
Help Brad collect the spanners he needs to carry out the repairs.
Track along the route, via the spanners, as quickly as you can.
Remember: air supply is limited. You have 30 seconds to reach the other side
and collect all the spanners
Move with the arrow keys.
'''
        if self.part == '12':
            self.textStory = '''
Brad has almost completed his repairs, He has now to operate some valves
manually to allow the remainder of the fuel to be available to the motors.
Select which eight valves can be operated using the spanners collected by Brad.
Use the mouse to select the spanner and its matching valve.
You have 3 attempts at mistakes.
'''
        if self.part == '13':
            self.textStory = '''
Now that is done, go back to the flight deck.
You have 35 seconds to reach the other side.
Move with the arrow keys.
'''
        if self.part == '14':
            self.textStory = '''
Discovery starts her descent. Brad Singleton is concentrating perhaps more
than he has ever concentrated before.
Help him through this ordeal by answering the following questions within
30 seconds.
Use the mouse to select.
'''
        if self.part == '15':
            self.textStory = '''
So far so good. But it's not over yet. Brad still has to get Discovery safely down to land-
and the storm's getting worse! Answer the following questions, If you make more than
two mistakes Discovery will be lost (Remember, there are no ejector seats in this shuttle.)
Use the mouse to select.
'''
        if self.part == '16':
            self.textStory = '''
Against all the odds, the shuttle landed safely. A jubilant but weary Brad Singleton came home to a hero's
welcome.
To commemorate the courageous, joint Russian - American effort, President McKenner and Premier Yeltsinov
each ordered that a medal be made. It was only later, long after the cheering and applause had faded,
that the world heard the full story of the Soviet's surprise rescue bid.
Just like Discovery, the Russian ship was at the end of her service life, and was to be decomissioned.
Without being one hundred percent ready for her last mission, the crew had volunteered to try and save
the Americans.
Now, the two veteran shuttles, Discovery and Tereshkova, stand side-by-side in the International
Space Museum at Cape Canaveral,a proud tribute to a remarkable space rescue.
'''               
            
    def isActive(self):
        return self.active
    def activate(self):
        self.active = True
    def deactivate(self):
        self.active = False
    def drawPart(self):
        self.active = True            
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))        
        if self.isActive():
            x,y= pygame.mouse.get_pos()
            textPos = self.nextTxt.get_pos()
            if x > textPos.left and x < textPos.right and y > textPos.top and y < textPos.bottom:
                f_source = self.nextTxt.render(self.nextTxt.get_text(),True,(0,0,0))
                self.background.blit(f_source,self.nextTxt.get_pos())

                f_source = self.nextTxt.render(self.nextTxt.get_text(),True,(117, 152, 231))
                self.background.blit(f_source,self.nextTxt.get_pos())
            else:
                f_source = self.nextTxt.render(self.nextTxt.get_text(),True,(0, 0, 0))
                self.background.blit(f_source,self.nextTxt.get_pos())
            
            pygame.draw.rect(screen,(255,25,25),(self.background.get_width()-200,self.centerY-5,100,30),2) #950 660                
                
    def handleEvent(self,event):
        if event.type == MOUSEBUTTONDOWN and self.isActive():            
            # get x and y of the current event 
            eventX = event.pos[0]
            eventY = event.pos[1]

            textPos = self.nextTxt.get_pos()
            if eventX > textPos.left and eventX < textPos.right and eventY > textPos.top and eventY < textPos.bottom:
                menuEvent = pygame.event.Event(self.MENUCLICKEDEVENT, item=0, text=self.nextTxt.get_text())
                pygame.event.post(menuEvent)           
        

class PartStory:
    MENUCLICKEDEVENT = USEREVENT + 1
    def __init__(self,part):
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        #self.background = pygame.Surface(screen.get_size())
        self.background = pygame.image.load(os.path.join(getCurrentFolder(),"img","intro.jpg"))
        self.background = self.background.convert()
        #self.background.fill((0, 0, 0))
        self.active = False
        self.part = part

        self.textStory = ""

        self.setText()

        self.textNext = "NEXT"
        
        if pygame.font:
            fontSize = 25
            fontSpace = 2
            mybigfont = pygame.font.SysFont('MS Comic Sans',25)
            
            centerY = fontSize/2
            y = fontSize
            x = fontSize*2
            for line in self.textStory.split("\n"):                
                #nCenterX = ((len(line))*((fontSize/5)))-5
                #newEnty = MenuItem(line, (0, 0),fontSize=fontSize)                
                #self.background.blit(newEnty.get_surface(), (nCenterX,centerY))#newEnty.get_pos())
                centerY+=fontSize+fontSpace
                                
                label = mybigfont.render(line,1,(255,255,255))
                self.background.blit(label,(x,y))
                #self.mLayer.blit(label,(250,500))
                y+=fontSize+fontSpace
                
            centerX = self.background.get_width()-50
            self.nextTxt = MenuItem(self.textNext,(centerX,centerY+10),fontSize=fontSize)
            self.background.blit(self.nextTxt.get_surface(), self.nextTxt.get_pos())

            self.centerY = centerY

    def setText(self):
        if self.part == '1':
            self.textStory = '''
Shuttle Commander Bradley Singleton was on the flight deck of Discovery, writing up the day's log,
when the call from Mission Control came through: "We have an assignment for you.
Can you drop some supplies off at the lunar mine at Rook Mountain?" "Yeah, no sweat ..."
Brad affirmed;after all, Moon missions in the space shuttle were, by now, no more than routine."
"One other thing, Brad," Control added, "When you get back to base, dock the old ship at engineering.
She's due for decomission. This will be her last mission ..."
Commander Brad Singleton had been expecting the news sooner or later, 
but now that it had come he felt stunned.
Discovery was one of the oldest shuttles in the US fleet. Back in the 1990s, she had worked hard,
carrying parts from Earth to space to build the first space stations. For the last few years,
though, she had stayed in space, based on US station Freedom. Her duties included servcing and
retrieving satellites, and, from time to time, delivering supplies to the Moon.
Now, in the year 2002, this pioneer shuttle was to be taken out of service to become a spare-parts
store for younger shuttles. Scrap metal. It seemed a sad end. But Brad Singleton had a job to do.
He called his crew to a prelaunch briefing. "The lunar mine at Rook Mountain is short of supplies.
There are also a couple of mining engineers to be dropped off. Jeanne, you will pilot the shuttle,
and you, Chuck, will be in charge of the lunar transfer vehicle as usual. Now, we all know the
routine. Let's go!" 
It was a smooth take-off from the space station, followed by a perfect entry into Moon orbit.
Nothing much happened in between although from time to time on the journey out the shuttle's
radar picked up the steady traffic of mineral containers that were regularly launched into Earth
orbit from the Moon. Once the LTV (lunar transfer vehicle) has made a successful landing,
Brad Singleton jettisoned the shuttle's now empty main tank, ready to return to Earth orbit and Freedom ...'''
        if self.part == '2':
            self.textStory = '''On the moon, Discovery's two engineering specialists, Leif Dexter
and Saladin Lasker, wasted no time in reporting to the mining complex at Rook Mountain.
It was Leif's firstassignment. "This area was just dust and craters only a few years back,"
commented Saladin, who knew the mines like the back of his hand, "It now produces a third of
all the minerals and oxygen we need up in space at present."
"See that production line? It's almost fully automated, you know. Only needs a couple of guys
to keep an eye on it."
As Saladin spoke, a giant digger full of excavated moonrock tipped its load. Busy robot arms set
to work sorting it. "Once that's processed," said Saladin, "the minerals will be packed in
containers and launched into space. Come on, I'll show you"
The two men took a lunar rover and watched as containers were loaded one at a time into the mass-driver,
a huge machine that used powerful magnetic fields to accelerate objects along a tube at very high speeds
for launch into Earth orbit.
"Hey, watch it!" an urgent voice shouted. "That pod's damaged." The warning was too late. Before the
engineer on duty could move, a faulty metal container was whisked into the machine. Seconds later,
to everyone's horror, it was seen to break up as it left the muzzle of the mass-driver, shattering
in pieces and spraying metal debris into space like pellets from a shotgun.
"Oh no!" yelled Leif, "Discovery's up there in orbit. We must warn Brad!"
But, up in the shuttle, Brad and his crew needed no warning. The flight-deck instrument panel told it all.
Brad had avoided the largest lumps of metal hurling towards his ship.
Pilot Jeanne Allison stayed calm. Having alerted Lunar Command and Station Controller on Freedom,
she was about to call Mission Control back on Earth when quite suddenly, she cried
"Commander. Look! On the radar. Those smaller metal fragments. They're going to hit us!"
'''
        if self.part == '4':
            self.textStory = '''
By a miracle, the shuttle had survived the bombardment. But at what cost? Brad Singleton ordered a
system check. The news was grim. Several small fragments had hit Discovery, damaging the life-support
system, possibly loosening tiles on the ship's top side and jamming some of the nozzles on the orbital
manuevering gear. Worst of all, though, a lump of metal debris had struck the shuttle's underside,
ripping open the remaining external fuel tank.
Looking out of the windows, Brad could see an expanding cloud of gas around the shuttle, confirming what
the computers told them. There had been a catastrophic fuel loss. Discovery's plight was being monitored
by stations throughout Earth and space.
A short time later, Mission Control made matters worse. "Sorry. More bad news. We can't launch a rescue
shuttle to you from Cape Canaveral. We have a hurricane down here."
"That's all I need," groaned Brad, "Anything at Vandenberg?"
"Nothing. And nothing in orbit that can get to you either," Control added."Thanks," Brad muttered curtly.
"Ello, Discovery. ESA speaking," It was the European Space Agency, "We think we can help.
An experimental fuel rocket has just been launched from Kourou, French Guiana. It's in the right orbit."
Brad looked at Jeanne, eyebrows raised. "We could ..." Suddenly, the voice of Mission Control cut in:
"Brad. This is urgent. Our computer's telling us you must fix your oxygen pump right away. Otherwise,
the life-support system will burn out. Rig up a replacement with parts from a back-pack. We are sending a plan ..."
'''
        if self.part == '5':
            self.textStory = '''
The shuttle crew had averted one disaster, only to find themselves faced with another that was
even worse. Discovery was now hurtling helplessly towards Earth and imminent burn up in the atmosphere ...
"What was ESA about to say?" one of the Mission Specialists, Victor Lee, asked.
"No idea," Jeanne answered. Then, a momemtn later :"Yes I have! The Europeans are experimenting with
a universal payload module, the UPM(F). I bet they were going to offer to send fuel. Quick, call them ..."
'''
        if self.part == '6':
            self.textStory = '''
With the European fuel module connected in the shuttle's cargo hold, Discovery was able to fire her main motors.
This lifted her out of immediate danger and into a low polar orbit.
Discovery's four crew members snatched time to review their situation.
"Here's how we stans," said the commander quietly. "Our orbit's decaying badly; gives us about three hours, Jeanne?"
Jeanne looked anxiously at her watch. "As you know, Brad, we've sustained some motor damage so steering's a problem.
This, together with our orbit, means we can't get back to Freedom. Also, we probably have some loose tiles.
If any are damaged, we risk burn up on re-entry should we try to return to Earth."
There was a moment's pause: "But thanks to ESA, we have fuel. Some went on that first 'burn' and most of the
remainder will be used up in a main 'burn', which we have to do to position ourselves in a higher, safer orbit. After that ... "
"Can't ESA send more fuel?" interrupted Bill Gibson, the second Mission Specialist.
"No," Brad replied, "That was their only UPM."
"What about the Soviets on Cosmograd?" suggested Vic.
"No chance. The Russian space station is in equitorial orbit, same as Freedom. No way can either of them reach us in
a polar orbit, " Jeanne explained grimly. The crew were silent. Everyone understood the position; It was not healthy.
Eventually, Brad spoke again, "Come on, you guys. Let's have a shot at lifting her into a better orbit.
We now have under three hours ..."
'''
        if self.part == '7':
            self.textStory = '''
While the life and death drama was being played out in space, back on Earth frantic efforts were being made at the
very highest levels to find a way to rescue the stranded astronauts.
At Russian Space Command, the Supreme Space Committee was in emergency session, discussing a daring plan.
Colonel Yuri Sopofsky put down the phone: "Premier Yeltsinov has given the go-ahead."
Seconds later, in the White House, the red phone rang. President McKenner listened intently, a grave
expression on his face. He briefed his advisers: "The Soviets have a suggestion. It's a real surprise,
but they've offered to put up one of their shuttles to the off our crew."
"What about Discovery?" one expert asked.
"They'll pack her with explosives. She'll be blown to bits when she eventually enters the atmosphere,"
answered the President, "Can't have a piece of metal that big landing where it pleases."
The advisers objected: "We don't like it Mr. President. We ... " 
"We have no choice," came the curt reply. "Go for it!"
Moments later, in the tense atmosphere of Discovery's flight deck, the four astronauts learned
of the Russian suggestion from Mission Control. Risky as the rescue attempt would be, the crew knew it had to be tried.
If it failed, they knew full well they would not come out alive.
'''
        if self.part == '8':
            self.textStory = '''
It was some time before Discovery's radar picked up the Soviet shuttle powering swiftly towards her.
"Looks like we'll intercept over Florida," shouted a joyful Bill Gibson.
He was dead right. As the two space shuttles approached one another, frantic activity could be seen on
the Russian craft. Brad could clearly make out the name on the fuselage: Tereshkova.
A hatch opened to reveal Soviet cosmonaut Vladimir Manarov preparing to spacewalk.
"He's going to attach a line to us!" cried Vic.
'''
        if self.part == '9':
            self.textStory = '''
Manarov carried out the transfer operation with all the precision and skill his years of training had given him.
Within minutes, all but one of the American crew were safely across to Tereshkova,
Then it was Brad Singleton's turn. As he was on the point of leaving his ship, he was seen to turn and go back
inside.
"Mission Control, do you hear me? I have a plan. It might just work, " Brad's voice was calm but firm. "Get
me the President!"
President McKenner heard Brad through, "It sounds dangerous, but you have my blessing, " he said, and added:
"Good luck, Brad; I think you'll need it."
Meanwhile, from the cabin of the Russian shuttle, the American crew could just see their commander moving
about on Discovery.
"Brad must feel choked up abandoning her," said Vic. "He's been with the old ship for the best part of five years.
He's grown quite attached to her."
"Even so, I wish he'd hurry over," said Jeanne, glancing at the Russian demolition explosives.
"The sooner we get away the better!"
Suddenly, Bill called out, "Hey! Discovery's hatch is closing. What's going on?"
At that moment, Vladimir Manarov entered Tereshkova's cramped cabin. "I will tell you," he explained. "I have been
listening to your brave commander. Rather than risk overloading this ship, he's decided to stay with the Discovery
and is going to try to fly her back to Earth single-handed!"
"However," he added, "we too must return to Earth. Please prepare yourselves." The explosives were jettisoned and
everyone settled into their couches.
As the Soviet crew started re-entry procedures, Jeanne could not help noticing Vladimir had his fingers crossed ...
'''
        if self.part == '10':
            self.textStory = '''
Alone on his ship, Brad had to put his plan into action. He reckoned that, although there was only a slim chance
of success, he would have to repair the damaged motors. This would enable him to maneuver Discovery into the
correct position for re-entry.
But first he had to divery the rest of the fuel to the motors.
While he was thinking, a message came through from Soviet base. Tereshkova had landed at Tyuratam.
Brad had heard good news at least! The flight and landing had been rough, but both crews were now down and the
Americans were already preparing for transfer to a States-bound airline.
Knowing his crew were safely back on Earth, Brad could concentrate fully on his own rescue attempt. He knew that,
in order to restore the fuel flow, he would have to open some jammed valves by hand. And that, he realized, would
mean a spacewalk.
First, though, the commander set to work to drain the last drop from European fuel module, before ejecting it
through the open bay doors. All the fuel was now in the shuttle's internal tanks.
With only six hours to go before Discovery would start to skim the Earth's upper atmosphere and "heat-up",
Brad struggled into his spacesuit ready for his walk in space ...
'''
        if self.part == '11':
            self.textStory = '''
Brad is out of the airlock and into the vacuum of space! Ahead of him: a spacewalk during which he must repair the
shuttle's fuel system and motors.
Unfortunately, some tools have been scattered by the accident. Luckily they are magnetic and have remained in the bay.
'''
        if self.part == '12':
            self.textStory = '''
Just as the commander was finishing a particularly tricky repair to fuel pipe, there was a buzz on his transceiver and
a familiar voice called: "Hi, Brad, how are you doing?" It was the commander's wife. "Marry Ann! It's great to hear you,"
cried Brad. "I'm doing fine." Then he explained, "I've fixed all I can on the old ship, but it'll be a rough ride home.
Anyway, how about you?"
"I've just artived at Mission Control." answered Mary Ann. "Jeanne Allison and the crew are here, too. We are all with you,
Brad. You'll be okay, " sheadded quietly.
"Sure. As long as the tiles do their job during re-entry, we'll make it." Brad said, and went on: "I keep thinking of that
time back in 1992 when my fighter went into a spin over the Med. Pulled up with inches to spare," he said, "Do you remember?
I got out of that one all right, and it was much worse than this!"
At that moment, the transmission stopped. Brad shrugged and started the lone spacewalk back to the flight deck and a final
systems check.
'''

        if self.part == '14':
            self.textStory = '''
Fortunately, the on-board computer screen showed the fuel system to be working properly and the motors seem to be okay.
Now, with only seconds to go to re-entry, Bradley fired the retro rockets, rapidly using up most of the fuel.
This braked the shuttle, tilting her into the right position for re-entry.
Almost immediately, as Discovery hit the upper atmosphere, a faint pink glow surrounded the craft, quickly turning to a
fierce orangey-red. Shuttle started to shake violently. Brad hoped the tiles would cope.
Vladimir Manarov, monitoring the re-entry from Baikonur, crossed his fingers once again ..
'''
        if self.part == '15':
            self.textStory = '''
Discovery had survived the fiery return from space into the atmosphere, and was on course for a landing at Edwards Air Force
Base, when, yet again, there was a signal from Mission Control. "Oh no, what now?" groaned the commander.
"Weather over the Californian coast is not good, Brad," reported Control, "There's heavy cloud build up, and something we didn't
anticipate - a freak electrical storm over Edwards. Visibility is low. NASA is sending up an all-weather A-7 to guide you in."
"Right," radioed Brad. "The plane will be white, I take it?" I should pick that out."
The shuttle hit turbulence 52,00 feet up over Silver Lake. Just as she was nearing the rendezvous, she encountered the full force
of the storm. Singleton wrestled to keep the huge spaceship under control. Then, through the starboard window, he spotted the A-7,
shining white like some sort of guardian angel. At least, he thought, the nightmare journey was near its end.
Suddenly, there was a tremendous blue-white flash. Lightning had struck the A-7.
Once again, Brad struggled with the controls as the plane, its pilot safely ejected, banked directly into the shuttle's flight path.
Surely, after all that had happened in space, on the Moon, on re-entry, Brad Singleton's brave rescue mission was not going to fail
so close to home ...
'''
         

    def isActive(self):
        return self.active
    def activate(self):
        self.active = True
    def deactivate(self):
        self.active = False
        
    def drawPart(self):
        self.active = True            
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))        
        if self.isActive():
            x,y= pygame.mouse.get_pos()
            textPos = self.nextTxt.get_pos()
            if x > textPos.left and x < textPos.right and y > textPos.top and y < textPos.bottom:
                f_source = self.nextTxt.render(self.nextTxt.get_text(),True,(0,0,0))
                self.background.blit(f_source,self.nextTxt.get_pos())

                f_source = self.nextTxt.render(self.nextTxt.get_text(),True,(117, 152, 231))
                self.background.blit(f_source,self.nextTxt.get_pos())
            else:
                f_source = self.nextTxt.render(self.nextTxt.get_text(),True,(255, 255, 255))
                self.background.blit(f_source,self.nextTxt.get_pos())
            
            pygame.draw.rect(screen,(255,25,25),(self.background.get_width()-100,self.centerY-5,100,30),2) #950 660
                
                
    def handleEvent(self,event):
        if event.type == MOUSEBUTTONDOWN and self.isActive():            
            # get x and y of the current event 
            eventX = event.pos[0]
            eventY = event.pos[1]

            textPos = self.nextTxt.get_pos()
            if eventX > textPos.left and eventX < textPos.right and eventY > textPos.top and eventY < textPos.bottom:
                menuEvent = pygame.event.Event(self.MENUCLICKEDEVENT, item=0, text=self.nextTxt.get_text())
                pygame.event.post(menuEvent)            
        
def main():
    # pygame initialization
    width = 1100
    height = 1000

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Shuttle Mission: Retrival')
    pygame.mouse.set_visible(1)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    clock = pygame.time.Clock()    
    
    
    # draw background
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    # code for our menu 
    ourMenu = ["Start New Game",
               "Select Stage",               
               "Quit"]
    levelStart = None

    while levelStart == None:    
        myMenu = Menu(ourMenu)
        myMenu.drawMenu()
        # pygame.display.flip()
        # main loop for event handling and drawing
        
        while myMenu.isActive():
            clock.tick(60)

            # Handle Input Events
            for event in pygame.event.get():            
                myMenu.handleEvent(event)
                # quit the game if escape is pressed
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Quit") > -1:
                        return
                    elif event.text.find("Start New Game") > -1:                    
                        myMenu.deactivate()
                        levelStart = 1
                    elif event.text.find("Select Stage") > -1:
                        myMenu.deactivate()
            screen.blit(background, (0, 0))    
            if myMenu.isActive():
                myMenu.drawMenu()
            else:
                background.fill((10, 10, 10))
            pygame.display.flip()

        if levelStart == None:        
            levelsMenu = []
            for i in range(1,16):
                levelsMenu.append('Stage '+str(i))
            levelsMenu.append('Back')
            levelMenu = Menu(levelsMenu)
            levelMenu.drawMenu()
            destination = None
            while levelMenu.isActive():
                clock.tick(60)
                for event in pygame.event.get():
                    levelMenu.handleEvent(event)
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                    elif event.type == Menu.MENUCLICKEDEVENT:                    
                        for i in levelsMenu:
                            if event.text.find(i) > -1:                            
                                destination = i
                                levelMenu.deactivate()
                screen.blit(background,(0,0))
                if levelMenu.isActive():
                    levelMenu.drawMenu()
                else:
                    background.fill((10,10,10))
                pygame.display.flip()
            
            if destination != 'Back':
                levelStart = int(destination.split(' ')[1])
                                
    while levelStart == 1:
        part1 = PartStory('1')
        part1.drawPart()

        while part1.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                part1.handleEvent(event)            
                if event.type == QUIT:
                    return              
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("NEXT") > -1:
                        part1.deactivate() 
            screen.blit(background,(0,0))
            if part1.isActive():
                part1.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()        

        introGame1 = IntroGame('1')
        introGame1.drawPart()
        while introGame1.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                introGame1.handleEvent(event)
                if event.type == QUIT:
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Start") > -1:
                        introGame1.deactivate()
            screen.blit(background,(0,0))
            if introGame1.isActive():
                introGame1.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        game1 = Game1()
        game1.drawPart()
        gameRunning = 1
        while gameRunning < 100 : 
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == pygame.K_UP:
                        game1.moveUp()
                    elif event.key == pygame.K_DOWN:
                        game1.moveDown()
                    elif event.key == pygame.K_LEFT:
                        game1.moveLeft()
                    elif event.key == pygame.K_RIGHT:
                        game1.moveRight()
            game1.update()        
            game1.draw()
            pygame.display.flip()
            if game1.isSuccess() or (game1.isActive() == False and game1.isSuccess() == False):
                gameRunning+=1
        if game1.isSuccess():
            levelStart+=1
        else:
            retryMenuOptions = ['Retry','Quit']
            retryMenu = Menu(retryMenuOptions)
            retryMenu.drawMenu()
            while retryMenu.isActive():
                clock.tick(60)
                for event in pygame.event.get():
                    retryMenu.handleEvent(event)
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                    elif event.type == Menu.MENUCLICKEDEVENT:
                        if event.text.find('Retry') > -1:
                            retryMenu.deactivate()
                        elif event.text.find('Quit') > -1:
                            return
                screen.blit(background,(0,0))
                if retryMenu.isActive():
                    retryMenu.drawMenu()
                else:
                    background.fill((10,10,10))
                pygame.display.flip()

    while levelStart == 2:
        part2 = PartStory('2')
        part2.drawPart()

        while part2.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                part2.handleEvent(event)            
                if event.type == QUIT:
                    return                
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("NEXT") > -1:
                        part2.deactivate() 
            screen.blit(background,(0,0))
            if part2.isActive():
                part2.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        introGame2 = IntroGame('2')
        introGame2.drawPart()
        while introGame2.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                introGame2.handleEvent(event)
                if event.type == QUIT:
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Start") > -1:
                        introGameTwo.deactivate()
            screen.blit(introGame2,(0,0))
            if introGame2.isActive():
                introGame2.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        game2 = Game2()
        game2.drawPart()
        gameRunning = 1
        while gameRunning < 100:
            clock.tick(60)
            for event in pygame.event.get():
                game2.handleEvent(event)
                if event.type == QUIT:
                    return              
            game2.draw()
            pygame.display.flip()
            if game2.isSuccess() or (game2.isActive() == False and game2.isSuccess() == False):
                gameRunning+=1
        if game2.isSuccess():
            levelStart+=1
        else:
            retryMenuOptions = ['Retry','Quit']
            retryMenu = Menu(retryMenuOptions)
            retryMenu.drawMenu()
            while retryMenu.isActive():
                clock.tick(60)
                for event in pygame.event.get():
                    retryMenu.handleEvent(event)
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                    elif event.type == Menu.MENUCLICKEDEVENT:
                        if event.text.find('Retry') > -1:
                            retryMenu.deactivate()
                        elif event.text.find('Quit') > -1:
                            return
                screen.blit(background,(0,0))
                if retryMenu.isActive():
                    retryMenu.drawMenu()
                else:
                    background.fill((10,10,10))
                pygame.display.flip()            
            
    while levelStart == 3:
        introGame3 = IntroGame('3')
        introGame3.drawPart()
        while introGame3.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                introGame3.handleEvent(event)
                if event.type == QUIT:
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Start") > -1:
                        introGame3.deactivate()
            screen.blit(background,(0,0))
            if introGame3.isActive():
                introGame3.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()
        
        game3 = Game3()
        game3.drawPart()
        gameRunning = 1
        while gameRunning < 100:
            clock.tick(60)
            for event in pygame.event.get():
                game3.handleEvent(event)
                if event.type == QUIT:
                    return
            game3.draw()
            pygame.display.flip()
            if game3.isSuccess() or (game3.isActive() == False and game3.isSuccess() == False):
                gameRunning+=1
        if game3.isSuccess():
            levelStart+=1
        else:
            retryMenuOptions = ['Retry','Quit']
            retryMenu = Menu(retryMenuOptions)
            retryMenu.drawMenu()
            while retryMenu.isActive():
                clock.tick(60)
                for event in pygame.event.get():
                    retryMenu.handleEvent(event)
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                    elif event.type == Menu.MENUCLICKEDEVENT:
                        if event.text.find('Retry') > -1:                            
                            retryMenu.deactivate()
                        elif event.text.find('Quit') > -1:
                            return
                screen.blit(background,(0,0))
                if retryMenu.isActive():
                    retryMenu.drawMenu()
                else:
                    background.fill((10,10,10))
                pygame.display.flip()

    while levelStart == 4:
        part4 = PartStory('4')
        part4.drawPart()

        while part4.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                part4.handleEvent(event)            
                if event.type == QUIT:
                    return                
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("NEXT") > -1:
                        part4.deactivate() 
            screen.blit(background,(0,0))
            if part4.isActive():
                part4.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()    

        introGame4 = IntroGame('4')
        introGame4.drawPart()
        while introGame4.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                introGame4.handleEvent(event)
                if event.type == QUIT:
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Start") > -1:
                        introGame4.deactivate()
            screen.blit(background,(0,0))
            if introGame4.isActive():
                introGame4.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()    
        game4 = Game4()
        game4.drawPart()
        gameRunning = 1
        while gameRunning < 100:
            clock.tick(60)
            for event in pygame.event.get():
                game4.handleEvent(event)
                if event.type == QUIT:
                    return
            game4.draw()
            pygame.display.flip()
            if game4.isSuccess() or (game4.isActive() == False and game4.isSuccess() == False):
                gameRunning+=1
        if game4.isSuccess():
            levelStart+=1
        else:
            retryMenuOptions = ['Retry','Quit']
            retryMenu = Menu(retryMenuOptions)
            retryMenu.drawMenu()
            while retryMenu.isActive():
                clock.tick(60)
                for event in pygame.event.get():
                    retryMenu.handleEvent(event)
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                    elif event.type == Menu.MENUCLICKEDEVENT:
                        if event.text.find('Retry') > -1:                            
                            retryMenu.deactivate()
                        elif event.text.find('Quit') > -1:
                            return
                screen.blit(background,(0,0))
                if retryMenu.isActive():
                    retryMenu.drawMenu()
                else:
                    background.fill((10,10,10))
                pygame.display.flip()
                
    while levelStart == 5:
        part5 = PartStory('5')
        part5.drawPart()

        while part5.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                part5.handleEvent(event)            
                if event.type == QUIT:
                    return                
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("NEXT") > -1:                    
                        part5.deactivate() 
            screen.blit(background,(0,0))
            if part5.isActive():
                part5.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()    

        introGame5 = IntroGame('5')
        introGame5.drawPart()
        while introGame5.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                introGame5.handleEvent(event)
                if event.type == QUIT:
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Start") > -1:
                        introGame5.deactivate()
            screen.blit(background,(0,0))
            if introGame5.isActive():
                introGame5.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()
            
        game5 = Game5()
        game5.drawPart()
        gameRunning = 1
        while gameRunning < 100:
            clock.tick(60)
            for event in pygame.event.get():
                game5.handleEvent(event)
                if event.type == QUIT:
                    return
            game5.draw()
            pygame.display.flip()    
            if game5.isSuccess() or (game5.isActive() == False and game5.isSuccess() == False):
                gameRunning+=1
        if game5.isSuccess():
            levelStart+=1
        else:
            retryMenuOptions = ['Retry','Quit']
            retryMenu = Menu(retryMenuOptions)
            retryMenu.drawMenu()
            while retryMenu.isActive():
                clock.tick(60)
                for event in pygame.event.get():
                    retryMenu.handleEvent(event)
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                    elif event.type == Menu.MENUCLICKEDEVENT:
                        if event.text.find('Retry') > -1:                            
                            retryMenu.deactivate()
                        elif event.text.find('Quit') > -1:
                            return
                screen.blit(background,(0,0))
                if retryMenu.isActive():
                    retryMenu.drawMenu()
                else:
                    background.fill((10,10,10))
                pygame.display.flip()

    while levelStart == 6:
        part6 = PartStory('6')
        part6.drawPart()

        while part6.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                part6.handleEvent(event)            
                if event.type == QUIT:
                    return                
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("NEXT") > -1:                    
                        part6.deactivate() 
            screen.blit(background,(0,0))
            if part6.isActive():
                part6.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()    

        introGame6 = IntroGame('6')
        introGame6.drawPart()
        while introGame6.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                introGame6.handleEvent(event)
                if event.type == QUIT:
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Start") > -1:
                        introGame6.deactivate()
            screen.blit(background,(0,0))
            if introGame6.isActive():
                introGame6.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()
            
        game6 = Game6()
        game6.drawPart()
        gameRunning = 1
        while gameRunning < 100:
            clock.tick(60)
            for event in pygame.event.get():
                game6.handleEvent(event)
                if event.type == QUIT:
                    return        
            game6.draw()
            pygame.display.flip()
            if game6.isSuccess() or (game6.isActive() == False and game6.isSuccess() == False):
                gameRunning+=1
        if game6.isSuccess():
            levelStart+=1
        else:
            retryMenuOptions = ['Retry','Quit']
            retryMenu = Menu(retryMenuOptions)
            retryMenu.drawMenu()
            while retryMenu.isActive():
                clock.tick(60)
                for event in pygame.event.get():
                    retryMenu.handleEvent(event)
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                    elif event.type == Menu.MENUCLICKEDEVENT:
                        if event.text.find('Retry') > -1:                            
                            retryMenu.deactivate()
                        elif event.text.find('Quit') > -1:
                            return
                screen.blit(background,(0,0))
                if retryMenu.isActive():
                    retryMenu.drawMenu()
                else:
                    background.fill((10,10,10))
                pygame.display.flip()

    while levelStart == 7:
        part7 = PartStory('7')
        part7.drawPart()

        while part7.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                part7.handleEvent(event)            
                if event.type == QUIT:
                    return                
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("NEXT") > -1:                    
                        part7.deactivate() 
            screen.blit(background,(0,0))
            if part7.isActive():
                part7.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()    

        introGame7 = IntroGame('7')
        introGame7.drawPart()
        while introGame7.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                introGame7.handleEvent(event)
                if event.type == QUIT:
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Start") > -1:
                        introGame7.deactivate()
            screen.blit(background,(0,0))
            if introGame7.isActive():
                introGame7.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        game7 = Game7()
        game7.drawPart()
        gameRunning = 1
        while gameRunning < 100:
            clock.tick(60)
            for event in pygame.event.get():
                game7.handleEvent(event)
                if event.type == QUIT:
                    return        
            game7.draw()
            pygame.display.flip()
            if game7.isSuccess() or (game7.isActive() == False and game7.isSuccess() == False):
                gameRunning+=1
        if game7.isSuccess():
            levelStart+=1
        else:
            retryMenuOptions = ['Retry','Quit']
            retryMenu = Menu(retryMenuOptions)
            retryMenu.drawMenu()
            while retryMenu.isActive():
                clock.tick(60)
                for event in pygame.event.get():
                    retryMenu.handleEvent(event)
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                    elif event.type == Menu.MENUCLICKEDEVENT:
                        if event.text.find('Retry') > -1:
                            retryMenu.deactivate()
                        elif event.text.find('Quit') > -1:
                            return
                screen.blit(background,(0,0))
                if retryMenu.isActive():
                    retryMenu.drawMenu()
                else:
                    background.fill((10,10,10))
                pygame.display.flip()
                
    while levelStart == 8:
        part8 = PartStory('8')
        part8.drawPart()

        while part8.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                part8.handleEvent(event)            
                if event.type == QUIT:
                    return                
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("NEXT") > -1:                    
                        part8.deactivate() 
            screen.blit(background,(0,0))
            if part8.isActive():
                part8.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        introGame8 = IntroGame('8')
        introGame8.drawPart()
        while introGameEight.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                introGame8.handleEvent(event)
                if event.type == QUIT:
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Start") > -1:
                        introGame8.deactivate()
            screen.blit(background,(0,0))
            if introGame8.isActive():
                introGame8.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()        
        

        game8 = Game8()
        game8.drawPart()
        gameRunning  = 1
        while gameRunning < 100:
            clock.tick(60)
            for event in pygame.event.get():
                game8.handleEvent(event)
                if event.type == QUIT:
                    return
            game8.update()
            game8.draw()
            pygame.display.flip()
            if game8.isSuccess() or (game8.isActive() == False and game8.isSuccess() == False):
                gameRunning+=1
        if game8.isSuccess():
            levelStart+=1
        else:
            retryMenuOptions = ['Retry','Quit']
            retryMenu = Menu(retryMenuOptions)
            retryMenu.drawMenu()
            while retryMenu.isActive():
                clock.tick(60)
                for event in pygame.event.get():
                    retryMenu.handleEvent(event)
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                    elif event.type == Menu.MENUCLICKEDEVENT:
                        if event.text.find('Retry') > -1:
                            retryMenu.deactivate()
                        elif event.text.find('Quit') > -1:
                            return
                screen.blit(background,(0,0))
                if retryMenu.isActive():
                    retryMenu.drawMenu()
                else:
                    background.fill((10,10,10))
                pygame.display.flip()
                
    while levelStart == 9:
        part9 = PartStory('9')
        part9.drawPart()

        while part9.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                part9.handleEvent(event)            
                if event.type == QUIT:
                    return                
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("NEXT") > -1:                    
                        part9.deactivate() 
            screen.blit(background,(0,0))
            if part9.isActive():
                part9.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        introGame9 = IntroGame('9')
        introGame9.drawPart()
        while introGame9.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                introGame9.handleEvent(event)
                if event.type == QUIT:
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Start") > -1:
                        introGame9.deactivate()
            screen.blit(background,(0,0))
            if introGame9.isActive():
                introGame9.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        game9 = Game9()
        game9.drawPart()
        gameRunning = 1
        while gameRunning < 100:
            clock.tick(60)
            for event in pygame.event.get():
                game9.handleEvent(event)
                if event.type == QUIT:
                    return
            game9.update()
            game9.draw()
            pygame.display.flip()
            if game9.isSuccess() or (game9.isActive() == False and game9.isSuccess() == False):
                gameRunning+=1
        if game9.isSuccess():
            levelStart+=1
        else:
            retryMenuOptions = ['Retry','Quit']
            retryMenu = Menu(retryMenuOptions)
            retryMenu.drawMenu()
            while retryMenu.isActive():
                clock.tick(60)
                for event in pygame.event.get():
                    retryMenu.handleEvent(event)
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                    elif event.type == Menu.MENUCLICKEDEVENT:
                        if event.text.find('Retry') > -1:
                            retryMenu.deactivate()
                        elif event.text.find('Quit') > -1:
                            return
                screen.blit(background,(0,0))
                if retryMenu.isActive():
                    retryMenu.drawMenu()
                else:
                    background.fill((10,10,10))
                pygame.display.flip()
                
    while levelStart == 10:
        part10 = PartStory('10')
        part10.drawPart()

        while part10.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                part10.handleEvent(event)            
                if event.type == QUIT:
                    return                
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("NEXT") > -1:                    
                        part10.deactivate() 
            screen.blit(background,(0,0))
            if part10.isActive():
                part10.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        introGame10 = IntroGame('10')
        introGame10.drawPart()
        while introGame10.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                introGame10.handleEvent(event)
                if event.type == QUIT:
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Start") > -1:
                        introGame10.deactivate()
            screen.blit(background,(0,0))
            if introGame10.isActive():
                introGame10.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()    

        game10 = Game10()
        game10.drawPart()
        gameRunning = 1
        while gameRunning < 100:
            clock.tick(60)
            for event in pygame.event.get():
                game10.handleEvent(event)
                if event.type == QUIT:
                    return        
            game10.draw()
            pygame.display.flip()
            if game10.isSuccess() or (game10.isActive() == False and game10.isSuccess() == False):
                gameRunning+=1
        if game10.isSuccess():
            levelStart+=1
        else:
            retryMenuOptions = ['Retry','Quit']
            retryMenu = Menu(retryMenuOptions)
            retryMenu.drawMenu()
            while retryMenu.isActive():
                clock.tick(60)
                for event in pygame.event.get():
                    retryMenu.handleEvent(event)
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                    elif event.type == Menu.MENUCLICKEDEVENT:
                        if event.text.find('Retry') > -1:
                            retryMenu.deactivate()
                        elif event.text.find('Quit') > -1:
                            return
                screen.blit(background,(0,0))
                if retryMenu.isActive():
                    retryMenu.drawMenu()
                else:
                    background.fill((10,10,10))
                pygame.display.flip()
                
    while levelStart == 11:
        part11 = PartStory('11')
        part11.drawPart()

        while part11.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                part11.handleEvent(event)            
                if event.type == QUIT:
                    return                
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("NEXT") > -1:                    
                        part11.deactivate() 
            screen.blit(background,(0,0))
            if part11.isActive():
                part11.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        introGame11 = IntroGame('11')
        introGame11.drawPart()
        while introGame11.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                introGame11.handleEvent(event)
                if event.type == QUIT:
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Start") > -1:
                        introGame11.deactivate()
            screen.blit(background,(0,0))
            if introGame11.isActive():
                introGame11.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        game11 = Game11()
        game11.drawPart()
        gameRunning = 1
        while gameRunning < 100:
            clock.tick(60)
            for event in pygame.event.get():
                game11.handleEvent(event)
                if event.type == QUIT:
                    return
            game11.update()
            game11.draw()
            pygame.display.flip()
            if game11.isSuccess() or (game11.isActive() == False and game11.isSuccess() == False):
                gameRunning+=1
        if game11.isSuccess():
            levelStart+=1
        else:
            retryMenuOptions = ['Retry','Quit']
            retryMenu = Menu(retryMenuOptions)
            retryMenu.drawMenu()
            while retryMenu.isActive():
                clock.tick(60)
                for event in pygame.event.get():
                    retryMenu.handleEvent(event)
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                    elif event.type == Menu.MENUCLICKEDEVENT:
                        if event.text.find('Retry') > -1:
                            retryMenu.deactivate()
                        elif event.text.find('Quit') > -1:
                            return
                screen.blit(background,(0,0))
                if retryMenu.isActive():
                    retryMenu.drawMenu()
                else:
                    background.fill((10,10,10))
                pygame.display.flip()

    while levelStart == 12:
        part12 = PartStory('12')
        part12.drawPart()

        while part12.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                part12.handleEvent(event)            
                if event.type == QUIT:
                    return                
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("NEXT") > -1:                    
                        part12.deactivate() 
            screen.blit(background,(0,0))
            if part12.isActive():
                part12.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        introGame12 = IntroGame('12')
        introGame12.drawPart()
        while introGame12.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                introGame12.handleEvent(event)
                if event.type == QUIT:
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Start") > -1:
                        introGame12.deactivate()
            screen.blit(background,(0,0))
            if introGame12.isActive():
                introGame12.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        game12 = Game12()
        game12.drawPart()
        gameRunning = 1
        while gameRunning < 100:
            clock.tick(60)
            for event in pygame.event.get():
                game12.handleEvent(event)
                if event.type == QUIT:
                    return        
            game12.draw()
            pygame.display.flip()
            if game12.isSuccess() or (game12.isActive() == False and game12.isSuccess() == False):
                gameRunning+=1
        if game12.isSuccess():
            levelStart+=1
        else:
            retryMenuOptions = ['Retry','Quit']
            retryMenu = Menu(retryMenuOptions)
            retryMenu.drawMenu()
            while retryMenu.isActive():
                clock.tick(60)
                for event in pygame.event.get():
                    retryMenu.handleEvent(event)
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                    elif event.type == Menu.MENUCLICKEDEVENT:
                        if event.text.find('Retry') > -1:
                            retryMenu.deactivate()
                        elif event.text.find('Quit') > -1:
                            return
                screen.blit(background,(0,0))
                if retryMenu.isActive():
                    retryMenu.drawMenu()
                else:
                    background.fill((10,10,10))
                pygame.display.flip()

    while levelStart == 13:
        introGame13 = IntroGame('13')
        introGame13.drawPart()
        while introGame13.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                introGame13.handleEvent(event)
                if event.type == QUIT:
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Start") > -1:
                        introGame13.deactivate()
            screen.blit(background,(0,0))
            if introGame13.isActive():
                introGame13.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        game13 = Game13()
        game13.drawPart()
        gameRunning = 1
        while gameRunning < 100:
            clock.tick(60)
            for event in pygame.event.get():
                game13.handleEvent(event)
                if event.type == QUIT:
                    return
            game13.update()
            game13.draw()
            pygame.display.flip()
            if game13.isSuccess() or (game13.isActive() == False and game13.isSuccess() == False):
                gameRunning+=1
        if game13.isSuccess():
            levelStart+=1
        else:
            retryMenuOptions = ['Retry','Quit']
            retryMenu = Menu(retryMenuOptions)
            retryMenu.drawMenu()
            while retryMenu.isActive():
                clock.tick(60)
                for event in pygame.event.get():
                    retryMenu.handleEvent(event)
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                    elif event.type == Menu.MENUCLICKEDEVENT:
                        if event.text.find('Retry') > -1:
                            retryMenu.deactivate()
                        elif event.text.find('Quit') > -1:
                            return
                screen.blit(background,(0,0))
                if retryMenu.isActive():
                    retryMenu.drawMenu()
                else:
                    background.fill((10,10,10))
                pygame.display.flip()

    while levelStart == 14:
        part14 = PartStory('14')
        part14.drawPart()

        while part14.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                part14.handleEvent(event)            
                if event.type == QUIT:
                    return                
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("NEXT") > -1:                    
                        part14.deactivate() 
            screen.blit(background,(0,0))
            if part14.isActive():
                part14.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        introGame14 = IntroGame('14')
        introGame14.drawPart()
        while introGame14.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                introGame14.handleEvent(event)
                if event.type == QUIT:
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Start") > -1:
                        introGame14.deactivate()
            screen.blit(background,(0,0))
            if introGame14.isActive():
                introGame14.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        game14 = Game14()
        game14.drawPart()
        gameRunning = 1
        while gameRunning < 100:
            clock.tick(60)
            for event in pygame.event.get():
                game14.handleEvent(event)
                if event.type == QUIT:
                    return        
            game14.draw()
            pygame.display.flip()
            if game14.isSuccess() or (game14.isActive() == False and game14.isSuccess() == False):
                gameRunning+=1
        if game14.isSuccess():
            levelStart+=1
        else:
            retryMenuOptions = ['Retry','Quit']
            retryMenu = Menu(retryMenuOptions)
            retryMenu.drawMenu()
            while retryMenu.isActive():
                clock.tick(60)
                for event in pygame.event.get():
                    retryMenu.handleEvent(event)
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                    elif event.type == Menu.MENUCLICKEDEVENT:
                        if event.text.find('Retry') > -1:
                            retryMenu.deactivate()
                        elif event.text.find('Quit') > -1:
                            return
                screen.blit(background,(0,0))
                if retryMenu.isActive():
                    retryMenu.drawMenu()
                else:
                    background.fill((10,10,10))
                pygame.display.flip()

    while levelStart == 15:        
        part15 = PartStory('15')
        part15.drawPart()

        while part15.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                part15.handleEvent(event)            
                if event.type == QUIT:
                    return                
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("NEXT") > -1:                    
                        part15.deactivate() 
            screen.blit(background,(0,0))
            if part15.isActive():
                part15.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        introGame15 = IntroGame('15')
        introGame15.drawPart()
        while introGame15.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                introGame15.handleEvent(event)
                if event.type == QUIT:
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Start") > -1:
                        introGame15.deactivate()
            screen.blit(background,(0,0))
            if introGame15.isActive():
                introGame15.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()

        game15 = Game15()
        game15.drawPart()
        gameRunning = 1
        while gameRunning < 100:
            clock.tick(60)
            for event in pygame.event.get():
                game15.handleEvent(event)
                if event.type == QUIT:
                    return        
            game15.draw()
            pygame.display.flip()
            if game15.isSuccess() or (game15.isActive() == False and game15.isSuccess() == False):
                gameRunning+=1
        if game15.isSuccess():
            levelStart+=1
        else:
            retryMenuOptions = ['Retry','Quit']
            retryMenu = Menu(retryMenuOptions)
            retryMenu.drawMenu()
            while retryMenu.isActive():
                clock.tick(60)
                for event in pygame.event.get():
                    retryMenu.handleEvent(event)
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
                    elif event.type == Menu.MENUCLICKEDEVENT:
                        if event.text.find('Retry') > -1:
                            retryMenu.deactivate()
                        elif event.text.find('Quit') > -1:
                            return
                screen.blit(background,(0,0))
                if retryMenu.isActive():
                    retryMenu.drawMenu()
                else:
                    background.fill((10,10,10))
                pygame.display.flip()

    if levelStart == 16:
        ending = IntroGame('16')
        ending.drawPart()
        while ending.isActive():
            clock.tick(60)
            for event in pygame.event.get():
                ending.handleEvent(event)
                if event.type == QUIT:
                    return
                elif event.type == Menu.MENUCLICKEDEVENT:
                    if event.text.find("Finish") > -1:
                        ending.deactivate()
            screen.blit(background,(0,0))
            if ending.isActive():
                ending.drawPart()
            else:
                background.fill((10,10,10))
            pygame.display.flip()        
        
        
if __name__ == '__main__':    
    main()
