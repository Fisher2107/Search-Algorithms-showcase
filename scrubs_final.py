import pygame
import math
from sys import exit
from collections import deque
import numpy as np


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

scrubslinks={1:((2,),(23.2,83.7)),
            2:((1,3,4),(39.7,83.6)),
            3:((2,5),(45.4,73.4)),
            4:((2,5,6),(52.6,83)),
            5:((3,4,7,47),(52.9,73.6)),
            6:((4,7,17),(67.3,99.4)),
            7:((5,6,8,15),(72.1,85.8)),
            8:((7,9,14,47),(72,73.1)),
            9:((8,13,47),(75.3,63.4)),
            10:((11,12,47),(51,59.1)),
            11:((10,),(49.1,54.5)),
            12:((10,13,25),(87.3,56.5)),
            13:((9,12,14,23,24),(96.1,63.3)),
            14:((8,13,15,18,23),(102.5,83.6)),
            15:((7,14,16),(107.4,106.9)),
            16:((15,17,18,45),(140.4,127.1)),
            17:((6,16,46),(140.6,130.6)),
            18:((14,16,19,20),(157.4,95.3)),
            19:((18,20,22,23),(146.7,72.0)),
            20:((18,19,21),(162.3,74.3)),
            21:((20,22),(166.4,56.5)),
            22:((19,21,23,24,29),(144.7,45.3)),
            23:((13,14,19,22),(118.1,63.4)),
            24:((13,22,25,28),(133.2,35.9)),
            25:((12,24,26,27),(121.3,27.9)),
            26:((25,),(117.4,24.5)),
            27:((25,28,31),(133.8,8.8)),
            28:((24,27,29,30),(146.7,14)),
            29:((22,28,30,35),(157,21.8)),
            30:((28,29,33),(162.3,16.8)),
            31:((27,32,33,34),(202,12.6)),
            32:((31,),(202.3,4.4)),
            33:((30,31,35),(198.9,21.5)),
            34:((31,36),(218.3,21.5)),
            35:((29,33,37),(198.9,44.5)),
            36:((34,37,38),(206.3,54.7)),
            37:((35,36,42),(199.1,61.6)),
            38:((36,39),(277.9,65.2)),
            39:((38,40),(300.8,51.9)),
            40:((39,41,42),(337.2,61.6)),
            41:((40,),(343.2,61.4)),
            42:((37,40,43),(310.6,85.7)),
            43:((42,44,45),(284.9,119.3)),
            44:((43,),(291.2,124.7)),
            45:((16,43,46),(220.5,156.2)),
            46:((17,45),(209.6,159.5)),
            47:((5,8,9,10),(53.1,63.4)),
            }

scrubslinkstransform = {}
for i in range(1,len(scrubslinks)+1):
    #e is equal to enlargement factor
    e=3.7
    scrubslinkstransform[i] = (scrubslinks[i][0],(scrubslinks[i][1][0]*e-40,(SCREEN_HEIGHT - scrubslinks[i][1][1]*e)-40))

class search2:
    def __init__(self,map):
        self.map=map
        
    def dist_finder(self,a,b):
        x=self.map[a][1]
        y=self.map[b][1]
        return math.sqrt(((x[0]-y[0])**2)+((x[1]-y[1])**2))

    def breadthfirst(self,x,y,enque=False):
        return self.algos(x,y,'breadth',enque)

    def depthfirst(self,x,y,enque=False):
        return self.algos(x,y,'depth',enque)

    def hillclimb(self,x,y,enque=False):
        return self.algos(x,y,'hillclimb',enque)

    def beam(self,x,y,enque=False):
        return self.algos(x,y,'beam',enque)
    
    def branchbound(self,x,y,enque=False,admissibleh=False):
        return self.algos(x,y,'branchbound',enque,admissibleh)
    
    def Astar(self,x,y):
        return self.branchbound(x,y,True,True)
    
    def algos(self,x,y,whichalgo,enque,admissibleh=False):
        global enquedlist
        queue=deque()
        queue.append((np.array([x]),0))
        enqueuings=0
        extensions=0
        pathlength=0
        enquedlist={}
        
        def conclusion(popped=0):
            global enqueuingstext
            global extensionstext
            global queuesizetext
            global pathelementstext
            global pathlenghttext
            enqueuingstext = gui_font2.render('Enqueuings = ' + str(enqueuings),True,'#1f1f1f')
            extensionstext = gui_font2.render('Extensions = ' + str(extensions),True,'#1f1f1f')
            queuesizetext = gui_font2.render('Queuesize = ' + str(len(queue)+popped),True,'#1f1f1f')
            pathelementstext = gui_font2.render('Path Elements = ' + str(len(expand[0])),True,'#1f1f1f')
            pathlenghttext = gui_font2.render('Path Length = ' + str("{:.2f}".format(expand[1])),True,'#1f1f1f')
            screen.blit(enqueuingstext,(15,500))
            screen.blit(extensionstext,(15,542))
            screen.blit(queuesizetext,(15,584))
            screen.blit(pathelementstext,(15,626))
            screen.blit(pathlenghttext,(15,668))
            return expand[0]
        
        if whichalgo == 'beam':
            beamlist=deque()
        elif whichalgo == 'breadth':
            breadthnum=1
            
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            #print(queue)
            if whichalgo == 'branchbound':
                pathlengthlist=tuple(queue[i][1] for i in range(len(queue)))
                if admissibleh:
                    disttobeextended = tuple(self.dist_finder(queue[i][0][-1],y) for i in range(len(queue)))
                    admissibleheuristic=tuple(map(lambda x, y: x + y, pathlengthlist, disttobeextended))
                    minnode=min(range(len(admissibleheuristic)), key=admissibleheuristic.__getitem__)
                    expand=queue[minnode]
                    del queue[minnode]
                    #print(pathlengthlist)
                    #print(disttobeextended)
                    #print(admissibleheuristic)
                    #print(minnode)   
                else:
                    minnode=min(range(len(pathlengthlist)), key=pathlengthlist.__getitem__)
                    expand=queue[minnode]
                    del queue[minnode]
                    #print(pathlengthlist)
                    #print(minnode)      

            elif whichalgo == 'hillclimb':
                disttobeextended = tuple(self.dist_finder(queue[i][0][-1],y) for i in range(len(queue)))
                minnode = min(range(len(disttobeextended)), key=disttobeextended.__getitem__)
                expand=queue[minnode]
                del queue[minnode]
                #print(disttobeextended)
                #print(minnode)
            elif whichalgo == 'beam':
            #here we are taking paths to consider to be 3
                #print(beamlist)
                #print('')
                if len(beamlist)==0:
                    if len(queue)<=3:
                        expand=queue.pop()
                    else:
                        disttobeextended = tuple(self.dist_finder(queue[i][0][-1],y) for i in range(len(queue)))
                        if 0 in disttobeextended:
                            expand=queue[disttobeextended.index(0)]
                            return conclusion()
                        minnodes=[0,0,0]
                        minnodesindex=[0,1,2]
                        maxmin=[0,0]
                        for i,distance in enumerate(disttobeextended):
                            if i<=2:
                                minnodes[i]=distance
                                if distance>maxmin[1]:
                                    maxmin = [i,distance]
                            else:
                                if distance<maxmin[1]:
                                    minnodes[maxmin[0]]=distance
                                    minnodesindex[maxmin[0]]=i
                                    maxmin=[minnodes.index(max(minnodes)),max(minnodes)]
                        #print(minnodes)
                        #print(minnodesindex)
                        for i in minnodesindex: beamlist.append(queue[i])
                        minnodesindex.sort(reverse=True)
                        for i in range(3): del queue[minnodesindex[i]]
                else:
                    expand=beamlist.pop()
            elif whichalgo == 'breadth':
                if breadthnum!=0:
                    expand=queue.pop()
                    breadthnum-=1
                else:
                    for i in range(len(queue)):
                        if y==queue[i][0][-1]:
                            expand=queue[i]
                            return conclusion()

                    breadthnum=len(queue)
                    expand=queue.pop()
                    breadthnum-=1
                    #print('not in queue')

            elif whichalgo == 'depth':
                expand=queue.popleft()
            else:
                return "error"
                
            #expanding selected node and adding extenstions back to queue    
            expandnode=expand[0][-1]
            if expandnode == y:
                return conclusion(1)
            if expandnode in enquedlist:
                continue
            #i represents nodes connected to expandnode        
            for i in self.map[expandnode][0]:
                if i not in expand[0]:
                        newnode=(np.append(expand[0],i),expand[1]+self.dist_finder(expandnode,i))
                        queue.appendleft(newnode)
                        enqueuings+=1
            extensions+=1
            if enque:
                enquedlist[expandnode] = None   
            
            
            #drawing stuff
            setspeed = speedslist[speednames.index(chosenspeed)]
            setspeedi=0
            drawbottomright = True
            while setspeedi<setspeed:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                screen.fill(screen_color)
                
                #draw map    
                for i in range(1,len(scrubslinkstransform)+1):
                    for j in scrubslinkstransform[i][0]:
                        if j>i:
                            pygame.draw.line(screen,line_color, scrubslinkstransform[i][1], scrubslinkstransform[j][1],width=2)
                            
                #draw buttons
                buttonrun.draw()
                buttonpause.draw()
                buttonresume.draw()
                buttonstop.draw()
                #draw switches
                drawswitches()
                #start and gaol
                drawstart()
                drawgoal()
                #draw top right stuff
                drawtopright()
                #draw speed
                buttonspeedselect.draw()
                if collapsespeed: #2
                    for i,button in enumerate(speedbuttonlist):
                        if chosenspeed == speednames[i]:
                            button.drawselected()
                        else:
                            button.draw()
                
                #drawing selectedline
                for i in range(len(expand[0])-1):
                    pygame.draw.line(screen,'red', scrubslinkstransform[expand[0][i]][1], scrubslinkstransform[expand[0][i+1]][1],width=5)

                #draw enqued nodes
                for i in enquedlist:    
                    pygame.draw.circle(screen,'red', scrubslinkstransform[i][1],radius=4)

                setspeed = speedslist[speednames.index(chosenspeed)]
                setspeedi +=1
                
                #draw bottomleft
                if drawbottomright:
                    enqueuingstext = gui_font2.render('Enqueuings = ' + str(enqueuings),True,'#1f1f1f')
                    extensionstext = gui_font2.render('Extensions = ' + str(extensions),True,'#1f1f1f')
                    queuesizetext = gui_font2.render('Queuesize = ' + str(len(queue)+1),True,'#1f1f1f')
                    pathelementstext = gui_font2.render('Path Elements = ' + str(len(expand[0])),True,'#1f1f1f')
                    pathlenghttext = gui_font2.render('Path Length = ' + str("{:.2f}".format(expand[1])),True,'#1f1f1f')
                    drawbottomright = False
                screen.blit(enqueuingstext,(15,500))
                screen.blit(extensionstext,(15,542))
                screen.blit(queuesizetext,(15,584))
                screen.blit(pathelementstext,(15,626))
                screen.blit(pathlenghttext,(15,668))
                
                if pause:
                    setspeedi = setspeed -1 
                    
                pygame.display.update()
                
                if stop:
                    return conclusion(1)
                
                if not setspeed==1:
                    clock.tick(60)

class Switch:
    def __init__(self,width,pos,identity):
        self.pressed = False
        self.width = width
        self.pos=pos
        self.radius = width//4
        self.font = pygame.font.Font(None,width//3)
        self.identity = identity
        
        self.wholerect = pygame.Rect(pos,(width,width//2))
        self.middlerect = pygame.Rect((pos[0]+width//4,pos[1]),(width//2,width//2))
        self.middlecolor = 'Red'
        
        self.movingcirclepos = [self.pos[0]+3*self.radius,self.pos[1]+self.radius]
        self.movement = 0
        self.direction = -5
        
        self.leftcircle = pygame.draw.circle(screen,'Red',(pos[0]+self.radius,pos[1]+self.radius),self.radius,0)
        self.rightcircle = pygame.draw.circle(screen,'Green',(pos[0]+3*self.radius,pos[1]+self.radius),self.radius,0)

        self.textoff_surf = self.font.render('Off',True,'black')
        self.texton_surf = self.font.render('On',True,'black')
        self.textoff_rect =  self.textoff_surf.get_rect(center = (pos[0]+self.radius,pos[1]+self.radius))
        self.texton_rect = self.texton_surf.get_rect(center = (pos[0]+3*self.radius,pos[1]+self.radius))
       
        
    def draw(self):
        if self.movingcirclepos[0] == self.pos[0]+3*self.radius:
             self.direction = -abs(self.direction)
        elif self.movingcirclepos[0] == self.pos[0]+self.radius:
            self.direction = abs(self.direction)
        if self.movement != 0:
            self.movingcirclepos[0] += self.direction
            self.movement -= abs(self.direction)
        
        #optional addition of outline on switch, I personally prefer it without which is why I ommited it
        #pygame.draw.line(screen,'black',(self.pos[0]+self.width//4,self.pos[1]),(self.pos[0]+3*self.width//4,self.pos[1]),width=5)
        #pygame.draw.line(screen,'black',(self.pos[0]+self.width//4,self.pos[1]+self.width//2),(self.pos[0]+3*self.width//4,self.pos[1]+self.width//2),width=3) 
        #pygame.draw.circle(screen,'black',(self.pos[0]+self.radius,self.pos[1]+self.radius),self.radius+2,10)
        #pygame.draw.circle(screen,'black',(self.pos[0]+3*self.radius,self.pos[1]+self.radius),self.radius+2,10)        
        
        pygame.draw.rect(screen,self.middlecolor, self.middlerect)
        
        pygame.draw.circle(screen,'Red',(self.pos[0]+self.radius,self.pos[1]+self.radius),self.radius,0)
        pygame.draw.circle(screen,'Green',(self.pos[0]+3*self.radius,self.pos[1]+self.radius),self.radius,0)
        
        screen.blit(self.textoff_surf, self.textoff_rect)
        screen.blit(self.texton_surf, self.texton_rect) 
        
        pygame.draw.circle(screen,'#979797',self.movingcirclepos ,self.radius,0)
        self.check_click()
        
    def check_click(self):
        global switch1status
        global switch2status
        mouse_pos = pygame.mouse.get_pos()
        if self.wholerect.collidepoint(mouse_pos) and not runtrue:
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    self.movement = self.width//2
                    if self.middlecolor == 'Red':
                        self.middlecolor = 'Green'
                    else: 
                        self.middlecolor = 'Red'
                    self.pressed = False
                    
        if self.middlecolor == 'Red':
            if self.identity: switch2status = 'Off'
            else: switch1status = 'Off'
        else:
            if self.identity: switch2status = 'On'
            else: switch1status = 'On'

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
algonames2 = ('breadthfirst','depthfirst','hillclimb','beam','branchbound','Astar')

buttonalgoselect = Button('Select search algorithm:',320,40,(0,5),5,'algo')
button1 = Button(algonames[0],320,30,(0,47),2,'algosub')
button2 = Button(algonames[1],320,30,(0,79),2,'algosub')
button3 = Button(algonames[2],320,30,(0,111),2,'algosub')
button4 = Button(algonames[3],320,30,(0,143),2,'algosub')
button5 = Button(algonames[4],320,30,(0,175),2,'algosub')
button6 = Button(algonames[5],320,30,(0,207),2,'algosub')

algobuttonlist=(button1,button2,button3,button4,button5,button6)


#switches
switch1=Switch(60,(1200,122),0)
switch2=Switch(60,(1200,170),1)

#switchstatus, is either False if switch not there or is 'On' or 'Off'
switch1status = False
switch2status = False

#set orgin and destination buttons
buttonstart = Button('Set Start',180,40,(540,7),5,'select',radius=30)
buttongoal = Button('Set Goal',180,40,(725,7),5,'select',radius=30)

#speedbuttons
speednames=('1 fps','4 fps','30 fps','no cap')
speedslist= (60,15,2,1)

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
    


def drawswitches():
    global switch1status
    global switch2status
    if chosenalgorithm != 'Not selected' and chosenalgorithm != 'A*':
        switch1.draw()  
        screen.blit(enquetext,(1025,126))
    else: switch1status = False

    if chosenalgorithm == 'Branch and Bound':
        switch2.draw()  
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
                
    if runtrue:

        but=search2(scrubslinks)
        algonum = algonames.index(chosenalgorithm)
        if switch1status == 'On' and switch2status == 'On':
            path = getattr(but, algonames2[algonum])(chosenstart,chosengoal,True,True)
        elif switch1status == 'On':
            path = getattr(but, algonames2[algonum])(chosenstart,chosengoal,True)
        elif switch2status == 'On':
            path = getattr(but, algonames2[algonum])(chosenstart,chosengoal,False,True)
        else:
            path = getattr(but, algonames2[algonum])(chosenstart,chosengoal)
        stop = False
        pause = False
        runtrue = False
        ran = True
    if run:
        if chosengoal and chosenstart and chosenalgorithm != 'Not selected':
            runtrue = True
            collapsespeed = False
            collapsealgo = False
            run = False
        else:
            mistakes = []
            if chosenalgorithm == 'Not selected': mistakes.append('Not chosen Algorithm')
            if not chosenstart: mistakes.append('Not selected Start')
            if not chosengoal: mistakes.append('Not selected Goal')
            errormessage = 'Error: '
            error()
            run = False
    if ran:
        for i in range(len(path)-1):
            pygame.draw.line(screen,'red', scrubslinkstransform[path[i]][1], scrubslinkstransform[path[i+1]][1],width=5)
        #draw enqued nodes
        for i in enquedlist:    
            pygame.draw.circle(screen,'red', scrubslinkstransform[i][1],radius=4)
        #bottom left
        screen.blit(enqueuingstext,(15,500))
        screen.blit(extensionstext,(15,542))
        screen.blit(queuesizetext,(15,584))
        screen.blit(pathelementstext,(15,626))
        screen.blit(pathlenghttext,(15,668))
        
    if len(mistakes) > 0:
        error()
        if pygame.mouse.get_pressed()[0]: 
            mistakes = []
        
        
    pygame.display.update()
    clock.tick(60)
