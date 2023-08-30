import pygame

class Switch:
    def __init__(self,width,pos,identity,screen):
        self.screen=screen
        self.pressed = False
        self.width = width
        self.pos=pos
        self.radius = width//4
        self.font = pygame.font.Font(None,width//3)
        #switch 1 has identity 0, switch 2 has identity 1
        self.identity = identity
        
        self.wholerect = pygame.Rect(pos,(width,width//2))
        self.middlerect = pygame.Rect((pos[0]+width//4,pos[1]),(width//2,width//2))
        self.middlecolor = 'Red'
        
        self.movingcirclepos = [self.pos[0]+3*self.radius,self.pos[1]+self.radius]
        self.movement = 0
        self.direction = -5
        
        self.leftcircle = pygame.draw.circle(self.screen,'Red',(pos[0]+self.radius,pos[1]+self.radius),self.radius,0)
        self.rightcircle = pygame.draw.circle(self.screen,'Green',(pos[0]+3*self.radius,pos[1]+self.radius),self.radius,0)

        self.textoff_surf = self.font.render('Off',True,'black')
        self.texton_surf = self.font.render('On',True,'black')
        self.textoff_rect =  self.textoff_surf.get_rect(center = (pos[0]+self.radius,pos[1]+self.radius))
        self.texton_rect = self.texton_surf.get_rect(center = (pos[0]+3*self.radius,pos[1]+self.radius))
       
        
    def draw(self,runtrue):
        if self.movingcirclepos[0] == self.pos[0]+3*self.radius:
             self.direction = -abs(self.direction)
        elif self.movingcirclepos[0] == self.pos[0]+self.radius:
            self.direction = abs(self.direction)
        if self.movement != 0:
            self.movingcirclepos[0] += self.direction
            self.movement -= abs(self.direction)
        
        #optional addition of outline on switch, I personally prefer it without which is why I ommited it
        '''pygame.draw.line(screen,'black',(self.pos[0]+self.width//4,self.pos[1]),(self.pos[0]+3*self.width//4,self.pos[1]),width=5)
        pygame.draw.line(screen,'black',(self.pos[0]+self.width//4,self.pos[1]+self.width//2),(self.pos[0]+3*self.width//4,self.pos[1]+self.width//2),width=3) 
        pygame.draw.circle(screen,'black',(self.pos[0]+self.radius,self.pos[1]+self.radius),self.radius+2,10)
        pygame.draw.circle(screen,'black',(self.pos[0]+3*self.radius,self.pos[1]+self.radius),self.radius+2,10)'''
        
        pygame.draw.rect(self.screen,self.middlecolor, self.middlerect)
        
        pygame.draw.circle(self.screen,'Red',(self.pos[0]+self.radius,self.pos[1]+self.radius),self.radius,0)
        pygame.draw.circle(self.screen,'Green',(self.pos[0]+3*self.radius,self.pos[1]+self.radius),self.radius,0)
        
        self.screen.blit(self.textoff_surf, self.textoff_rect)
        self.screen.blit(self.texton_surf, self.texton_rect) 
        
        pygame.draw.circle(self.screen,'#979797',self.movingcirclepos ,self.radius,0)
        return self.check_click(runtrue)
        
    def check_click(self,runtrue):
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
            if self.identity: switchstatus = 'Off'
            else: switchstatus = 'Off'
        else:
            if self.identity: switchstatus = 'On'
            else: switchstatus = 'On'
        return (switchstatus,self.screen)