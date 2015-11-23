import pygame,sys,random
from pygame.locals import *

#constant of game
screen = pygame.display.set_mode((640,480))
screen_width = screen.get_width()
screen_height = screen.get_height()
win_number = 0
#class of object in the game
class Boss:
    def __init__(self,xpos,ypos,image):
        self.health = 30
        self.x = xpos
        self.y = ypos
        self.cooldown = 500    
        self.speed = 100
        self.last = pygame.time.get_ticks()
        self.image = image
        self.bullets = []
        self.boss_width = image.get_width()
        self.boss_height = image.get_height()
    def render(self):
        screen.blit(self.image,(self.x,self.y))
    def move(self,direction):
        if direction == "left" and self.x > 30:
            self.x -= self.speed
        elif direction == "right" and self.x < 450:
            self.x += self.speed
        elif direction == "up" and self.y > self.boss_height:
            self.y -= self.speed
        elif direction == "down" and self.y < 250:
            self.y += self.speed
    def checkcooldown(self,time):
        if time - self.last >= self.cooldown:
            self.last = time
            return True
        return False
            
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
    def checkcollide(self,x1,x2,x3,x4):
        if(self.x >= x1 and self.x <= x1+x2 and self.y >= x3 and self.y <= x3+x4):
            return True
        return False
    def outofscreen(self):
        if self.y < 0 or self.y > screen_height:
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
    boss = Boss(304,50,pygame.image.load("boss.bmp").convert_alpha())


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
                if enemies[count].bullets[0].checkcollide(barrier.x,barrier.barrier_width,barrier.y,barrier.barrier_height):
                    barrier.health -= 1
                    del enemies[count].bullets[0]
                    if barrier.health == 0:
                        barrier.ultimatebullet = True            
        
            #Check if enemy bullet hit player
            if len(enemies[count].bullets) > 0:
                if enemies[count].bullets[0].checkcollide(player.x,player.player_width,player.y,player.player_height):
                    player.health -= 1
                    del enemies[count].bullets[0]
                    if player.health < 0:
                            Gameover()
                            main()
     
            #Check if player bullet hit enemy
            if len(player.bullets)>0:
                if player.bullets[0].checkcollide(enemies[count].x,enemies[0].enemy_width,enemies[count].y,enemies[0].enemy_height):
                        del enemies[count]
                        del player.bullets[0]
                        break
            
            #Check if barrier bullet hit enemy
            if len(barrier.bullet)>0:
                if barrier.bullet[0].checkcollide(enemies[count].x,enemies[0].enemy_width,enemies[count].y,enemies[0].enemy_height):
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
                


        #Check number of enemy if none You win
        if len(enemies) == 0:
            win_number += 1
            if win_number < 3:
                main()

        #Boss Action
        if win_number>3:
            now = pygame.time.get_ticks()
            randbossaction = random.randint(0,100)     
            #Check if missile hit boss
            if randbossaction < 4 :
                if randbossaction == 0 and boss.checkcooldown(now):
                    boss.move("up")
                elif randbossaction == 1 and boss.checkcooldown(now):
                    boss.move("down")
                elif randbossaction == 2 and boss.checkcooldown(now):
                    boss.move("left")
                elif randbossaction == 3 and boss.checkcooldown(now):
                    boss.move("right")
            elif randbossaction <= 100:
                if boss.checkcooldown(now) and len(boss.bullets) < 3:
                    boss.bullets.append(Bullet(250 ,boss.y,pygame.image.load("bossbullet.bmp").convert_alpha()))

            for count in range(len(boss.bullets)):
                 if boss.bullets[count].y <screen_width and boss.bullets[count].y > 0:
                    boss.bullets[count].render()
                    boss.bullets[count].y += 10           

            if len(player.bullets)>0:
                if player.bullets[0].checkcollide(boss.x,boss.boss_width,boss.y,boss.boss_height):
                    boss.health -= 1
                    del player.bullets[0]

            if len(boss.bullets) > 0:
                if boss.bullets[0].checkcollide(barrier.x,barrier.barrier_width,barrier.y,barrier.barrier_height):
                    barrier.health -= 2
                    del boss.bullets[0]
                    if barrier.health <= 0:
                        barrier.ultimatebullet = True      
                if boss.bullets[0].checkcollide(player.x,player.player_width,player.y,player.player_height):
                    player.health -= 2
                    del boss.bullets[0]
                    if player.health <= 0:
                        Gameover()
                        main()
                if boss.bullets[0].outofscreen():
                    del boss.bullets[0]                        
       


                        
                    

            
            
            

        #Key event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    press_right = True
                if event.key == pygame.K_LEFT:                    
                    press_left = True
                if event.key == pygame.K_d:
                    press_d = True
                if event.key == pygame.K_a:                    
                    press_a = True
                if event.key == pygame.K_c:                    
                    press_c = True    
                if event.key == pygame.K_z:
                    if(len(player.bullets)!=100):
                        player.bullets.append(Bullet(player.x+player.player_width/2,player.y,pygame.image.load("bullet.bmp").convert_alpha()))
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
                    
        if press_right:
            player.move("right")
        if press_left:
            player.move("left")
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
            barrier.y = -100

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
        
            
