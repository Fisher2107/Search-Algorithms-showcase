import queue
import pygame
import math
from sys import exit
from collections import deque
import numpy as np
from links import scrubslinkstransform
from switch import Switch
import asyncio


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def algos(chosenalgorithm,enque,admissibleh,pathdict,runtrue):
        
    def dist_finder(a,b):
        x=scrubslinkstransform[a][1]
        y=scrubslinkstransform[b][1]
        return math.sqrt(((x[0]-y[0])**2)+((x[1]-y[1])**2))
            
    if chosenalgorithm=='A*':
        chosenalgorithm,enque,admissibleh='Branch and Bound',True,True

    def conclusion():
        return pathdict,expand,False 
        
    #find what to expand from queue
    if chosenalgorithm == 'Branch and Bound':
        pathlengthlist=tuple(pathdict['queue'][i][1] for i in range(len(pathdict['queue'])))
        if admissibleh:
            disttobeextended = tuple(dist_finder(pathdict['queue'][i][0][-1],chosengoal) for i in range(len(pathdict['queue'])))
            admissibleheuristic=tuple(map(lambda x, y: x + y, pathlengthlist, disttobeextended))
            minnode=min(range(len(admissibleheuristic)), key=admissibleheuristic.__getitem__)
            expand=pathdict['queue'][minnode]
            del pathdict['queue'][minnode]

        else:
            minnode=min(range(len(pathlengthlist)), key=pathlengthlist.__getitem__)
            expand=pathdict['queue'][minnode]
            del pathdict['queue'][minnode]

    elif chosenalgorithm == 'Hillclimb':
        disttobeextended = tuple(dist_finder(pathdict['queue'][i][0][-1],chosengoal) for i in range(len(pathdict['queue'])))
        minnode = min(range(len(disttobeextended)), key=disttobeextended.__getitem__)
        expand=pathdict['queue'][minnode]
        del pathdict['queue'][minnode]

    elif chosenalgorithm == 'Beam':
        #here we are taking paths to consider to be 3
        betaval=3
        if len(pathdict['queue'])>0:
            expand=pathdict['queue'].pop()
        else:
            pathdict['beamlist'].sort(key=lambda x: dist_finder(x[0][-1],chosengoal))

            for i in pathdict['beamlist'][:4]:
                print(i,dist_finder(i[0][-1],chosengoal))
            print("")

            for i in range(min(betaval-1,len(pathdict['beamlist'])-1)):
                pathdict['queue'].appendleft(pathdict['beamlist'][i+1])
            expand=pathdict['beamlist'][0]
            pathdict['beamlist']=[]

    elif chosenalgorithm == 'Breadth first':
            expand=pathdict['queue'].pop()

    elif chosenalgorithm == 'Depthfirst':
        expand=pathdict['queue'].popleft()
    else:
        raise Exception('not listed seach algo selected somehow')
        
    #expanding selected node and adding extenstions back to pathdict['queue']   
    pathdict['extensions']+=1 
    expandnode=expand[0][-1]
    if expandnode == chosengoal:
        return conclusion()
    if expandnode in pathdict['enquedlist']:
        return algos(chosenalgorithm,enque,admissibleh,pathdict,runtrue)
    
    #i represents nodes connected to expandnode        
    for i in scrubslinkstransform[expandnode][0]:
        if i not in expand[0]:
            newnode=(np.append(expand[0],i),expand[1]+dist_finder(expandnode,i))
            if chosenalgorithm == 'Beam': 
                pathdict['beamlist'].append(newnode)
            else:
                pathdict['queue'].append(newnode)
            pathdict['enqueuings']+=1
    if enque:
        pathdict['enquedlist'][expandnode] = None 

    return pathdict,expand,runtrue 

class Button:
    def __init__(self,text,width,height,pos,elevation,group,gui_big=False,radius=10,topcolor='#475F77'):
        #Core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.text = text
        self.group = group
        self.radius = radius

        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = topcolor
        self.top_color_og = topcolor

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#354B5E'
        #text
        if gui_big:
            self.text_surf = gui_font_big.render(text,True,'#FFFFFF')
        else:
            self.text_surf = gui_font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        # elevation logic 
        if not runtrue or self.group in ['speed','speedsub','run']:
            self.top_rect.y = self.original_y_pos - self.dynamic_elecation
            self.text_rect.center = self.top_rect.center 

            self.bottom_rect.midtop = self.top_rect.midtop
            self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

            pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = self.radius)
            pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = self.radius)
            screen.blit(self.text_surf, self.text_rect)
        
            self.check_click()
    
    def drawselected(self):
        self.top_color = '#5496c4'
        self.draw()
            
    def check_click(self):
        global collapsealgo
        global collapsespeed
        global chosenalgorithm
        global chosenspeed
        global choosingstart
        global choosinggoal
        global run
        global pause
        global stop
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                    self.dynamic_elecation = self.elevation
                    if self.pressed == True:
                        if self.group == 'algo' or self.group == 'algosub':
                            collapsealgo = not collapsealgo
                            if self.group == 'algosub':
                                chosenalgorithm = self.text
                        elif self.group == 'speed' or self.group == 'speedsub':
                            collapsespeed = not collapsespeed
                            if self.group == 'speedsub':
                                chosenspeed = self.text
                        elif self.group == 'select':
                            if self.text == 'Set Start':
                                choosingstart = True
                            else: 
                                choosinggoal = True
                        else:  #self.group = 'run'
                            if self.text == 'RUN' and not runtrue:
                                run = True
                            elif runtrue and self.text == 'Pause':
                                pause = True
                            elif runtrue and self.text == 'Stop':
                                stop = True
                            elif runtrue and self.text == 'Resume':
                                pause = False
                        self.pressed = False
                    
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.top_color_og

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('scrubs maze')
clock=pygame.time.Clock()
gui_font = pygame.font.Font(None,30)
gui_font2 = pygame.font.Font(None,40)
gui_font_big2 = pygame.font.Font(None,50)
gui_font_big = pygame.font.Font(None,60)
gui_font_small = pygame.font.Font(None,10)

screen_color = (230, 230, 230)
line_color = (0, 0, 0)
collapsealgo=False
collapsespeed=False


screen.fill(screen_color)


#grouptypes = ('algo','algosub','speed','speedsub','run','select')
#algo buttons
algonames=('Breadth first','Depthfirst','Hillclimb','Beam','Branch and Bound','A*')

buttonalgoselect = Button('Select search algorithm:',320,40,(0,5),5,'algo')
button1 = Button(algonames[0],320,30,(0,47),2,'algosub')
button2 = Button(algonames[1],320,30,(0,79),2,'algosub')
button3 = Button(algonames[2],320,30,(0,111),2,'algosub')
button4 = Button(algonames[3],320,30,(0,143),2,'algosub')
button5 = Button(algonames[4],320,30,(0,175),2,'algosub')
button6 = Button(algonames[5],320,30,(0,207),2,'algosub')

algobuttonlist=(button1,button2,button3,button4,button5,button6)

#switchstatus, is either False if switch not there or is 'On' or 'Off'
switch1status = False
switch2status = False

#set orgin and destination buttons
buttonstart = Button('Set Start',180,40,(540,7),5,'select',radius=30)
buttongoal = Button('Set Goal',180,40,(725,7),5,'select',radius=30)

#speedbuttons
speednames=('1 fps','4 fps','30 fps','no limit')
speedsdict= {'1 fps':60,'4 fps':15,'30 fps':1,'no limit':0}
setspeedi=0

buttonspeedselect = Button('Speed:',160,40,(320,5),5,'speed')
buttonslow = Button(speednames[0],160,30,(320,47),2,'speedsub')
buttonmed  = Button(speednames[1],160,30,(320,79),2,'speedsub')
buttonfast = Button(speednames[2],160,30,(320,111),2,'speedsub')
buttonnocap= Button(speednames[3],160,30,(320,143),2,'speedsub')

speedbuttonlist=(buttonslow,buttonmed,buttonfast,buttonnocap)

#run, pause resume buttons
buttonrun = Button('RUN',282,60,(900,620),5,'run',True)
buttonpause = Button('Pause',94,30,(900,587),3,'run')
buttonstop = Button('Stop',94,30,(994,587),3,'run')
buttonresume = Button('Resume',94,30,(1088,587),3,'run')

#run is when run button is clicked
run = False
#runtrue is when class algos is activated
runtrue = False
ran = False
pause = False
stop = False
#in case of error
mistakes = []
#selectedbuttons
chosenalgorithm='Not selected'
chosenspeed='4 fps'
#where user clicked in (x,y)
clickedstart = None
clickedgoal = None
#which node is activated
chosenstart = None
chosengoal = None
#creates animation of start and goal selection
choosinggoal = False
choosingstart = False
clicked=False
#Top right stuff
selectedalgotext = gui_font.render('Selected Algorithm:',True,'black')
goaltextsurf = gui_font.render('Goal',True,'green')
starttextsurf = gui_font.render('Start',True,'red')
algotextborder = pygame.Rect((930,30),(324,80))

enquetext = gui_font.render('+ Extended list',True,'black')
admissibletext = gui_font.render('+ Admissible',True,'black')
heuristictext = gui_font.render('  Heuristic',True,'black')
def drawtopright():
    algotext = gui_font_big2.render(chosenalgorithm,True,'black')
    algotextrect = algotext.get_rect(center = (1092,70))
    
    pygame.draw.rect(screen,'white',algotextborder,border_radius=20)
    pygame.draw.rect(screen,'black',algotextborder,5,20)

    screen.blit(selectedalgotext,(992,7))
    screen.blit(algotext,algotextrect)
    

#switches
switch1=Switch(60,(1200,122),0,screen)
switch2=Switch(60,(1200,170),1,screen)
def drawswitches():
    global switch1status
    global switch2status
    if chosenalgorithm != 'Not selected' and chosenalgorithm != 'A*':
        switch1status,screen=switch1.draw(runtrue)  
        screen.blit(enquetext,(1025,126))
    else: switch1status = False

    if chosenalgorithm == 'Branch and Bound':
        switch2status,screen=switch2.draw(runtrue)  
        screen.blit(admissibletext,(1025,165))
        screen.blit(heuristictext,(1069,190))
    else: switch2status = False

def error():
    errormessage2 = ''
    for i in range(len(mistakes)):
        if i==0:
            errormessage = 'Error: '
            errormessage += mistakes[i]
            errormessagefont = gui_font.render(errormessage,True,'red')
            screen.blit(errormessagefont,(900,560 - 30*(len(mistakes)-1)))
        elif i==1:
            errormessage2 = ' & '
            errormessage2 += mistakes[i]
            errormessagefont = gui_font.render(errormessage2,True,'red')
            screen.blit(errormessagefont,(980,560 - 30*(len(mistakes)-2)))
        else:
            errormessage3 = ' & '
            errormessage3 += mistakes[i]
            errormessagefont = gui_font.render(errormessage3,True,'red')
            screen.blit(errormessagefont,(980,560))

async def main():
    global choosingstart,choosinggoal,chosenstart,chosengoal
    global collapsealgo,collapsespeed
    global run,runtrue,ran,pause,stop
    global mistakes
    global clicked
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        screen.fill(screen_color)
        #switches
        drawswitches()
        
        #selects
        buttonalgoselect.draw()
        buttonspeedselect.draw()
        
        #Origin, Destination
        mouse_pos = pygame.mouse.get_pos()
        buttonstart.draw()
        buttongoal.draw()

        def drawstart():
            redstartrect = pygame.draw.rect(screen,'green',mousestart,border_radius=2)
            starttextrect = starttextsurf.get_rect(center = redstartrect.center)
            screen.blit(starttextsurf, starttextrect)
            pygame.draw.circle(screen,'blue',redstartrect.midbottom,4)
            
        if choosingstart:
            mousestart = pygame.Rect((0,0),(55,30))
            mousestart.midbottom = mouse_pos
            drawstart()
            if pygame.mouse.get_pressed()[0]: 
                clicked = True
            else:
                if clicked:
                    choosingstart = False
                    clickedstart = mouse_pos
                    closestdistance=10000000
                    for i in range(1,len(scrubslinkstransform)+1):
                        if math.sqrt(((scrubslinkstransform[i][1][0]-clickedstart[0])**2)+((scrubslinkstransform[i][1][1]-clickedstart[1])**2)) < closestdistance:
                            closestdistance = math.sqrt(((scrubslinkstransform[i][1][0]-clickedstart[0])**2)+((scrubslinkstransform[i][1][1]-clickedstart[1])**2))
                            chosenstart = i
                    mousestart.midbottom = scrubslinkstransform[chosenstart][1]
                    clicked = False
                    
        if chosenstart:
            drawstart()
            if math.sqrt(((scrubslinkstransform[chosenstart][1][0]-mouse_pos[0])**2)+((scrubslinkstransform[chosenstart][1][1]-mouse_pos[1])**2)) <= 5:
                if pygame.mouse.get_pressed()[0]:
                    choosingstart = True
            
        def drawgoal():
            redgoalrect = pygame.draw.rect(screen,'red',mousegoal,border_radius=2)
            goaltextrect = goaltextsurf.get_rect(center = redgoalrect.center)
            screen.blit(goaltextsurf, goaltextrect)
            pygame.draw.circle(screen,'blue',redgoalrect.midbottom,4)
            
        if choosinggoal:
            mousegoal = pygame.Rect((0,0),(55,30))
            mousegoal.midbottom = mouse_pos
            drawgoal()
            if pygame.mouse.get_pressed()[0]: 
                clicked = True
            else:
                if clicked:
                    choosinggoal = False
                    clickedgoal = mouse_pos
                    closestdistance=10000000
                    for i in range(1,len(scrubslinkstransform)+1):
                        if math.sqrt(((scrubslinkstransform[i][1][0]-clickedgoal[0])**2)+((scrubslinkstransform[i][1][1]-clickedgoal[1])**2)) < closestdistance:
                            closestdistance = math.sqrt(((scrubslinkstransform[i][1][0]-clickedgoal[0])**2)+((scrubslinkstransform[i][1][1]-clickedgoal[1])**2))
                            chosengoal = i
                    mousegoal.midbottom = scrubslinkstransform[chosengoal][1]
                    clicked = False
                    
        if chosengoal:
            drawgoal()
            if math.sqrt(((scrubslinkstransform[chosengoal][1][0]-mouse_pos[0])**2)+((scrubslinkstransform[chosengoal][1][1]-mouse_pos[1])**2)) <= 5:
                if pygame.mouse.get_pressed()[0]:
                    choosinggoal = True
        #run
        buttonrun.draw()
        buttonpause.draw()
        buttonresume.draw()
        buttonstop.draw()
        
        #Text topright
        drawtopright()
        #temptext = gui_font_big2.render(str((switch1status,switch2status)),True,'black')
        #algotextrect = temptext.get_rect(center = (1092,70))
        #screen.blit(temptext,algotextrect)
        #screen.blit(temptext,algotextrect)
        
        #collapse buttons draw
        if collapsealgo: #1
            for i,button in enumerate(algobuttonlist):
                if chosenalgorithm == algonames[i]:
                    button.drawselected()
                else:
                    button.draw()
            
        if collapsespeed: #2
            for i,button in enumerate(speedbuttonlist):
                if chosenspeed == speednames[i]:
                    button.drawselected()
                else:
                    button.draw()

        #draw map    
        for i in range(1,len(scrubslinkstransform)+1):
            for j in scrubslinkstransform[i][0]:
                if j>i:
                    pygame.draw.line(screen,line_color, scrubslinkstransform[i][1], scrubslinkstransform[j][1],width=2)
                    
        if runtrue and setspeedi>=speedsdict[chosenspeed]:

            #whichalgo is chosenalgroithm
            if switch1status == 'On' and switch2status == 'On':
                enque,admissibleh=True,True
            elif switch1status == 'On':
                enque,admissibleh=True,False
            elif switch2status == 'On':
                enque,admissibleh=False,True
            else:
                enque,admissibleh=None,None

            pathdict,expand,runtrue = algos(chosenalgorithm,enque,admissibleh,pathdict,runtrue)

            path=expand[0]

            enqueuingstext = gui_font2.render('Enqueuings = ' + str(pathdict['enqueuings']),True,'#1f1f1f')
            extensionstext = gui_font2.render('Extensions = ' + str(pathdict['extensions']-1),True,'#1f1f1f')
            queuesizetext = gui_font2.render('Queuesize = ' + str(len(pathdict['queue'])),True,'#1f1f1f')
            pathelementstext = gui_font2.render('Path Elements = ' + str(len(expand[0])),True,'#1f1f1f')
            pathlenghttext = gui_font2.render('Path Length = ' + str("{:.2f}".format(expand[1])),True,'#1f1f1f')

            if not runtrue:
                stop = False
                pause = False
                runtrue = False
                ran = True
                setspeedi=0
            setspeedi=0

        elif runtrue and not pause:
            setspeedi+=1

        if runtrue and stop:
            stop = False
            pause = False
            runtrue = False
            ran = True
            setspeedi=0


        if ran or runtrue:
            for i in range(len(path)-1):
                pygame.draw.line(screen,'red', scrubslinkstransform[path[i]][1], scrubslinkstransform[path[i+1]][1],width=5)
            #draw enqued nodes
            for i in pathdict['enquedlist']:    
                pygame.draw.circle(screen,'red', scrubslinkstransform[i][1],radius=4)
            #bottom left
            screen.blit(enqueuingstext,(15,500))
            screen.blit(extensionstext,(15,542))
            screen.blit(queuesizetext,(15,584))
            screen.blit(pathelementstext,(15,626))
            screen.blit(pathlenghttext,(15,668))


        if run:
            if chosengoal and chosenstart and chosenalgorithm != 'Not selected':
                runtrue = True
                collapsespeed = False
                collapsealgo = False
                run = False

                pathdict={
                    'queue': deque(),
                    'enqueuings':0,
                    'extensions':0,
                    'enquedlist':{},
                    'beamlist': [],
                }
                pathdict['queue'].append((np.array([chosenstart]),0))

                setspeedi=100
            else:
                mistakes = []
                if chosenalgorithm == 'Not selected': mistakes.append('Not chosen Algorithm')
                if not chosenstart: mistakes.append('Not selected Start')
                if not chosengoal: mistakes.append('Not selected Goal')
                errormessage = 'Error: '
                error()
                run = False

            
        if len(mistakes) > 0:
            error()
            if pygame.mouse.get_pressed()[0]: 
                mistakes = []
            
            
        pygame.display.update()
        if not (chosenspeed=='no limit' and runtrue):
            clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
