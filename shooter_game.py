from pygame import *
from random import randint
from time import time as timer


#Fonts
font.init()
font_2 = font.SysFont("Arial", 36)
font_1 = font.SysFont('Arial', 80)

Win = font_1.render('You Win!', True, (255, 255, 255))
Lose = font_1.render('You Lose!', True, (255, 255, 255))

score = 0
lose = 0
goal = 10
max_lose = 3

#In game music and sound effects:
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


class GameSprites(sprite.Sprite):
        #class constructor
   def __init__(self, player_image, player_x, player_y, player_size_x, player_size_y, player_speed):
       sprite.Sprite.__init__(self)
       #every sprite must store the image property
       self.image = transform.scale(image.load(player_image), (player_size_x, player_size_y))
       self.speed = player_speed
       #every sprite must have the rect property – the rectangle it is fitted in
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

   
   def reset(self):
       windows.blit(self.image, (self.rect.x, self.rect.y))


class player(GameSprites): #A command to control the rocket
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < Win_W - 80:
            self.rect.x += self.speed


    def fire(self): #A command to shoot from the rocket
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprites):
    #Enemy movement
    def update(self):
        self.rect.y += self.speed
        global lose
        #Enemy disappears upon reaching the window's edge
        if self.rect.y > Win_H:
            self.rect.x = randint(80, Win_W - 80)
            self.rect.y = 0
            lose = lose + 1


class Bullet(GameSprites):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



#Game scene:
Win_W = 700
Win_H = 500
windows = display.set_mode((Win_W, Win_H))

display.set_caption("Space Shooter")
background = transform.scale(image.load("galaxy.jpg"), (Win_W, Win_H))


rocket = player('rocket.png', 5, Win_H - 100, 80, 100, 10)
monsters = sprite.Group() #To group the monsters

for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, Win_W -80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()

for i in range(1, 3):
    asteroid = Enemy("asteroid.png", randint(80, Win_H - 80), -40, 80, 50, randint(1, 3))
    asteroids.add(asteroid)

bullets = sprite.Group()

#Variables list:
Finish = False #To determine wether the Finish stituation is true or not.
Start = True #To determine wether the Start stituation is true or not.
Num_Fire = 0
Rel_Time = False
life = 3


#Game loop:
while Start:
    for e in event.get():
        if e.type == QUIT:
            Start = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if Num_Fire < 5 and Rel_Time == False:
                    Num_Fire = Num_Fire + 1
                    fire_sound.play()
                    rocket.fire()

                if Num_Fire >= 5 and Rel_Time == False:
                    Last_Time = timer()
                    Rel_Time = True
                        


    if not Finish:
       windows.blit(background, (0, 0))

      

       rocket.update()
       monsters.update()
       bullets.update()
       asteroids.update()
       rocket.reset()
       monsters.draw(windows)
       bullets.draw(windows)
       asteroids.draw(windows)

       if Rel_Time == True:
           New_Time = timer()
           if New_Time - Last_Time < 3:
               Reload = font_2.render("Realoading!", 1, (150, 0, 0))
               windows.blit(Reload, (260, 460))

           else:
               Num_Fire = 0
               Rel_Time = False
               

       collide = sprite.groupcollide(monsters, bullets, True, True)
       for c in collide:
           score = score + 1 
           monster = Enemy('ufo.png', randint(80, Win_W - 80), -40, 60, 50, randint(1, 5))
           monsters.add(monster)
        
       if sprite.spritecollide(rocket, monsters, False) or sprite.spritecollide(rocket, asteroids, False):
           sprite.spritecollide(rocket, monsters, True)
           sprite.spritecollide(rocket, asteroids, True)
           life = life - 1
           
       if life == 0 or lose >= max_lose:
           Finish = True
           windows.blit(Lose, (200, 200))

       if score >= goal:
           Finish = True
           windows.blit(Win, (200, 200))

       text = font_2.render("Score: " + str(score), 1, (255, 255, 255)) 
       windows.blit(text, (10, 20))
       text_2 = font_2.render("Missed: " + str(lose), 1, (255, 255, 255))
       windows.blit(text_2, (10, 50))

       if life == 3:
           lifecolor = (0, 150, 0)

       if life == 2:
           lifecolor = (150, 150, 0)

       if life == 1:
           lifecolor = (150, 0, 0)

       text_life = font_1.render(str(life), 1, lifecolor)
       windows.blit(text_life, (650, 10))

       display.update()

    else:
        Finish = False
        score = 0
        lose = 0
        Num_Fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for e in range(1, 6):
            monster = Enemy("ufo.png", randint(80, Win_W -80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        for e in range(1, 3):
            asteroid = Enemy("asteroid.png", randint(80, Win_H - 80), -40, 80, 50, randint(1, 3))
            asteroids.add(asteroid)


    time.delay(50)