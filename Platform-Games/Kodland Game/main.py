import pgzrun
from pgzero.builtins import Actor, keyboard, Rect
import time
import random

WIDTH = 600
HEIGHT = 300
FPS = 30

play_button = Actor("oyna.jpg", (300, 100))  
sound_button = Actor("sound_open", (580, 25))  
exit_button = Actor("oyna.jpg", (300, 150))  
background = Actor("background.jpg")
karakter = Actor("stand", (50,200))
#dusman_1 = Actor("animateright_0", (650,200))



sound_on = True
mod = "menu"
puan = 0
footstep_timer = 0  
bomb_timer = 0
bomb_duraction = 1
heart_timer = 0
heart_duratcion = 1
footstep_duration = 0.25  
swords = []
bombs = []
enemys = []
hearts = []
explosion_frames = [
    "animateright_1",
    "animateright_2",
    "animateright_3",
    "animateright_4",
    "animateright_5",
    
]
explosions = []

class Explosion(Actor):
    def __init__(self, position):
        super().__init__("animateright_0", position)
        self.frame = 0
        self.animation_speed = 0.6

    def update(self):
        self.frame += self.animation_speed
        if self.frame >= len(explosion_frames):
            self.frame = 0
            explosions.remove(self)
        self.image = explosion_frames[int(self.frame)]

class Bomb(Actor):
    def __init__(self, image, position, speed):
        super().__init__(image, position)
        self.speed = speed

    def move(self):
        if self.y < HEIGHT:
            self.y += self.speed
        

class Enemy(Actor):
    def __init__(self, image, position, speed):
        super().__init__(image, position)
        self.speed = speed

    def move(self):
        if self.x > -20:
            self.x -= self.speed
        else:
            self.reset_position()

    def reset_position(self):
        self.y = 200
        self.x = random.randint(600, 900)
        self.speed = random.randint(1, 3)
    

class Heart(Actor):
    def __init__(self, image, position, speed):
        super().__init__(image, position)
        self.speed = speed

    def move(self):
        if self.y < HEIGHT:
            self.y += self.speed
        else:
            self.reset_position()
            

    def reset_position(self):
        self.y = random.randint(-450, -50)
        self.x = random.randint(0, WIDTH)
        self.speed = random.randint(2, 5)
        


def create_bombs(count):
    for _ in range(count):
        x = random.randint(0, WIDTH)
        y = random.randint(-450, -50)
        speed = random.randint(2, 8)
        bombs.append(Bomb("bomb", (x, y), speed))
def create_enemys(count):
    for _ in range(count):
        x = random.randint(600, 900)
        y = 200
        speed = random.randint(1,3)
        enemys.append(Enemy("animateright_0", (x, y), speed))

def create_hearts(count):
    for _ in range(count):
        x = random.randint(0, WIDTH)
        y = random.randint(-450, -50)
        speed = random.randint(2, 10)
        hearts.append(Heart("heart", (x, y), speed))
    

def move_enemy_bomb():
    for bomb in bombs[:]:
        bomb.move()

def move_enemy():
    for enemy in enemys[:]:
        enemy.move()
def move_heart():
    for heart in hearts[:]:
        heart.move()


def draw():
    if mod == "menu":
        background.draw()
        play_button.draw()
        screen.draw.text("Game", center=(300,100), color="white", fontsize=36)
        sound_button.draw()
        exit_button.draw()
        screen.draw.text("Exit", center=(300,150), color="white", fontsize=36)
    elif mod == "game":
        background.draw()
        screen.draw.text("Puan: {}".format(puan), center=(20, 20), color="red", fontsize=36)
        for i in range(len(swords)):
            swords[i].draw()
        for i in range(len(bombs)):
            bombs[i].draw()
        for i in range(len(hearts)):
            hearts[i].draw()
        for i in range(len(enemys)):
            enemys[i].draw()
        for explosion in explosions:
            explosion.draw()
        karakter.draw()
        #dusman_1.draw()
        
        sound_button.draw()
    elif mod == "and":
        background.draw()
        screen.draw.text("Oyun Bitti", center=(300,150), color="red", fontsize=36)
    elif mod == "win":
        background.draw()
        screen.draw.text("KAZANDINIZ :)", center=(300,150), color="red", fontsize=36)

def sword_move():
    
    for i in range(len(swords)):
        if swords[i].x >= karakter.x:
            swords[i].x += 5
            swords[i].image = "swordright"
    
        



def collisions():
    global mod
    for enemy in enemys[:]:
        if karakter.colliderect(enemy): 
            enemys.remove(enemy)
            create_enemys(1)
            mod = "and"

        for sword in swords[:]:
            if sword.colliderect(enemy):
               
                enemys.remove(enemy)
                swords.remove(sword)
                create_enemys(1)

                explosion = Explosion(enemy.pos)
                explosions.append(explosion)
                break
     
def combat_bomb():
    global mod
    for i in range(len(bombs)):
        if karakter.colliderect(bombs[i]):
            play_bombs_sound()
            mod = "and"
def combat_heart():
    global mod
    global puan
    for i in range(len(hearts)):
        if karakter.colliderect(hearts[i]):
            play_hearts_sound()
            hearts.pop(i)
            create_hearts(1)
            puan += 1
            break
            
def idle_animation():
    if mod == "game" and karakter.image == "stand":
        animate(karakter, tween="bounce_end", duration=0.5, y=karakter.y - 10) 
        clock.schedule_unique(lambda: animate(karakter, tween="bounce_end", duration=0.5, y=karakter.y + 10), 0.5)  


def update(dt):
    clock.schedule_interval(idle_animation, 1)
    karakter.y = 200
    global footstep_timer  
    global bomb_timer
    global mod 
    if mod == "game":
        if puan >= 5:
            move_enemy_bomb()
        if puan == 10:
            mod = "win"
        sword_move()
        combat_bomb()
        move_heart()
        move_enemy()
        combat_heart()
        collisions()
        # animate_move_1()
        #combat_animate()        
        
        if (keyboard.left or keyboard.a) and karakter.x > 0:
            karakter.x -= 5
            karakter.image = "left"
            play_footstep_sound()
        elif (keyboard.right or keyboard.d):
            karakter.x += 5
            karakter.image = "right"
            play_footstep_sound()
        elif keyboard.down or keyboard.s:
            karakter.image = "duck"
        elif keyboard.up or keyboard.space or keyboard.w :
            karakter.y = 120
            animate(karakter, tween="bounce_end", duration=1, y=200) 
        else:
            karakter.image = "stand"
            sounds.grass.stop()

    
        if footstep_timer > 0 and time.time() - footstep_timer >= footstep_duration:
            sounds.grass.stop()
            footstep_timer = 0
        for explosion in explosions:
            explosion.update()
        
        #if karakter.colliderect(dusman_1) :
        #   mod = "and"



def play_footstep_sound():
    global footstep_timer
    if footstep_timer == 0:  
        sounds.grass.play()
        footstep_timer = time.time()  
def play_bombs_sound():
    global bomb_timer
    if bomb_timer == 0:  
        sounds.bombvoice.play()
        bomb_timer = time.time()  
def play_hearts_sound():
    global heart_timer
    if bomb_timer == 0:  
        sounds.heart.play()
        heart_timer = time.time()  

def on_mouse_down(button, pos):
    global sound_on
    global mod

    if button == mouse.LEFT and mod == "menu":
        if play_button.collidepoint(pos):
            mod = "game"
        elif sound_button.collidepoint(pos):
            sound_on = not sound_on
            if sound_on:
                sounds.birds.play(-1)
            else:
                sounds.birds.stop()
        elif exit_button.collidepoint(pos):
            exit()
    elif button == mouse.LEFT and mod == "game":
        sword = Actor("swordright")
        sword.pos = karakter.pos
        swords.append(sword)

        
        if pos[0] < karakter.x:  
            sword.image = "sword"
        else:  
            sword.image = "swordright"

        if sound_button.collidepoint(pos):
            sound_on = not sound_on
            if sound_on:
                sounds.birds.play(-1)
            else:
                sounds.birds.stop()

create_bombs(5)
create_hearts(5)
create_enemys(2)
pgzrun.go()