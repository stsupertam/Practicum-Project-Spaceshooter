import pygame,sys,random
from practicum import findDevices
from peri import PeriBoard
from numpy import interp

#constant of game
screen = pygame.display.set_mode((640,480))
screen_width = screen.get_width()
screen_height = screen.get_height()
win_number = 0
devs = findDevices()
if len(devs) == 0:
    print '*** No MCU board found.'
    board = None
else:
    board = PeriBoard(devs[0])
    print '*** MCU board found'
    print '*** Device manufacturer: %s' % board.getVendorName()
    print '*** Device name: %s' % board.getDeviceName()
    print 'Calibrating board.'

    raw_input('Face the board down then press ENTER...')

    minLight = board.getLight()
    print minLight 
    raw_input('Face the board up then press ENTER...')

    maxLight = board.getLight()
    print maxLight
    board.lightRange = (minLight,maxLight)

#class of object in the game
class Boss:
    def __init__(self,xpos,ypos,image):
        self.health = 100
        self.x = xpos
        self.y = ypos
        self.speed = 5
        self.image = image
        self.bullets = []
        self.boss_width = image.get_width()
        self.boss_height = image.get_height()
    def render(self):
        screen.blit(self.image,(self.x,self.y))
    def move(self,direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        elif direction == "right" and self.x < screen_width-self.boss_width:
            self.x += self.speed
        elif direction == "up" and self.y < screen_width-self.player_width:
            self.y += self.speed
        elif direction == "down" and self.x < screen_width-self.player_width:
            self.x += self.speed
            
class Player:
    def __init__(self,xpos,ypos,image):
        self.health = 3
        self.x = xpos
        self.y = ypos
        self.speed = 5
        self.image = image
        self.bullets = []
        self.player_width = image.get_width()
        self.player_height = image.get_height()
    def render(self):
        screen.blit(self.image,(self.x,self.y))
    def move(self,direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        elif direction == "right" and self.x < screen_width-self.player_width:
            self.x += self.speed

class Enemy:
    def __init__(self,xpos,ypos,image):
        self.x = xpos
        self.y = ypos
        self.speed = 3
        self.image = image
        self.bullets = []
        self.enemy_width = image.get_width()
        self.enemy_height = image.get_height()
        self.godown = False
    def render(self):
        screen.blit(self.image,(self.x,self.y))
    def enemymove(self):
        if self.x > screen_width-self.enemy_width:
            enemy.y += 5
            self.speed = -3

class Bullet:
    def __init__(self,xpos,ypos,image):
        self.x = xpos
        self.y = ypos
        self.image = image
        self.speed = 5
        self.bullet_width = image.get_width()
        self.bullet_height = image.get_height()
    def render(self):
        screen.blit(self.image,(self.x,self.y))
    def checkcollide(self,sprite_x,sprite_y):
        if (self.x > sprite_x-32) and (self.x < sprite_x +32) and (self.y > sprite_y-32) and (self.y < sprite_y+32):
            return True
        return False
    def checkcollideboss(self,sprite_x,sprite_y):
        if (self.x > sprite_x-64) and (self.x < sprite_x +64) and (self.y > sprite_y-64) and (self.y < sprite_y+64):
            return True
        return False
    def outofscreen(self):
        if self.y < 0 or self.y > screen_width:
            return True
        return False
    def move(self,direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        elif direction == "right" and self.x < screen_width-self.bullet_width:
            self.x += self.speed


class Barrier:
    def __init__(self,xpos,ypos,image):
        self.bullet = []
        self.x = xpos
        self.y = ypos
        self.health = 4
        self.speed = 5
        self.image = image
        self.ultimatebullet = False
        self.barrier_width = image.get_width()
        self.barrier_height = image.get_height()
    def set_position(self,xpos,ypos):
        self.x = xpos
        self.y = ypos
    def render(self):
        screen.blit(self.image,(self.x,self.y))        
    def move(self,direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        elif direction == "right" and self.x < screen_width-self.barrier_width:
            self.x += self.speed

def Titlescreen():
    exittitle = False
    image = pygame.image.load("TITLE.bmp").convert_alpha()
    clock = pygame.time.Clock()    
    while not exittitle:
        pygame.init()
        screen.fill((0,0,0))          
        screen.blit(image,(0,0))
        clock.tick(60)   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:     
                if event.key == pygame.K_z:
                    exittitle = True
                if event.key == pygame.K_q:
                    sys.exit()
        pygame.display.update()                            
        
def Gameover():
    startgame = False
    image = pygame.image.load("gameover.bmp").convert_alpha()
    clock = pygame.time.Clock()    
    while not startgame:
        pygame.init()
        screen.fill((0,0,0))          
        screen.blit(image,(0,0))
        clock.tick(60)   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:     
                if event.key == pygame.K_r:
                    startgame = True
                if event.key == pygame.K_q:
                    sys.exit()
        pygame.display.update()              
  
        
def Pause():
    image = pygame.image.load("pause.bmp").convert_alpha()
    startgame = False
    clock = pygame.time.Clock()    
    while not startgame:
        pygame.init()
        screen.blit(image,(0,0))
        clock.tick(60)        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:     
                if event.key == pygame.K_r:
                    startgame = True
                    main()
                if event.key == pygame.K_SPACE:
                    startgame = True
        pygame.display.update()      

def Win():
    image = pygame.image.load("win.bmp").convert_alpha()
    startgame = False
    clock = pygame.time.Clock()    
    while not startgame:
        pygame.init()
        screen.blit(image,(0,0))
        clock.tick(60)        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:     
                if event.key == pygame.K_z:
                    startgame = True
                if event.key == pygame.K_q:
                    sys.exit()
        pygame.display.update()      




def main():    
    #Game picture
    pygame.init()
    clock = pygame.time.Clock()
    enemies = []
    x = 0
    y = 0
    global win_number
    #add enemy
    boss = None
    if win_number <3:
        for column in range(1):
            for count in range(1):
                enemies.append(Enemy(50*x + 50,50*y + 50,pygame.image.load("enemy.bmp").convert_alpha()))
                x += 1
            x = 0
            y += 1



    #create new object
    player =  Player(304,448,pygame.image.load("spaceship.bmp").convert_alpha())
    barrier = Barrier(304,428,pygame.image.load("barrier.bmp").convert_alpha())
    boss = Boss(304,150,pygame.image.load("boss.bmp").convert_alpha())


    #Key
    press_z = False
    press_right = False
    press_left = False
    press_a = False
    press_c = False
    press_d = False
    pressed_r = False
    pressed_space = False        
    #Gamestart here
    while True:
        clock.tick(60)
        screen.fill((0,0,0))
        #create enemy        

        #enemy action
        for count in range(len(enemies)):
            enemies[count].render()
            enemies[count].x += enemies[count].speed
            
            #enemy move right
            if enemies[count].x > screen_width-enemies[0].enemy_width: 
                for count1 in range(len(enemies)):
                    enemies[count1].y += 5
                enemies[count].speed = -3
                break
            
            #enemy move left
            if enemies[count].x < 0:
                for count1 in range(len(enemies)):
                    enemies[count1].y += 5
                enemies[count].speed = +3
                break
            
            #random if enemy have to shoot or not
            rand = random.randint(0,100)            
            if rand < 5:
                if len(enemies[count].bullets) < 1:
                    enemies[count].bullets.append(Bullet(enemies[count].x+enemies[0].enemy_width/2,\
                    enemies[count].y,pygame.image.load("enemybullet.bmp").convert_alpha()))
            
            #enemy bullet move
            if len(enemies[count].bullets) > 0:
                enemies[count].bullets[0].y += 3
                
            #Check if enemy bullet hit barrier    
            if len(enemies[count].bullets) > 0:
                if enemies[count].bullets[0].checkcollide(barrier.x,barrier.y):
                    barrier.health -= 1
                    del enemies[count].bullets[0]
                    if barrier.health == 0:
                        barrier.ultimatebullet = True            
        
            #Check if enemy bullet hit player
            if len(enemies[count].bullets) > 0:
                if enemies[count].bullets[0].checkcollide(player.x,player.y):
                    player.health = 1
                    del enemies[count].bullets[0]
                    if player.health == 0:
                            Gameover()
                            main()
     
            #Check if player bullet hit enemy
            if len(player.bullets)>0:
                if player.bullets[0].checkcollide(enemies[count].x,enemies[count].y):
                        del enemies[count]
                        del player.bullets[0]
                        break
            
            #Check if barrier bullet hit enemy
            if len(barrier.bullet)>0:
                if barrier.bullet[0].checkcollide(enemies[count].x,enemies[count].y):
                    del enemies[count]
                    break
           
            #Check enemy bullet outofscreen
            if len(enemies[count].bullets) > 0:
                if enemies[count].bullets[0].outofscreen():
                    del enemies[count].bullets[0]    
           
            #render enemy bullet
            if len(enemies[count].bullets) > 0:
                enemies[count].bullets[0].render()
###########################################################################################

        #player bullet move
        for count in range(len(player.bullets)):
             if player.bullets[count].y <screen_width and player.bullets[count].y > 0:
                player.bullets[count].render()
                player.bullets[count].y -= 5
        
        #barrier bullet move
        if len(barrier.bullet) > 0:
            if barrier.bullet[0].y <screen_width and barrier.bullet[0].y > 0:
                barrier.bullet[0].render()
                barrier.bullet[0].y -= 2
                                
        #Check player bullet out of screen
        if len(player.bullets)>0:
            if player.bullets[0].outofscreen():
                del player.bullets[0]
        
        #Check barrier bullet out of screen
        if len(barrier.bullet)>0:
            if barrier.bullet[0].outofscreen():
                del barrier.bullet[0]
                
        #Check if missile hit boss
        if win_number>3:
            if len(player.bullets)>0:
                if player.bullets[0].checkcollideboss(boss.x,boss.y):
                    boss.health -= 1
                    del player.bullets[0]

        #Check number of enemy if none You win
        if len(enemies) == 0:
            win_number += 1
            if win_number < 3:
                main()


        #Key event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    press_d = True
                if event.key == pygame.K_a:                    
                    press_a = True                
              #  if event.key == pygame.K_z:
                if board.getSwitch == False :
		    player_missile.x = player.x
                    player_missile.y = player.y
                if event.key == pygame.K_SPACE:                    
                    Pause()
                    press_z = False
                    press_right = False
                    press_left = False
                    press_a = False
                    press_d = False
                    pressed_r = False
                    pressed_space = False                         

                                                                  
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    press_right = False
                if event.key == pygame.K_LEFT:                    
                    press_left = False
                if event.key == pygame.K_d:
                    press_d = False
                if event.key == pygame.K_a:                    
                    press_a = False
                if event.key == pygame.K_SPACE:                    
                    press_space = False
                    
        if board.getLight()>(maxLight+minLight)/2 and player.x < screen_width - player.player_width:
            player.x += 5
        if board.getLight()<=(maxLight+minLight)/2 and player.x>0:
            player.x -= 5
        if press_d:
            barrier.move("right")
        if press_a:
            barrier.move("left")
        
        #Barrier bullet move
        if len(barrier.bullet) >0:
            if press_d:
                barrier.bullet[0].move("right")                           
            if press_a:
                barrier.bullet[0].move("left")
           
        player.render()
        #Render barrier
        if barrier.health >= 0:
            barrier.render()
  
        #Render barrier bullet
        if barrier.ultimatebullet and press_c:
            barrier.bullet.append(Bullet(barrier.x+barrier.barrier_width/2,barrier.y-10,pygame.image.load("ultimate.bmp").convert_alpha()))
            barrier.y = -10

        #Render boss
        if win_number>3:
            if boss.health>0:
                boss.render()
            else:
                win_number = 0
                Win()
        
        pygame.display.update()
        pygame.time.delay(5)          
        
if __name__ == "__main__":
    Titlescreen()
    main()
        
            
