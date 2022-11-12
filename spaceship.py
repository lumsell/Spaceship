import pygame, random, sys, math, copy, sys
#import screen_object.py
from pygame.locals import *

pygame.init()
icon = pygame.image.load("sprites/buttons/planet_geolyte.png")
icon.set_colorkey((255,0,255))
pygame.display.set_icon(icon)
screenx = 400 # width of screen
screeny = 600 # height of screen
screen = pygame.display.set_mode((screenx, screeny)) 
mainfont = pygame.font.SysFont("monospace", 15)
bigfont = pygame.font.SysFont("monospace", 40) #Two fonts
painFlash = pygame.image.load('sprites/damage.png') #Image shown when taking damage
hardmode = False


tick_counter = 0

#===================================================|GAME ENTITIES|==========================================================

#Collision detection.
def colDet(source, target):
    try:
        if source.x < target.x + target.w and source.x + source.w > target.x:
            if source.y < target.y + target.h and source.h + source.y > target.y:
                return True
        else:
            return False
    except:
        return False

def enemySpawn(enemy, x):
    world.enemylist.append(copy.copy(enemy()))
    world.enemylist[len(world.enemylist)-1].x = x

class Entity(object):
    def __init__(self):
        None
        
#This class takes the level lists and spawns enemies at the specified y-position.
class Level(Entity):
    def __init__(self, levellist, bgc = (0,0,0)):
        self.planet = None
        self.queue = levellist
        self.bgc = bgc
        self.pos = 1
        self.nextspawn = (5*60)
        self.current = []
        self.finished = False

    def tick(self):
        if len(world.enemylist) == 0 and (self.nextspawn - 105) > tick_counter:
            self.nextspawn = tick_counter + 105
        if hardmode and self.nextspawn > tick_counter + 180:
            self.nextspawn = tick_counter + 180
        if self.nextspawn < tick_counter:
            if len(self.queue) > self.pos:
                self.current = self.queue[self.pos]
                self.spawn()
            elif len(world.enemylist) == 0:
                global scrap
                global reward
                if self.finished == False:
                    scrap = scrap + reward
                self.finished = True
                label = bigfont.render("MISSION COMPLETE", 1, (255,255,0))
                screen.blit(label, (-1,256))
                label = mainfont.render("YOU HAVE EARNED ϕ"+str(reward), 1, (255,255,0))
                screen.blit(label, (-1,300))
                self.planet.completed = True
                self.planet.spoils = 0
                

    def spawn(self):
        enemySpawn(self.current[0],self.current[1]*4)
        self.pos = self.pos + 1
        self.nextspawn = tick_counter + (self.current[2]*60)
                   
        
#Holds every entity in gameplay and runs the tick function of all of them in gameplay
class World(Entity):
    def __init__(self):
        self.playerlist = []
        self.enemylist = []
        self.misclist = []
        self.bulletlist = []
        self.levellist = None
        self.score = 0

    def tick(self):
        for x in reversed(self.enemylist):
            x.tick()
        for x in reversed(self.playerlist):
            x.tick()
        for x in reversed(self.bulletlist):
            x.tick()
        for x in reversed(self.misclist):
            x.tick()
        self.levellist.tick()
        self.scorebar = mainfont.render(str(self.score), 1, (255,255,255))
        screen.blit(self.scorebar, (256,0))

#Holds every entity in menus
class Menu(Entity):
    def __init__(self):
        self.layer1 = []
        self.layer2 = []
        self.layer3 = []
        self.layer4 = []
        self.misclist = []

# the class for any visible item.
class ScreenObject(Entity):
    def __init__(self, imageFileName, screen):
        super().__init__()
        self.image = pygame.image.load(imageFileName)
        #loads the sprite into memory
        self.image = self.image.convert()
        self.image.set_colorkey((255,0,255))
        #sprites have magenta backgrounds that are removed by colorkey
        self.x = 0
        self.y = 0
        #x and y position.
        self.xoffset = 0
        self.yoffset = 0
        #offset is used to have the sprite render in a different position to the object origin.
        #mainly for things that have hitboxes.
        
        ###self.imagePos = (self.x, self.y)
        self.screen = screen
        
        self.xVelocity = 0
        self.yVelocity = 0

    #The tick function in every class is called every frame. Get used to seeing it a lot.
    def tick(self):
        self.move()

    #Moves an object by x & y velocity
    def move(self):
        self.x = self.x + self.xVelocity
        self.y = self.y + self.yVelocity
        self.screen.blit(self.image, (self.x + self.xoffset, self.y + self.yoffset))

class LineObject(object):
    def __init__(self, colour, start, end, width):
        self.colour = colour
        self.start = start
        self.end = end
        self.width = width
        self.birthday = tick_counter
        self.lifetime = 3
        
    def tick(self):
        pygame.draw.line(screen, self.colour, self.start, self.end, self.width)
        if tick_counter > self.birthday + self.lifetime:
            self.die()

    def die(self):
        world.misclist.remove(self)

#Draws a font on the screen. Used, like, once? 
class TextObject(Entity):
    def __init__(self, text, rgb, screen):
        super().__init__()
        self.text = text
        self.colour = rgb 
        self.x = 0
        self.y = 0
        self.screen = screen
        
        #self.xVelocity = 0
        #self.yVelocity = 0

    def tick(self):
        self.render()

    def render(self):
        #self.x = self.x + self.xVelocity
        #self.y = self.y + self.yVelocity
        
        label = mainfont.render(text, 1, colour)
        self.screen.blit(label, (self.x + self.xoffset, self.y))

#"We have nothing to fear but fear itself"

#These are the bracket graphics used for button mouseovers
ul_br = pygame.image.load("sprites/buttons/bracket_ul.png")
ul_br = ul_br.convert()
ul_br.set_colorkey((255,0,255))
ur_br = pygame.image.load("sprites/buttons/bracket_ur.png")
ur_br = ur_br.convert()
ur_br.set_colorkey((255,0,255))
bl_br = pygame.image.load("sprites/buttons/bracket_bl.png")
bl_br = bl_br.convert()
bl_br.set_colorkey((255,0,255))
br_br = pygame.image.load("sprites/buttons/bracket_br.png")
br_br = br_br.convert()
br_br.set_colorkey((255,0,255))

#A button you can click with the mouse
class Button(ScreenObject):
    def __init__(self, imageFileName, screen, height=32, width=64):
        super().__init__(imageFileName, screen)
        self.h = height
        self.w = width
        self.pressed = False

    def tick(self):
        super().tick()
        #This resets the pressed state if the button isn't being pressed anymore.
        self.pressed = False
        tup = pygame.mouse.get_pos
        #draws brackets around buttons you mouseover
        if tup(0)[0] > self.x and tup(0)[0] < self.x+self.w and tup(0)[1] > self.y and tup(0)[1] < self.y+self.h:
            self.screen.blit(ul_br, (self.x, self.y))
            self.screen.blit(ur_br, (self.x+self.w-11, self.y))
            self.screen.blit(bl_br, (self.x, self.y+self.h-11))
            self.screen.blit(br_br, (self.x+self.w-11, self.y+self.h-11))
        if pygame.mouse.get_pressed()[0]:
            #checks collision with the mouse cursor
            if tup(0)[0] > self.x and tup(0)[0] < self.x+self.w and tup(0)[1] > self.y and tup(0)[1] < self.y+self.h:
             
                self.pressed = True
    

#============================================================================================================#


#Objects that cycle through multiple sprites
class Effect(ScreenObject):
    def __init__(self, imageFileList, screen):
        super().__init__(imageFileList[0], screen)
        self.imageFileList = imageFileList #list of sprites for animation
        self.cycle = 0 #position of the current sprite in the animation

    def tick(self):
        super().tick()
        self.cycle = self.cycle + 1
        if self.cycle >= len(self.imageFileList): #if out of sprites to cycle through
            self.die() 
        else:
            self.imageFileName = self.imageFileList[self.cycle]
            self.image = pygame.image.load(self.imageFileName) 
            self.image = self.image.convert()
            self.image.set_colorkey((255,0,255))
            #Loads the next sprite in the animation

    def die(self):
        world.misclist.remove(self)

#A screen object that can be collided with
class TangibleObject(ScreenObject):
    def __init__(self, imageFileName, screen, height=0, width=0):
        super().__init__(imageFileName, screen)
        self.h = height
        self.w = width
    
    def tick(self):
        super().tick()


#Bad guy class
class EnemyShip(TangibleObject):
    def __init__(self, imageFileName, screen, height=26, width=26):
        super().__init__(imageFileName, screen, height, width)
        self.yVelocity = 1
        self.firerate = 60 #Rate of fire, in frames
        self.lastshotfired = random.randint(-5,0) #Time of the last shot
        #self.bullet = None
        self.health = 10 
        self.y = -32 #Default starting position
        self.punchrate = 2
        #Rate of collision bumping. Unused, except for bosses.
        self.lastpunch = 0

    def tick(self):
        super().tick()
        self.shoot()
        if self.y > screeny: #if ofscreen
            self.y = -1*self.h - 10 - 20*self.yVelocity #Loop back to top of screen
            self.jumpParticle()
            
        #if self.punchrate + self.lastpunch < tick_counter:
        #    for i in world.playerlist:
        #        if colDet(self,i):
        #            dist = math.sqrt((self.x - i.x)**2 + (self.y - i.y)**2)
        #            i.xVelocity = (3/dist)*(i.x - self.x)
        #            i.yVelocity = (3/dist)*(i.y - self.y)
        #            self.lastpunch = tick_counter
            
    #Used when a ship 'talks shit'/takes damage
    def getHit(self, damage):
        self.health = self.health - damage
    
        if self.health < 1:
            self.die()

    def jumpParticle(self):
        for i in range(20):
            world.misclist.append(Effect(["sprites/generic.png" for j in range(i//2)]+
                                        ["sprites/effects/shine_01.png",
                                          "sprites/effects/shine_02.png",
                                          "sprites/effects/shine_03.png",
                                          "sprites/effects/shine_04.png",
                                          "sprites/effects/shine_05.png",
                                          "sprites/effects/shine_06.png",
                                          "sprites/effects/shine_07.png",]
                                        , screen))
            world.misclist[-1].x = self.x + 5
            world.misclist[-1].y = 580 - i*30

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            #Makes a bullet
            world.bulletlist.append(Bullet("devpulse.png", screen, 8, 8, False))
            #Alters the properties of the most recent bullet
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 8 
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 10
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 6
            world.bulletlist[len(world.bulletlist)-1].damage = 10
            self.lastshotfired = tick_counter

    def die(self):
        world.score = world.score + 1
        #Wicked nasty explosion animation
        world.misclist.append(Effect(["sprites/effects/explosion_small_01.png",
                                      "sprites/effects/explosion_small_02.png",
                                      "sprites/effects/explosion_small_03.png",
                                      "sprites/effects/explosion_small_04.png",
                                      "sprites/effects/explosion_small_05.png",
                                      "sprites/effects/explosion_small_06.png",
                                      "sprites/effects/explosion_small_07.png",
                                      "sprites/effects/explosion_small_08.png",
                                      "sprites/effects/explosion_small_09.png",
                                      "sprites/effects/explosion_small_10.png",
                                      "sprites/effects/explosion_small_11.png",
                                      "sprites/effects/explosion_small_12.png",
                                      "sprites/effects/explosion_small_13.png",
                                      ],screen))
        world.misclist[-1].x = self.x -14 
        world.misclist[-1].y = self.y -4
        world.enemylist.remove(self)

class collisionBox(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

def copyBullets(bullet, poslist, spdlist):
    for i in range(len(poslist)):
        world.bulletlist.append(copy.copy(bullet))
        world.bulletlist[len(world.bulletlist)-1].x = poslist[i][0]
        world.bulletlist[len(world.bulletlist)-1].y = poslist[i][1]
        world.bulletlist[len(world.bulletlist)-1].xVelocity = spdlist[i][0]
        world.bulletlist[len(world.bulletlist)-1].yVelocity = spdlist[i][1]
        
######################################
#damagemod, fireratemod and shotspeedmod are all modifiers to attacks gained from upgrades
        
#The boring gun. Fires bullets at a normal rate with pretty good damage
def weapon_generic(player, damagemod, fireratemod, shotspeedmod):
    if tick_counter - 15*fireratemod >  player.lastshotfired:
        world.bulletlist.append(Bullet("sprites/bullet/whitelaser.png", screen, 16, 8, True))
        world.bulletlist[-1].x = player.x + random.randint(3,4)
        world.bulletlist[-1].y = player.y - 8
        world.bulletlist[-1].yVelocity = -12*shotspeedmod
        world.bulletlist[-1].damage = 4*damagemod
        world.bulletlist[-1].hit_effect = ["sprites/effects/laserhit_big_01.png",
                                                                "sprites/effects/laserhit_big_02.png",
                                                                "sprites/effects/laserhit_big_03.png",
                                                                "sprites/effects/laserhit_big_04.png",
                                                                "sprites/effects/laserhit_big_05.png",
                                                                "sprites/effects/laserhit_big_06.png"]
        player.lastshotfired = tick_counter

#High fire rate, low damage
def weapon_gatling(player, damagemod, fireratemod, shotspeedmod):
    if tick_counter - 3*fireratemod >  player.lastshotfired:
        world.bulletlist.append(Bullet("sprites/bullet/devlaser.png", screen, 16, 4, True))
        world.bulletlist[-1].x = player.x + random.randint(-2,10)
        world.bulletlist[-1].y = player.y - 8
        world.bulletlist[-1].yVelocity = -12*shotspeedmod
        world.bulletlist[-1].damage = 1*damagemod
        player.lastshotfired = tick_counter

#Low fire rate and shot speed, high damage
def weapon_missile(player, damagemod, fireratemod, shotspeedmod):
    if tick_counter - 60*fireratemod >  player.lastshotfired:
        world.bulletlist.append(Rocket("sprites/bullet/friendrocket.png", screen, 16, 8))
        world.bulletlist[-1].x = player.x + 2
        world.bulletlist[-1].y = player.y - 16
        world.bulletlist[-1].w = 10
        world.bulletlist[-1].yVelocity = -5*shotspeedmod
        world.bulletlist[-1].damage = round(15*damagemod)
        world.bulletlist[-1].lifetime = 300
        world.bulletlist[-1].radius = 60
        world.bulletlist[-1].hit_effect = ["sprites/effects/wee_devsplode.png",
                                                                "sprites/effects/wee_devsplode.png",
                                                                "sprites/effects/wee_devsplode.png",]
        world.bulletlist[len(world.bulletlist)-1].offset = 44
        player.lastshotfired = tick_counter

#Fires four shots with spread
def weapon_shotgun(player, damagemod, fireratemod, shotspeedmod):
    if tick_counter - 35*fireratemod >  player.lastshotfired:
        world.bulletlist.append(TrailingBullet("sprites/generic.png", screen, 16, 4, True))
        world.bulletlist[len(world.bulletlist)-1].x = player.x + 1
        world.bulletlist[len(world.bulletlist)-1].y = player.y - 8
        world.bulletlist[len(world.bulletlist)-1].xVelocity = -3*shotspeedmod
        world.bulletlist[len(world.bulletlist)-1].yVelocity = -12*shotspeedmod
        world.bulletlist[len(world.bulletlist)-1].damage = 2*damagemod
        world.bulletlist[len(world.bulletlist)-1].effect = ["sprites/effects/splashlaser_01.png",
                                                            "sprites/effects/splashlaser_02.png",
                                                            "sprites/effects/splashlaser_03.png",
                                                            "sprites/effects/splashlaser_04.png",
                                                            ]
        world.bulletlist.append(TrailingBullet("sprites/generic.png", screen, 16, 4, True))
        world.bulletlist[len(world.bulletlist)-1].x = player.x + 1
        world.bulletlist[len(world.bulletlist)-1].y = player.y - 8
        world.bulletlist[len(world.bulletlist)-1].xVelocity = -1*shotspeedmod
        world.bulletlist[len(world.bulletlist)-1].yVelocity = -12*shotspeedmod
        world.bulletlist[len(world.bulletlist)-1].damage = 2*damagemod
        world.bulletlist[len(world.bulletlist)-1].effect = ["sprites/effects/splashlaser_01.png",
                                                            "sprites/effects/splashlaser_02.png",
                                                            "sprites/effects/splashlaser_03.png",
                                                            "sprites/effects/splashlaser_04.png",
                                                            ]
        world.bulletlist.append(TrailingBullet("sprites/generic.png", screen, 16, 4, True))
        world.bulletlist[len(world.bulletlist)-1].x = player.x + 1
        world.bulletlist[len(world.bulletlist)-1].y = player.y - 8
        world.bulletlist[len(world.bulletlist)-1].xVelocity = 1*shotspeedmod
        world.bulletlist[len(world.bulletlist)-1].yVelocity = -12*shotspeedmod
        world.bulletlist[len(world.bulletlist)-1].damage = 2*damagemod
        world.bulletlist[len(world.bulletlist)-1].effect = ["sprites/effects/splashlaser_01.png",
                                                            "sprites/effects/splashlaser_02.png",
                                                            "sprites/effects/splashlaser_03.png",
                                                            "sprites/effects/splashlaser_04.png",
                                                            ]
        world.bulletlist.append(TrailingBullet("sprites/generic.png", screen, 16, 4, True))
        world.bulletlist[len(world.bulletlist)-1].x = player.x + 1
        world.bulletlist[len(world.bulletlist)-1].y = player.y - 8
        world.bulletlist[len(world.bulletlist)-1].xVelocity = 3*shotspeedmod
        world.bulletlist[len(world.bulletlist)-1].yVelocity = -12*shotspeedmod
        world.bulletlist[len(world.bulletlist)-1].damage = 2*damagemod
        world.bulletlist[len(world.bulletlist)-1].effect = ["sprites/effects/splashlaser_01.png",
                                                            "sprites/effects/splashlaser_02.png",
                                                            "sprites/effects/splashlaser_03.png",
                                                            "sprites/effects/splashlaser_04.png",
                                                            ]
        player.lastshotfired = tick_counter

#Test weapon. Unused. 
def weapon_orbiter(player, damagemod, fireratemod, shotspeedmod):
    if tick_counter - 1*fireratemod >  player.lastshotfired:
        world.bulletlist.append(OrbitingBullet("sprites/bullet/redpulse.png", screen, 16, 8, True))
        world.bulletlist[-1].x = player.x  
        world.bulletlist[-1].y = player.y - 24
        world.bulletlist[-1].xtarget = player.x + 3
        world.bulletlist[-1].ytarget = player.y - 24
        world.bulletlist[-1].damage = 1*damagemod
        player.lastshotfired = tick_counter

def weapon_splode(player, damagemod, fireratemod, shotspeedmod):
    if tick_counter - 30*fireratemod >  player.lastshotfired:
        for j in range(5):
            for i in range(20):
                world.misclist.append(ScreenObject("sprites/effects/orange_debris.png", screen))
                world.misclist[len(world.playerlist)-1].xVelocity = math.sin(i*math.pi/10)*5/random.randint(5, 20)
                world.misclist[len(world.playerlist)-1].yVelocity = math.cos(i*math.pi/10)*5/random.randint(5, 20)
                world.misclist[len(world.playerlist)-1].x = player.x + 6 + random.randint(-3, 3)
                world.misclist[len(world.playerlist)-1].y = player.y + 10 + random.randint(-10, 10)
                player.lastshotfired = tick_counter
        for j in range(3):
            for i in range(20):
                world.misclist.append(ScreenObject("sprites/effects/orange_debris.png", screen))
                world.misclist[len(world.playerlist)-1].xVelocity = math.sin(i*math.pi/10)*40/random.randint(5, 20)
                world.misclist[len(world.playerlist)-1].yVelocity = math.cos(i*math.pi/10)*40/random.randint(5, 20)
                world.misclist[len(world.playerlist)-1].x = player.x + 6
                world.misclist[len(world.playerlist)-1].y = player.y + 10
                player.lastshotfired = tick_counter
        
                


#Fires a bomb in front of you. 15 second cooldown.
def altfire_rocket(player, damagemod, cooldownmod):
    if player.cooldown == 0:
        world.bulletlist.append(Rocket("sprites/bullet/bomb.png", screen, 16, 8 ))
        world.bulletlist[-1].x = player.x + 6
        world.bulletlist[-1].y = player.y - 8
        world.bulletlist[-1].yVelocity = -6
        world.bulletlist[-1].damage = 22*damagemod
        player.cooldown = 900 * cooldownmod

#Reflects enemy projectiles. 7 second cooldown.
def altfire_reflect(player, damagemod, cooldownmod):
    if player.cooldown == 0:
        world.misclist.append(Shield("sprites/effects/reflector.png", screen))
        world.misclist[-1].x = player.x - 43
        world.misclist[-1].y = player.y - 16
        world.misclist[-1].yVelocity = -0.5
        world.misclist[-1].lifetime = world.misclist[-1].lifetime*damagemod
        player.cooldown = 420 * cooldownmod#everyday

#Fires a damaging shot behind you. 10 second cooldown.
def altfire_backblast(player, damagemod, cooldownmod):
    if player.cooldown == 0:
        world.bulletlist.append(Bullet("sprites/bullet/backblast.png", screen, 16, 8, True))
        world.bulletlist[-1].x = player.x - 4
        world.bulletlist[-1].y = player.y + 26
        world.bulletlist[-1].yVelocity = 12
        world.bulletlist[-1].damage = 10*damagemod
        world.bulletlist[-1].w = 24
        world.bulletlist[-1].h = 16
        player.cooldown = 540 * cooldownmod
        player.yVelocity = player.yVelocity - 4
        
######################################

#You!
class PlayerShip(TangibleObject):
    def __init__(self, imageFileName, screen, height=26, width=14, attack=weapon_generic, altfire=altfire_backblast):
        super().__init__(imageFileName, screen, height, width)
        #Whether the player is pressing keys or not 
        self.upPress = False
        self.downPress = False
        self.leftPress = False
        self.rightPress = False
        self.shootPress = False
        self.altPress = False
        self.dodgePress = False
        
        self.maxhealth = 100
        self.health = self.maxhealth
        self.maxspeed = 5
        self.acceleration = 0.5
        self.deceleration = 0.5
        self.lastshotfired = 0
        self.xoffset = -6
        self.attack = attack   #define equipped weapon 
        self.altfire = altfire #define equipped altfire
        self.nextregentick = 0
        self.barrierstate = False 
        self.barrierchargerate = 600 #Time taken to recharge barrier
        self.lastdamagetaken = 0 - self.barrierchargerate
        self.maxcooldown = 1

        self.barrierallowed = False #Barrier upgrade state
        #Weapon/altfire modifiers, for upgrades
        self.damagemod = 1
        self.fireratemod = 1
        self.shotspeedmod = 1
        self.altfiremod = 1
        self.cooldownmod = 1
        self.candodge = False #Dodge upgrade state
        self.timedilation = False #unused
        self.gravitywell = False  #Despite the name, used for the autododge mechanic
        self.regen = 0 #unused
        self.regenrate = 60 #unused
        self.dodgedistance = 48 
        self.dodgerate = 60
        self.retaliate = False #use burst attack when hit
        self.revive = False
        
        self.lastdodge = 0 #last time dodged
        
        self.cooldown = 0 #current altfire cooldown

    def getHit(self, damage):
        if not self.lastdamagetaken + self.barrierchargerate < tick_counter or not self.barrierallowed:
            world.misclist.append(Effect(["sprites/damage.png","sprites/damage.png","sprites/damage.png"], screen))
            if self.lastdamagetaken + 20 > tick_counter: 
                self.health = self.health - damage//2
            else:
                self.health = self.health - damage
        if self.retaliate:
            for i in range(36):
                world.bulletlist.append(Bullet("sprites/effects/orange_debris.png", screen, 2, 2, True))
                world.bulletlist[-1].xVelocity = math.sin(i*math.pi/12)*10
                world.bulletlist[-1].yVelocity = math.cos(i*math.pi/12)*10
                world.bulletlist[-1].x = self.x + 6 
                world.bulletlist[-1].y = self.y + 10
                world.bulletlist[-1].damage = damage//6 + 1
        if self.health < 1 and not self.revive:
            #Death explosion
            for j in range(5):
                #Low velocity, "heavier" particles
                for i in range(60):
                    rando = random.randint(5, 20)
                    world.misclist.append(ScreenObject("sprites/effects/orange_debris.png", screen))
                    world.misclist[len(world.misclist)-1].xVelocity = math.sin(i*math.pi/30)*5/rando
                    world.misclist[len(world.misclist)-1].yVelocity = math.cos(i*math.pi/30)*5/rando
                    world.misclist[len(world.misclist)-1].x = self.x + 6 + random.randint(-3, 3)
                    world.misclist[len(world.misclist)-1].y = self.y + 10 + random.randint(-10, 10)
            for j in range(3):
                #High velocity, "lighter" particles
                for i in range(60):
                    rando = random.randint(5, 20)
                    world.misclist.append(ScreenObject("sprites/effects/orange_debris.png", screen))
                    world.misclist[len(world.misclist)-1].xVelocity = math.sin(i*math.pi/30)*40/rando
                    world.misclist[len(world.misclist)-1].yVelocity = math.cos(i*math.pi/30)*40/rando
                    world.misclist[len(world.misclist)-1].x = self.x + 6
                    world.misclist[len(world.misclist)-1].y = self.y + 10
            #An entity is created as a placeholder on death, so the game doesn't crash.
            world.playerlist.append(blank())
            world.playerlist[-1].y = 4000
            world.playerlist[-1].lifetime = 300
            #Without this, entities referring to the player or their position will crash.
            self.die()
        self.lastdamagetaken = tick_counter
        if self.health < 1 and self.revive:
            for j in range(2):
                for i in range(20):
                    rando = random.randint(5, 20)
                    world.misclist.append(ScreenObject("sprites/effects/orange_debris.png", screen))
                    world.misclist[len(world.misclist)-1].xVelocity = math.sin(i*math.pi/10)*2
                    world.misclist[len(world.misclist)-1].yVelocity = math.cos(i*math.pi/10)*2
                    world.misclist[len(world.misclist)-1].x = self.x + 6 + random.randint(-3, 3)
                    world.misclist[len(world.misclist)-1].y = self.y + 10 + random.randint(-10, 10)
            self.maxhealth = 40
            self.health = 40
            self.revive = False


    def die(self):
        endgame = True
            
    def shoot(self):
        self.attack(self, self.damagemod, self.fireratemod, self.shotspeedmod)

    def alt(self):
        if self.cooldown == 0:
            self.altfire(self, self.altfiremod, self.cooldownmod)
            self.maxcooldown = self.cooldown 

    def dodge(self):
        #teleports a short distance
        #For the warp drive upgrade
        dodge = False
        if self.upPress:
            self.y = self.y - self.dodgedistance
            dodge = True
        if self.downPress:
            self.y = self.y + self.dodgedistance
            dodge = True
        if self.leftPress:
            self.x = self.x + self.dodgedistance
            dodge = True
        if self.rightPress:
            self.x = self.x - self.dodgedistance
            dodge = True
        if dodge == True:
            self.lastdodge = tick_counter
            world.misclist.append(Effect(["sprites/effects/afterimage_01.png",
                                          "sprites/effects/afterimage_02.png",
                                          "sprites/effects/afterimage_03.png",
                                          "sprites/effects/afterimage_04.png",
                                          "sprites/effects/afterimage_05.png",
                                          ],screen))
            world.misclist[-1].x = self.x + self.xoffset
            world.misclist[-1].y = self.y
            world.misclist[-1].xVelocity = -self.xVelocity
            world.misclist[-1].yVelocity = -self.yVelocity

    def pushbullets(self):
        #Autododges bullets
        for i in world.bulletlist:
            if ((i.x - self.x)**2 + (i.y-self.y)**2) < 1600 and i.player == False:
                totalDistance = math.sqrt((i.x - self.x)**2 + (i.y-self.y)**2)
                i.y = i.y - (self.y - i.y)*0.1*i.xVelocity/totalDistance
                i.x = i.x - (self.x - i.x)*0.1*i.yVelocity/totalDistance
                self.y = self.y + (self.y - i.y)*0.15*i.xVelocity/totalDistance
                self.x = self.x + (self.x - i.x)*0.15*i.yVelocity/totalDistance
                
            

    def tick(self):
        super().tick()
        #movement code
        if self.upPress == True:
            if self.yVelocity > (-1*self.maxspeed):
                self.yVelocity = self.yVelocity - self.acceleration
        elif self.downPress == True:
            if self.yVelocity < self.maxspeed:
                self.yVelocity = self.yVelocity + self.acceleration
        else:
            if self.yVelocity > 0:
                if self.yVelocity - self.deceleration < 0:
                    self.yVelocity = 0
                else:
                    self.yVelocity = self.yVelocity - self.deceleration
            if self.yVelocity < 0:
                if self.yVelocity + self.acceleration > 0:
                    self.yVelocity = 0
                else:
                    self.yVelocity = self.yVelocity + self.acceleration
            
        if self.leftPress == True:
            if self.xVelocity < self.maxspeed:
               self.xVelocity = self.xVelocity + self.acceleration
        elif self.rightPress == True:
            if self.xVelocity > (-1*self.maxspeed):
                self.xVelocity = self.xVelocity - self.acceleration
        else:
            if self.xVelocity > 0:
                if self.xVelocity - self.acceleration < 0:
                    self.xVelocity = 0
                else:
                    self.xVelocity = self.xVelocity - self.acceleration
            if self.xVelocity < 0:
                if self.xVelocity + self.deceleration > 0:
                    self.xVelocity = 0
                else:
                    self.xVelocity = self.xVelocity + self.deceleration
        if self.x > screenx - self.w:
            self.x = screenx - self.w
            self.xVelocity = 0
        if self.x < 0:
            self.x = 0
            self.xVelocity = 0
        if self.y < 0:
            self.y = 0
            self.yVelocity = 0
        if self.y > screeny - self.h:
            self.y = screeny - self.h
            self.yVelocity = 0
        if self.shootPress==True:
            self.shoot()
        if self.altPress==True:
            self.alt()
        if self.candodge and self.dodgePress and self.dodgerate + self.lastdodge < tick_counter:
            self.dodge()

        #renders health bar
        label = mainfont.render(str(self.health), 1, (255,192,192))
        screen.blit(label, (10,screeny-24))
        pict = pygame.image.load('sprites/effects/hud/empty_segment.png')
        pict = pict.convert()
        for i in range(self.maxhealth):
            screen.blit(pict, (i+10, screeny - 10))
        pict = pygame.image.load('sprites/effects/hud/bar_segment.png')
        pict = pict.convert()
        for i in range(self.health):
            screen.blit(pict, (i+10, screeny - 10))

        #Renders the alternate fire recharge gauge
        charge = self.maxcooldown - self.cooldown 
        gaugelist = ["sprites/effects/hud/altfire_gauge_00.png",
                     "sprites/effects/hud/altfire_gauge_01.png",
                     "sprites/effects/hud/altfire_gauge_02.png",
                     "sprites/effects/hud/altfire_gauge_03.png",
                     "sprites/effects/hud/altfire_gauge_04.png",
                     "sprites/effects/hud/altfire_gauge_05.png",
                     "sprites/effects/hud/altfire_gauge_06.png",
                     "sprites/effects/hud/altfire_gauge_07.png",
                     "sprites/effects/hud/altfire_gauge_08.png",
                     "sprites/effects/hud/altfire_gauge_09.png",
                     "sprites/effects/hud/altfire_gauge_10.png",
                     "sprites/effects/hud/altfire_gauge_11.png",
                     "sprites/effects/hud/altfire_gauge_12.png",
                     "sprites/effects/hud/altfire_gauge_13.png",
                     "sprites/effects/hud/altfire_gauge_14.png",
                     "sprites/effects/hud/altfire_gauge_15.png",
                     "sprites/effects/hud/altfire_gauge_16.png"]
        pict = pygame.image.load(gaugelist[math.floor(charge/self.maxcooldown*16)])
        pict = pict.convert()
        pict.set_colorkey((255,0,255))
        screen.blit(pict, (screenx-50,screeny-25))

        if self.altfire == altfire_rocket:
            self.altfirename = "BOMB"
        elif self.altfire == altfire_reflect:
            self.altfirename = "REFLECTOR"
        elif self.altfire == altfire_backblast:
            self.altfirename = "BACKBLAST"
        else:
            self.altfirename = "ALT"
        label = mainfont.render(self.altfirename, 1, (255,255,255))
        screen.blit(label, (screenx-54-len(self.altfirename)*9,screeny-16))
            
        if self.nextregentick < tick_counter:
            self.nextregentick = tick_counter + self.regenrate
            if self.health < self.maxhealth:
                self.health = self.health + self.regen

        #Barrier render code
        if self.lastdamagetaken + self.barrierchargerate < tick_counter and self.barrierallowed:
            pict = pygame.image.load('sprites/effects/barrier.png')
            pict = pict.convert()
            pict.set_colorkey((255,0,255))
            screen.blit(pict, (self.x+self.xoffset-3, self.y-2))

        if self.gravitywell:
            self.pushbullets()

        #Altfire cooldown code
        if self.cooldown > 0:
            self.cooldown = self.cooldown - 1

    def die(self):
        world.playerlist.remove(self)
    
class Healthkit(TangibleObject):
    #repairs hull damage
    def __init__(self, imageFileName='sprites/healthkit.png', screen=screen, height=16, width=16):
        super().__init__(imageFileName, screen, height, width)
        self.yVelocity = 0.5
        self.healing = 50
        self.birthday = tick_counter

    def tick(self):
        super().tick()
        if self.y < 0 or self.y > screeny:
            self.y = 0
        if self.x < -128 or self.x > 512:
            self.die()
        self.collide()

    def collide(self):
        for i in world.playerlist:
            if colDet(self, i):
                if i.health + self.healing > i.maxhealth:
                    i.health = i.maxhealth
                else:
                    i.health = i.health + self.healing
                self.die()                

    def die(self):
        try:
            world.misclist.remove(self)
        except:
            None

#Bullet reflector object
class Shield(TangibleObject):
    def __init__(self, imageFileName, screen, height=70, width=100, playerOwned=True):
        super().__init__(imageFileName, screen, height, width)
        self.player = playerOwned
        self.lifetime = 30
        self.birthday = tick_counter

    def tick(self):
        super().tick()
        if self.y < -128 or self.y > 640:
            self.die()
        if self.x < -128 or self.x > 512:
            self.die()
        #inverts enemy bullet velocity and switches the alleigance if possible
        for i in world.bulletlist:
            if colDet(collisionBox(self.x, self.y, 100, 1), i) and i.player == False:
                i.yVelocity = -3-i.yVelocity
                if type(i) == Spark:
                    i.haste = -3-i.haste 
                if type(i) == OrbitingBullet:
                    i.lifetime = 360
                try:
                    i.player = True
                except:
                    i.die()
        #self.x = world.playerlist[0].x-48
        #self.y = world.playerlist[0].y-16
        if self.birthday + self.lifetime < tick_counter:
            self.die()

    def die(self):
        world.misclist.remove(self)
        

#Bullet object
class Bullet(TangibleObject):
    def __init__(self, imageFileName, screen, height=0, width=0, playerOwned=False):
        super().__init__(imageFileName, screen, height, width)
        self.damage = 1
        self.player = playerOwned
        self.hit_effect = ['sprites/effects/laserhit_01.png',
                          'sprites/effects/laserhit_02.png',
                          'sprites/effects/laserhit_03.png']
        self.despawn = True

    def tick(self):
        super().tick()
        if self.despawn == True: #if ofscreen, destroy self.
            if self.y < -128 or self.y > 640:
                self.die()
            if self.x < -128 or self.x > 512:
                self.die()
        self.collide()

    def collide(self):
        #collision detection and damage dealing
        if not self.player:
            for i in world.playerlist:
                if colDet(self, i):
                    i.getHit(self.damage)
                    world.misclist.append(Effect(self.hit_effect, screen))
                    world.misclist[len(world.misclist)-1].x = self.x - 4
                    world.misclist[len(world.misclist)-1].y = self.y
                    self.die()
        else:
            for i in world.enemylist:
                if colDet(self, i):
                    i.getHit(self.damage)
                    world.misclist.append(Effect(self.hit_effect, screen))
                    world.misclist[len(world.misclist)-1].x = self.x - 6
                    world.misclist[len(world.misclist)-1].y = self.y
                    self.die()
                

    def die(self):
        try:
            world.bulletlist.remove(self)
        except:
            None

class DyingBullet(Bullet):
    def __init__(self, imageFileName, screen, height=8, width=8, playerOwned=True):
        super().__init__(imageFileName, screen, height, width, playerOwned)
        self.birthday = tick_counter
        self.lifetime = 200

    def tick(self):
        super().tick()
        if self.lifetime + self.birthday < tick_counter:
            self.die()

#A bullet with an effect trail
class TrailingBullet(Bullet):
    def __init__(self, imageFileName, screen, height=8, width=8, playerOwned=True):
        super().__init__(imageFileName, screen, height, width, playerOwned)
        self.effect = []
        
    def tick(self):
        super().tick()
        world.misclist.append(Effect(self.effect, screen))
        world.misclist[-1].x = self.x
        world.misclist[-1].y = self.y

#A bullet that homes in on the player
class SeekingBullet(Bullet):
    def __init__(self, imageFileName, screen, height=8, width=8):
        super().__init__(imageFileName, screen, height, width)
        self.lifetime = 180
        self.birthday = tick_counter
        self.maxspeed = 6
        self.despawn = False
        self.accrate = 300 #acceleration
        self.hit_effect = ['sprites/effects/darkhit_01.png',
                          'sprites/effects/darkhit_02.png',
                          'sprites/effects/darkhit_03.png']

    def tick(self):
        super().tick()
        self.player = False
        #Code to move towards the player ship
        self.xVelocity = self.xVelocity + ((world.playerlist[0].x - self.x)/self.accrate)
        self.yVelocity = self.yVelocity + ((world.playerlist[0].y - self.y)/self.accrate)
        totalVelocity = math.sqrt(self.xVelocity**2+self.yVelocity**2)
        if totalVelocity > self.maxspeed:
            self.xVelocity = self.xVelocity*(self.maxspeed/totalVelocity)
            self.yVelocity = self.yVelocity*(self.maxspeed/totalVelocity) 

        if self.lifetime + self.birthday < tick_counter:
            world.misclist.append(Effect(self.hit_effect, screen))
            world.misclist[len(world.misclist)-1].x = self.x - 4
            world.misclist[len(world.misclist)-1].y = self.y
            self.die()

#A bullet that orbits around a specified point and fans out.
class OrbitingBullet(Bullet):
    def __init__(self, imageFileName, screen, height=8, width=8, playerOwned=False):
        super().__init__(imageFileName, screen, height, width, playerOwned)
        self.xtarget = 200
        self.ytarget = 300
        self.maxspeed = 8
        self.fanspeed = 1
        self.despawn = False
        self.birthday = tick_counter
        self.lifetime = 360

    def tick(self):
        super().tick()
        self.xVelocity = -1*(self.ytarget - self.y)
        self.yVelocity = (self.xtarget - self.x)
        totalVelocity = math.sqrt(self.xVelocity**2+self.yVelocity**2)
        #Code to move on the normal of the vector toward the orbit point
        #Look, don't worry about it.
        if totalVelocity != 0:
            self.xVelocity = self.xVelocity*(self.maxspeed/totalVelocity)
            self.yVelocity = self.yVelocity*(self.maxspeed/totalVelocity)
        fanx = self.xVelocity - ((self.xtarget - self.x))
        fany = self.yVelocity - ((self.ytarget - self.y))
        if totalVelocity != 0:
            self.xVelocity = self.xVelocity+ fanx*(self.fanspeed/totalVelocity)
            self.yVelocity = self.yVelocity+ fany*(self.fanspeed/totalVelocity)
        if self.player:
            self.xVelocity = -self.xVelocity
            self.yVelocity = -self.yVelocity
        if self.lifetime + self.birthday < tick_counter:
            self.die()

#A bullet that moves erratically.
#Jitters in random directions.
class Spark(Bullet):
    def __init__(self, imageFileName, screen, height=8, width=8, playerOwned=False):
        super().__init__(imageFileName, screen, height, width, playerOwned)
        self.maxspeed = 4
        self.switchtime = 5
        self.lastswitch = 0
        self.haste = 2 #Forced y-movement
        self.fan = 12  #Range of random jittering

    def tick(self):
        super().tick()
        if self.lastswitch + self.switchtime < tick_counter:
            rando = random.randint(-self.fan,self.fan)
            self.xVelocity = math.sin(math.pi*rando/12)*self.maxspeed 
            self.yVelocity = math.cos(math.pi*rando/12)*self.maxspeed + self.haste
            self.lastswitch = tick_counter

class Firework(Bullet):
    def __init__(self, imageFileName, screen, height=8, width=8):
        super().__init__(imageFileName, screen, height, width)
        self.lifetime = 45
        self.birthday = tick_counter
        self.bullet = "sprites/bullet/greenpulse.png"
        self.force = 5
        self.rot = 0
        
    def tick(self):
        super().tick()

        if self.lifetime + self.birthday < tick_counter:
            for i in range(8):
                world.bulletlist.append(Bullet(self.bullet, screen, 6, 8, False))
                world.bulletlist[len(world.bulletlist)-1].x = self.x 
                world.bulletlist[len(world.bulletlist)-1].y = self.y 
                world.bulletlist[len(world.bulletlist)-1].xVelocity = math.cos(self.rot+i*math.pi/4)*self.force
                world.bulletlist[len(world.bulletlist)-1].yVelocity = math.sin(self.rot+i*math.pi/4)*self.force
                world.bulletlist[len(world.bulletlist)-1].damage = 5

            self.die()

    def collide(self):
        super().collide()

#A "bullet" that explodes on impact or after a timer.
class Rocket(TangibleObject):
    def __init__(self, imageFileName, screen, height=8, width=8):
        super().__init__(imageFileName, screen, height, width)
        self.player = True
        self.lifetime = 30
        self.birthday = tick_counter
        self.hit_effect = ["sprites/effects/devsplode.png","sprites/effects/devsplode.png"]
        self.offset = 92  #explosion sprite offset
        self.radius = 100 #exlosion radius
        self.damage = 10

    def tick(self):
        super().tick()

        if self.lifetime + self.birthday < tick_counter:
            self.explode()
            self.die()
        self.collide()

    def explode(self):
        targetlist = []
        for i in world.enemylist:
            #Checks for every enemy in explosion radius.
            if (self.x - i.x-(0.5*i.w))**2 + (self.y - i.y-(0.5*i.h))**2 < (self.radius+0.5*i.w)**2:                
                targetlist.append(i)
                world.misclist.append(Effect(["sprites/effects/laserhit_01.png","sprites/effects/laserhit_02.png","sprites/effects/laserhit_03.png"],screen))
                world.misclist[-1].x = i.x + 3
                world.misclist[-1].y = i.y + 12
        for i in targetlist:
            #Damages everything in a radius.
            i.getHit(self.damage)
        for i in world.playerlist:
            #Damages the player if the player is nearby.
            if (self.x - i.x-(0.5*i.w))**2 + (self.y - i.y-(0.5*i.h))**2 < (self.radius+0.5*i.w)**2:
                i.getHit(6) #Always does six damage to the player, should it hit
                
        world.misclist.append(Effect(self.hit_effect,screen))
        world.misclist[-1].x = self.x - self.offset
        world.misclist[-1].y = self.y - self.offset


    def collide(self):
        for i in world.enemylist:
            if colDet(self, i):
                self.explode()
                self.die()

    def die(self):
        try:
            world.bulletlist.remove(self)
        except:
            pass

#A jittery version of the orbiting bullet. Unused
class OscillatingBullet(OrbitingBullet):
    def __init__(self, imageFileName, screen, height=8, width=8, playerOwned=False):
        super().__init__(imageFileName, screen, height, width, playerOwned)

    def tick(self):
        super().tick()
        self.x = self.x + random.randint(-1,1)
        self.y = self.y + random.randint(-1,1) 

class Location(object):
    def __init__(self, imageFileName, screen):
        self.x = 0
        self.y = 0


class Tutorial(Entity):
    def __init__(self):
        self.lifetime = 180
        self.text = "DUMMY"
        self.birthday = tick_counter
        self.msgx = 10
        self.msgy = 256
        self.x = -500
        self.y = -500
        self.w = 0
        self.h = 0

    def tick(self):
        label = mainfont.render(self.text, 1, (255,255,255))
        screen.blit(label, (self.msgx,self.msgy))
        if self.lifetime + self.birthday < tick_counter:
            self.die()

    def getHit(self):
        pass

    def die(self):
        world.enemylist.remove(self)
        

class tutorial_move(Tutorial):
    def __init__(self):
        super().__init__()
        self.text = "PRESS ARROW KEYS TO MOVE"

class tutorial_shoot(Tutorial):
    def __init__(self):
        super().__init__()
        self.text = "PRESS Z KEY TO SHOOT"

class tutorial_alt(Tutorial):
    def __init__(self):
        super().__init__()
        self.text = "PRESS X KEY TO USE ALTERNATE ATTACK"

class tutorial_health_1(Tutorial):
    def __init__(self):
        super().__init__()
        self.text = "THE BAR IN THE BOTTOM LEFT IS YOUR ARMOUR."
        
class tutorial_health_2(Tutorial):
    def __init__(self):
        super().__init__()
        self.text = "IF IT REACHES ZERO, YOU WILL DIE."
        self.msgy = 266

class tutorial_kit(Tutorial):
    def __init__(self):
        super().__init__()
        self.text = "GRAB A REPAIR KIT TO RESTORE YOUR ARMOUR."
        
class tutorial_cooldown_1(Tutorial):
    def __init__(self):
        super().__init__()
        self.text = "ALT ATTACKS HAVE A COOLDOWN TIME THAT IS"
        
class tutorial_cooldown_2(Tutorial):
    def __init__(self):
        super().__init__()
        self.text = "INDICATED IN THE BOTTOM RIGHT."
        self.msgy = 266
        

##################################### ENEMIES ##################################################        

#basic enemy type
class enemy_generic(EnemyShip):
    
    def __init__(self):
        super().__init__("devnemy.png", screen)

    def tick(self):
        super().tick()

    def shoot(self):
        super().shoot()

    def getHit(self, damage):
        super().getHit(damage)

    def die(self):
        super().die()

#fires fast-moving, weaker shots
class enemy_sniper(EnemyShip):
    
    def __init__(self):
        super().__init__("sprites/sniper.png", screen)
        self.firerate = 45
        self.health = 8

    def tick(self):
        super().tick()

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Bullet("sprites/bullet/whitepulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 8
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 10
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 10
            world.bulletlist[len(world.bulletlist)-1].damage = 6
            self.lastshotfired = tick_counter
        

    def getHit(self, damage):
        super().getHit(damage)

    def die(self):
        super().die()

#Weaksauce enemy
class enemy_sniper_weak(EnemyShip):
    def __init__(self):
        super().__init__("sprites/sniper.png", screen)
        self.firerate = 90

    def tick(self):
        super().tick()

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Bullet("sprites/bullet/whitepulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 8
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 10
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 8
            world.bulletlist[len(world.bulletlist)-1].damage = 6
            self.lastshotfired = tick_counter
        

    def getHit(self, damage):
        super().getHit(damage)

    def die(self):
        super().die()

#fires in bursts. if he shoots you, *monkey screech*, it's gonna hurt
class enemy_burst(EnemyShip):
    
    def __init__(self):
        super().__init__("sprites/burst.png", screen)
        self.firerate = 10
        self.shotcycle = 0
        self.health = 10

    def tick(self):
        super().tick()

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            self.shotcycle = self.shotcycle + 1
            world.bulletlist.append(Bullet("sprites/bullet/redpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 8
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 10
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 5
            world.bulletlist[len(world.bulletlist)-1].damage = 7
            self.lastshotfired = tick_counter
            if self.shotcycle > 3:
                self.firerate = 65
                self.shotcycle = 0
            else:
                self.firerate = 10
                
        

    def getHit(self, damage):
        super().getHit(damage)

    def die(self):
        super().die()

#sprays bullets in random directions at a rapid rate
class enemy_sprayer(EnemyShip):
    def __init__(self):
        super().__init__("sprites/sprayer.png", screen)
        self.firerate = 16

    def tick(self):
        super().tick()

    def getHit(self, damage):
        super().getHit(damage)
        
    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Bullet("sprites/bullet/pinkpulse.png", screen, 6, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 8
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 20
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 5
            world.bulletlist[len(world.bulletlist)-1].damage = 5
            world.bulletlist[len(world.bulletlist)-1].xVelocity = random.randint(-2, 2)
            world.bulletlist[len(world.bulletlist)-1].xoffset = -1
            self.lastshotfired = tick_counter

    def die(self):
        super().die()

#Slow moving enemy. Fires a wall of bullets to either side of it
class enemy_trawler(EnemyShip):
    
    def __init__(self):
        super().__init__("sprites/trawler.png", screen, width = 34)
        self.firerate = 10
        self.health = 25

    def getHit(self, damage):
        super().getHit(damage)
        
    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Bullet("sprites/bullet/devpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 6
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 20
            world.bulletlist[len(world.bulletlist)-1].xVelocity = -3
            world.bulletlist[len(world.bulletlist)-1].damage = 12
            world.bulletlist.append(Bullet("sprites/bullet/devpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 20
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 20
            world.bulletlist[len(world.bulletlist)-1].xVelocity = 3
            world.bulletlist[len(world.bulletlist)-1].damage = 12 
                
            self.lastshotfired = tick_counter

    def die(self):
        world.score = world.score + 1
        world.misclist.append(Effect(["sprites/effects/explosion_small_01.png",
                                      "sprites/effects/explosion_small_02.png",
                                      "sprites/effects/explosion_small_03.png",
                                      "sprites/effects/explosion_small_04.png",
                                      "sprites/effects/explosion_small_05.png",
                                      "sprites/effects/explosion_small_06.png",
                                      "sprites/effects/explosion_small_07.png",
                                      "sprites/effects/explosion_small_08.png",
                                      "sprites/effects/explosion_small_09.png",
                                      "sprites/effects/explosion_small_10.png",
                                      "sprites/effects/explosion_small_11.png",
                                      "sprites/effects/explosion_small_12.png",
                                      "sprites/effects/explosion_small_13.png",
                                      ],screen))
        world.misclist[-1].x = self.x -10
        world.misclist[-1].y = self.y -4
        world.enemylist.remove(self)

#Fires bullets eratically. Unused.
class enemy_spark(EnemyShip):
    def __init__(self):
        super().__init__("sprites/boss/RYAN.png", screen)
        self.firerate = 12

    def tick(self):
        super().tick()

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Spark("sprites/bullet/yellowpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 10
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 26
            world.bulletlist[len(world.bulletlist)-1].damage = 9
            world.bulletlist[len(world.bulletlist)-1].haste = 0
            self.lastshotfired = tick_counter
            
#fires three shots with wide spread
class enemy_shotgun(EnemyShip):
    
    def __init__(self):
        super().__init__("sprites/shotgun.png", screen)
        firerate = 60

    def tick(self):
        super().tick()

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Bullet("sprites/bullet/cyanpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 10
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 26
            world.bulletlist[len(world.bulletlist)-1].xVelocity = -3
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 4
            world.bulletlist[len(world.bulletlist)-1].damage = 9
            world.bulletlist.append(Bullet("sprites/bullet/cyanpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 10
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 26
            world.bulletlist[len(world.bulletlist)-1].xVelocity = 3
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 4
            world.bulletlist[len(world.bulletlist)-1].damage = 9
            world.bulletlist.append(Bullet("sprites/bullet/cyanpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 10
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 26
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 5
            world.bulletlist[len(world.bulletlist)-1].damage = 9
            
            self.lastshotfired = tick_counter

    def getHit(self, damage):
        super().getHit(damage)

    def die(self):
        super().die()

#an enemy that has got to go fast
class enemy_quick(EnemyShip):
    
    def __init__(self):
        super().__init__("sprites/quick.png", screen)
        self.yVelocity = 2
        self.health = 8
        firerate = 40

    def tick(self):
        super().tick()

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Bullet("sprites/bullet/yellowpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 10
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 26
            world.bulletlist[len(world.bulletlist)-1].xVelocity = -1
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 5
            world.bulletlist[len(world.bulletlist)-1].damage = 8
            world.bulletlist.append(Bullet("sprites/bullet/yellowpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 10
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 26
            world.bulletlist[len(world.bulletlist)-1].xVelocity = 1
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 5
            world.bulletlist[len(world.bulletlist)-1].damage = 8
            self.lastshotfired = tick_counter

    def getHit(self, damage):
        super().getHit(damage)

    def die(self):
        super().die()

#fires bombs that blossom into eight shots
class enemy_bomber(EnemyShip):
    def __init__(self):
        super().__init__("sprites/bomber.png", screen)
        self.firerate = 90
        self.health = 10

    def tick(self):
        super().tick()

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Firework("sprites/bullet/rocket.png", screen, 8, 8))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 8
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 10
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 4
            world.bulletlist[len(world.bulletlist)-1].damage = 15
            self.lastshotfired = tick_counter
        

    def getHit(self, damage):
        super().getHit(damage)

    def die(self):
        super().die()


#fires walls of bullets
class enemy_brickie(EnemyShip):
    def __init__(self):
        super().__init__("sprites/bricklayer.png", screen)
        self.firerate = 90
        self.health = 12
        self.damage = 5
        self.shotspeed = 2

    def tick(self):
        super().tick()

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            #Six slow moving bullets that fan out very slowly.
            world.bulletlist.append(Bullet("sprites/bullet/purplepulse.png", screen, 8, 8))
            world.bulletlist[len(world.bulletlist)-1].x = self.x -6
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 26
            world.bulletlist[len(world.bulletlist)-1].yVelocity = self.shotspeed
            world.bulletlist[len(world.bulletlist)-1].xVelocity = -0.09
            world.bulletlist[len(world.bulletlist)-1].damage = self.damage
            world.bulletlist.append(Bullet("sprites/bullet/purplepulse.png", screen, 8, 8))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 0
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 26
            world.bulletlist[len(world.bulletlist)-1].xVelocity = -0.06
            world.bulletlist[len(world.bulletlist)-1].yVelocity = self.shotspeed
            world.bulletlist[len(world.bulletlist)-1].damage = self.damage
            world.bulletlist.append(Bullet("sprites/bullet/purplepulse.png", screen, 8, 8))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 6
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 26
            world.bulletlist[len(world.bulletlist)-1].xVelocity = -0.03
            world.bulletlist[len(world.bulletlist)-1].yVelocity = self.shotspeed
            world.bulletlist[len(world.bulletlist)-1].damage = self.damage
            world.bulletlist.append(Bullet("sprites/bullet/purplepulse.png", screen, 8, 8))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 12
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 26
            world.bulletlist[len(world.bulletlist)-1].xVelocity = 0.03
            world.bulletlist[len(world.bulletlist)-1].yVelocity = self.shotspeed
            world.bulletlist[len(world.bulletlist)-1].damage = self.damage
            world.bulletlist.append(Bullet("sprites/bullet/purplepulse.png", screen, 8, 8))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 18
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 26
            world.bulletlist[len(world.bulletlist)-1].xVelocity = 0.06
            world.bulletlist[len(world.bulletlist)-1].yVelocity = self.shotspeed
            world.bulletlist[len(world.bulletlist)-1].damage = self.damage
            world.bulletlist.append(Bullet("sprites/bullet/purplepulse.png", screen, 8, 8))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 24
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 26
            world.bulletlist[len(world.bulletlist)-1].xVelocity = 0.1
            world.bulletlist[len(world.bulletlist)-1].yVelocity = self.shotspeed
            world.bulletlist[len(world.bulletlist)-1].damage = self.damage
            self.lastshotfired = tick_counter
        

    def getHit(self, damage):
        super().getHit(damage)

    def die(self):
        super().die()


#fires homing shots
class enemy_seeker(EnemyShip):
    
    def __init__(self):
        super().__init__("sprites/seeker.png", screen)
        self.firerate = 120
        self.health = 7

    def tick(self):
        super().tick()

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(SeekingBullet("sprites/bullet/blackpulse.png", screen, 8, 8))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 8
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 10
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 2
            world.bulletlist[len(world.bulletlist)-1].damage = 8
            self.lastshotfired = tick_counter
        

    def getHit(self, damage):
        super().getHit(damage)

    def die(self):
        super().die()

#fires a constant stream of bullets side-to-side
class enemy_hellion(EnemyShip):
    def __init__(self):
        super().__init__("sprites/hellion.png", screen)
        self.firerate = 6
        self.health = 5
        self.modifier = random.randint(0,10)

    def tick(self):
        super().tick()

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Bullet("sprites/bullet/greenpulse.png", screen, 8, 8))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 8
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 10
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 5
            world.bulletlist[len(world.bulletlist)-1].xVelocity = 2*(math.sin(self.y*0.03+self.modifier))
            world.bulletlist[len(world.bulletlist)-1].damage = 6
            self.lastshotfired = tick_counter
        

    def getHit(self, damage):
        super().getHit(damage)

    def die(self):
        super().die()

#Used to create lulls in the action
class blank(Entity):
    def __init__(self):
        self.birthday = tick_counter
        self.lifetime = 60
        self.x = 0
        self.y = -500
        self.w = 0
        self.h = 0
        
    def tick(self):
        if self.birthday + (self.lifetime) < tick_counter:
            self.die()
            
    def die(self):
        world.enemylist.remove(self)
        
    def getHit(self, x):
        pass

        
#WAVE------------------------------------------------------------------------------
        #These are the same enemies, but they move in a wave.
#a generic that moves in a sine wave
class enemy_generic_wave(enemy_generic):
    def __init__(self):
        super().__init__()
        self.xmod = 0
        
    def tick(self):
        super().tick()
        self.x = self.x - self.xmod
        self.xmod = 40*(math.sin(self.y*0.02))
        self.x = self.x + self.xmod

    def getHit(self, damage):
        super().getHit(damage)
        
    def shoot(self):
        super().shoot()

    def die(self):
        super().die()

class enemy_generic_wave_alt(enemy_generic):
    def __init__(self):
        super().__init__()
        self.xmod = 0
        
    def tick(self):
        super().tick()
        self.xmod = 0.8*(math.cos(self.y*0.02))
        self.x = self.x + self.xmod

    def getHit(self, damage):
        super().getHit(damage)
        
    def shoot(self):
        super().shoot()

    def die(self):
        super().die()


#a sprayer that moves in a sine wave
class enemy_sprayer_wave(enemy_sprayer):
    def __init__(self):
        super().__init__()
        self.health = 8
        self.xmod = 0

    def tick(self):
        super().tick()
        self.x = self.x - self.xmod
        self.xmod = 40*(math.sin(self.y*0.02))
        self.x = self.x + self.xmod

    def getHit(self, damage):
        super().getHit(damage)
        
    def shoot(self):
        super().shoot()

    def die(self):
        super().die()

#a sniper that moves in a sine wave
class enemy_sniper_wave(enemy_sniper):
    def __init__(self):
        super().__init__()
        self.xmod = 0

    def tick(self):
        super().tick()
        self.x = self.x - self.xmod
        self.xmod = 40*(math.sin(self.y*0.02))
        self.x = self.x + self.xmod

    def getHit(self, damage):
        super().getHit(damage)
        
    def shoot(self):
        super().shoot()

    def die(self):
        super().die()

#a burst that moves in a not-sine wave
class enemy_burst_wave(enemy_burst):
    def __init__(self):
        super().__init__()
        self.xmod = 0

    def tick(self):
        super().tick()
        self.x = self.x - self.xmod
        self.xmod = 40*(math.sin(self.y*0.02))
        self.x = self.x + self.xmod

    def getHit(self, damage):
        super().getHit(damage)
        
    def shoot(self):
        super().shoot()

    def die(self):
        super().die()

#a trawler that moves in a wave with unkown properties
class enemy_trawler_wave(enemy_trawler):
    def __init__(self):
        super().__init__()
        self.xmod = 0

    def tick(self):
        super().tick()
        self.x = self.x - self.xmod
        self.xmod = 40*(math.sin(self.y*0.02))
        self.x = self.x + self.xmod

    def getHit(self, damage):
        super().getHit(damage)
        
    def shoot(self):
        super().shoot()

    def die(self):
        super().die()

#a wavy burst that fires continuously
class enemy_burst_wave_unbound(enemy_burst_wave):
    def __init__(self):
        super().__init__()
        self.xmod = 0
        self.firerate = 10

    def tick(self):
        super().tick()

    def getHit(self, damage):
        super().getHit(damage)
        
    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Bullet("sprites/bullet/pinkpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 8
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 10
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 5
            world.bulletlist[len(world.bulletlist)-1].damage = 4
            self.lastshotfired = tick_counter

    def die(self):
        super().die()

#AAAAAAAAAAAAA
class enemy_whip_wave(enemy_burst_wave):
    def __init__(self):
        super().__init__()
        self.xmod = 0

    def tick(self):
        super().tick()

    def getHit(self, damage):
        super().getHit(damage)
        
    def shoot(self):
        world.bulletlist.append(Bullet("sprites/bullet/pinkpulse.png", screen, 8, 8, False))
        world.bulletlist[len(world.bulletlist)-1].x = self.x + 8
        world.bulletlist[len(world.bulletlist)-1].y = self.y + 10
        world.bulletlist[len(world.bulletlist)-1].yVelocity = 6
        world.bulletlist[len(world.bulletlist)-1].damage = 1
        self.lastshotfired = tick_counter

    def die(self):
        super().die()

#a shotgun man that moves in a mysterious pattern
class enemy_shotgun_wave(enemy_shotgun):
    def __init__(self):
        super().__init__()
        self.xmod = 0

    def tick(self):
        super().tick()
        self.x = self.x - self.xmod
        self.xmod = 40*(math.sin(self.y*0.02))
        self.x = self.x + self.xmod

    def getHit(self, damage):
        super().getHit(damage)
        
    def shoot(self):
        super().shoot()

    def die(self):
        super().die()

#it moves...... like lightning
class enemy_quick_wave(enemy_quick):
    def __init__(self):
        super().__init__()
        self.xmod = 0

    def tick(self):
        super().tick()
        self.x = self.x - self.xmod
        self.xmod = 40*(math.sin(self.y*0.02))
        self.x = self.x + self.xmod

    def getHit(self, damage):
        super().getHit(damage)
        
    def shoot(self):
        super().shoot()

    def die(self):
        super().die()

#it's like new year's eve
class enemy_bomber_wave(enemy_bomber):
    def __init__(self):
        super().__init__()
        self.xmod = 0

    def tick(self):
        super().tick()
        self.x = self.x - self.xmod
        self.xmod = 40*(math.sin(self.y*0.02))
        self.x = self.x + self.xmod

    def getHit(self, damage):
        super().getHit(damage)
        
    def shoot(self):
        super().shoot()

    def die(self):
        super().die()

#you build dat wall i dig a hole
class enemy_brickie_wave(enemy_brickie):
    def __init__(self):
        super().__init__()
        self.xmod = 0

    def tick(self):
        super().tick()
        self.x = self.x - self.xmod
        self.xmod = 40*(math.sin(self.y*0.02))
        self.x = self.x + self.xmod

    def getHit(self, damage):
        super().getHit(damage)

    def shoot(self):
        super().shoot()

    #some day that wall is gonna fall
    def die(self):
        super().die()

#can dodge you like you dodge it
class enemy_seeker_wave(enemy_seeker):
    def __init__(self):
        super().__init__()
        self.xmod = 0

    def tick(self):
        super().tick()
        self.x = self.x - self.xmod
        self.xmod = 40*(math.sin(self.y*0.02))
        self.x = self.x + self.xmod

    def getHit(self, damage):
        super().getHit(damage)
        
    def shoot(self):
        super().shoot()

    def die(self):
        super().die()

#wonder what the formula for the shot pattern is
class enemy_hellion_wave(enemy_hellion):
    def __init__(self):
        super().__init__()
        self.xmod = 0

    def tick(self):
        super().tick()
        self.x = self.x - self.xmod
        self.xmod = 40*(math.sin(self.y*0.02))
        self.x = self.x + self.xmod

    def getHit(self, damage):
        super().getHit(damage)
        
    def shoot(self):
        super().shoot()

    def die(self):
        super().die()

#HEALTH------------------------------------------------------------------------------
            #Versions of enemies that drop health
class enemy_sniper_health(enemy_sniper):
    def die(self):
        world.misclist.append(Healthkit())
        world.misclist[len(world.misclist)-1].x = self.x + 6
        world.misclist[len(world.misclist)-1].y = self.y
        super().die()

class enemy_shotgun_health(enemy_shotgun):
    def die(self):
        world.misclist.append(Healthkit())
        world.misclist[len(world.misclist)-1].x = self.x + 6
        world.misclist[len(world.misclist)-1].y = self.y
        super().die()

class enemy_burst_health(enemy_burst):
    def die(self):
        world.misclist.append(Healthkit())
        world.misclist[len(world.misclist)-1].x = self.x + 6
        world.misclist[len(world.misclist)-1].y = self.y
        super().die()

class enemy_trawler_health(enemy_trawler):
    def die(self):
        world.misclist.append(Healthkit())
        world.misclist[len(world.misclist)-1].x = self.x + 6
        world.misclist[len(world.misclist)-1].y = self.y
        super().die()

class enemy_sprayer_health(enemy_sprayer):
    def die(self):
        world.misclist.append(Healthkit())
        world.misclist[len(world.misclist)-1].x = self.x + 6
        world.misclist[len(world.misclist)-1].y = self.y
        super().die()

class enemy_quick_health(enemy_quick):
    def die(self):
        world.misclist.append(Healthkit())
        world.misclist[len(world.misclist)-1].x = self.x + 6
        world.misclist[len(world.misclist)-1].y = self.y
        super().die()

class enemy_bomber_health(enemy_bomber):
    def die(self):
        world.misclist.append(Healthkit())
        world.misclist[len(world.misclist)-1].x = self.x + 6
        world.misclist[len(world.misclist)-1].y = self.y
        super().die()
        
class enemy_brickie_health(enemy_brickie):
    def die(self):
        world.misclist.append(Healthkit())
        world.misclist[len(world.misclist)-1].x = self.x + 6
        world.misclist[len(world.misclist)-1].y = self.y
        super().die()

class enemy_seeker_health(enemy_seeker):
    def die(self):
        world.misclist.append(Healthkit())
        world.misclist[len(world.misclist)-1].x = self.x + 6
        world.misclist[len(world.misclist)-1].y = self.y
        super().die()
        
class enemy_hellion_health(enemy_hellion):
    def die(self):
        world.misclist.append(Healthkit())
        world.misclist[len(world.misclist)-1].x = self.x + 6
        world.misclist[len(world.misclist)-1].y = self.y
        super().die()

#BOSS------------------------------------------------------------------------------
        #Boss enemies
class Boss(EnemyShip):
    
    def __init__(self, imageFileName):
        super().__init__(imageFileName, screen, width = 78, height = 78)
        self.health = 200
        self.yVelocity = 0.5
        self.xmod = 0
        self.firerate = 30
        self.lastpunch = 0
        self.punchrate = 20
        self.y = -92
        self.punchVelocity = 15 #Force applied when the player touches the boss
        self.punchDamage = 12
        self.stoppingPoint = 64 #Point at which the boss stops moving
        self.wiggle = True #Enables the side-to-side movement of bosses

    def tick(self):
        super().tick()
        if self.y > self.stoppingPoint:
            self.yVelocity = 0
        if self.wiggle:
            self.x = self.x - self.xmod
            self.xmod = 40*(math.sin(tick_counter*0.02))
            self.x = self.x + self.xmod
        if self.punchrate + self.lastpunch < tick_counter:
            for i in world.playerlist:
                if colDet(self,i):
                    i.getHit(self.punchDamage)
                    dist = math.sqrt((self.x + (self.w/2) - i.x)**2 + (self.y - (self.h/2) - i.y)**2)
                    i.xVelocity = (self.punchVelocity/dist)*(i.x - self.x - (self.w/2))
                    i.yVelocity = (self.punchVelocity/dist)*(i.y - self.y - (self.h/2))
                    self.lastpunch = tick_counter
        #pict = pygame.image.load('sprites/effects/hud/empty_segment.png')
        #pict = pict.convert()
        #for i in range(self.maxhealth//2):
        #    screen.blit(pict, (i+10, 10))
        pict = pygame.image.load('sprites/effects/hud/bar_segment.png')
        pict = pict.convert()
        for i in range(round(self.health/2)):
            screen.blit(pict, (i+10, 10))
        

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Bullet("devpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 24
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 50
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 6
            world.bulletlist[len(world.bulletlist)-1].damage = 10
            self.lastshotfired = tick_counter

    def getHit(self, damage):
        super().getHit(damage)

    def die(self):
        world.misclist.append(Effect(["sprites/effects/explosion_small_01.png",
                                      "sprites/effects/explosion_small_02.png",
                                      "sprites/effects/explosion_small_03.png",
                                      "sprites/effects/explosion_small_04.png",
                                      "sprites/effects/explosion_small_05.png",
                                      "sprites/effects/explosion_small_06.png",
                                      "sprites/effects/explosion_small_07.png",
                                      "sprites/effects/explosion_small_08.png",
                                      "sprites/effects/explosion_small_09.png",
                                      "sprites/effects/explosion_small_10.png",
                                      "sprites/effects/explosion_small_11.png",
                                      "sprites/effects/explosion_small_12.png",
                                      "sprites/effects/explosion_small_13.png",
                                      ],screen))
        world.misclist[-1].x = self.x +50 
        world.misclist[-1].y = self.y +0.3*self.h
        world.misclist.append(Effect(["sprites/effects/explosion_small_01.png",
                                      "sprites/effects/explosion_small_02.png",
                                      "sprites/effects/explosion_small_03.png",
                                      "sprites/effects/explosion_small_04.png",
                                      "sprites/effects/explosion_small_05.png",
                                      "sprites/effects/explosion_small_06.png",
                                      "sprites/effects/explosion_small_07.png",
                                      "sprites/effects/explosion_small_08.png",
                                      "sprites/effects/explosion_small_09.png",
                                      "sprites/effects/explosion_small_10.png",
                                      "sprites/effects/explosion_small_11.png",
                                      "sprites/effects/explosion_small_12.png",
                                      "sprites/effects/explosion_small_13.png",
                                      ],screen))
        world.misclist[-1].x = self.x +21 
        world.misclist[-1].y = self.y +0.8*self.h
        super().die()

#First boss. Damage sponge who shoots forwards. An introduction to the concept of bosses.
class enemy_sniper_weak_boss(Boss):
    def __init__(self):
        super().__init__("sprites/boss/sniper_weak_b.png")
        self.h = 33
        self.firerate = 40

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Bullet("sprites/bullet/whitepulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 39
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 50
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 12
            world.bulletlist[len(world.bulletlist)-1].damage = 5
            self.lastshotfired = tick_counter

#A boss who shoots at you with fast bullets. Leads shots ever so slightly, making them a little harder to dodge.
class enemy_sniper_boss(Boss):
    def __init__(self):
        super().__init__("sprites/boss/sniper_b.png")
        self.h = 33
        self.health = 155
        self.firerate = 20

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Bullet("sprites/bullet/pinkpulse.png", screen, 8, 8, False))
            world.bulletlist[-1].x = self.x + 39
            world.bulletlist[-1].y = self.y + 33
            world.bulletlist[-1].yVelocity = 12
            world.bulletlist[-1].xVelocity = ((world.playerlist[0].x - 13 - self.x + (world.playerlist[0].xVelocity*math.sqrt(world.playerlist[0].x**2+world.playerlist[0].y**2)/40))/50)
            world.bulletlist[-1].yVelocity = ((world.playerlist[0].y - 13 - self.y + (world.playerlist[0].yVelocity*math.sqrt(world.playerlist[0].x**2+world.playerlist[0].y**2)/40))/50)
            totalVelocity = math.sqrt(world.bulletlist[-1].xVelocity**2+world.bulletlist[-1].yVelocity**2)
            if totalVelocity != 0:
                world.bulletlist[len(world.bulletlist)-1].xVelocity = world.bulletlist[-1].xVelocity*(10/totalVelocity)
                world.bulletlist[len(world.bulletlist)-1].yVelocity = world.bulletlist[len(world.bulletlist)-1].yVelocity*(10/totalVelocity) 
            world.bulletlist[len(world.bulletlist)-1].damage = 4
            self.lastshotfired = tick_counter

#A boss who shoots you with a jolly great big laser. 
class enemy_sniper_boss_2(Boss):
    def __init__(self):
        super().__init__("sprites/boss/sniper_b.png")
        self.h = 33
        self.health = 155
        self.aimrate = 5
        self.firerate = 30
        self.crosshairX = 100
        self.crosshairY = 300
        self.hit_effect = ["sprites/effects/wee_devsplode.png" for i in range(5)]
        self.offset = 40  #explosion sprite offset
        self.radius = 25 #exlosion radius

    def shoot(self):
        if tick_counter - self.aimrate ==  self.lastshotfired:
            self.crosshairX = world.playerlist[0].x
            self.crosshairY = world.playerlist[0].y
            world.misclist.append(Effect(["sprites/effects/devcrosshairs.png" for i in range(self.firerate-self.aimrate)],screen))
            world.misclist[-1].x = self.crosshairX -9
            world.misclist[-1].y = self.crosshairY                     
    
        if tick_counter - self.firerate > self.lastshotfired:
            #self.explode(self.crosshairX, self.crosshairY)
            hitplayer = False
            for i in range(40):
                xd = ((self.crosshairX -20 - self.x))
                yd = ((self.crosshairY -20 - self.y))
                td = math.sqrt(xd**2+yd**2)
                targetx = self.x + xd*(i*20/td) + 25
                targety = self.y + yd*(i*20/td) + 20
                
                for i in world.playerlist:
                    if (targetx - i.x)**2 + (targety - i.y)**2 < (self.radius)**2:
                        hitplayer = True
                        
            if abs(xd)<abs(yd): 
                laserwidth = math.sin(math.atan(abs(yd/xd)))
            else:
                laserwidth = math.sin(math.atan(abs(xd/yd)))
                
            world.misclist.append(LineObject((255,255,255), (self.x+25 +xd*(30/td),self.y+30+yd*(30/td)),
                                             (self.x + xd*(1200/td) + 25,
                                              self.y + yd*(1200/td) + 30),
                            abs(math.floor(50//laserwidth))
                                             ))
            
            world.misclist.append(Effect(self.hit_effect,screen))
            world.misclist[-1].x = self.x - self.offset +xd*(50/td) +25
            world.misclist[-1].y = self.y - self.offset +yd*(50/td) +20
            if hitplayer:
                world.playerlist[0].getHit(8)
            self.lastshotfired = tick_counter

    def die(self):
        world.misclist.append(ScreenObject('sprites/boss/gibs/sniper_b_gib_1.png', screen))
        world.misclist[-1].x = self.x
        world.misclist[-1].y = self.y
        world.misclist[-1].xVelocity = -0.4
        world.misclist[-1].yVelocity = 0.1
        world.misclist.append(ScreenObject('sprites/boss/gibs/sniper_b_gib_2.png', screen))
        world.misclist[-1].x = self.x
        world.misclist[-1].y = self.y
        world.misclist[-1].xVelocity = 0.4
        world.misclist[-1].yVelocity = -0.2
        world.misclist.append(ScreenObject('sprites/boss/gibs/sniper_b_gib_3.png', screen))
        world.misclist[-1].x = self.x
        world.misclist[-1].y = self.y
        world.misclist[-1].xVelocity = 0.3
        world.misclist[-1].yVelocity = 0.3
        world.misclist.append(ScreenObject('sprites/boss/gibs/sniper_b_gib_4.png', screen))
        world.misclist[-1].x = self.x
        world.misclist[-1].y = self.y
        world.misclist[-1].xVelocity = -0.2
        world.misclist[-1].yVelocity = -0.3
        super().die()
        
            
            
# Burst boss. Fires a constant stream of bullets at you. There's a trick to dodging it.
class enemy_burst_boss(Boss):
    def __init__(self):
        super().__init__("sprites/boss/burst_b.png")
        self.y = -80
        self.w = 78
        self.h = 78
        self.firerate = 10
        self.shotcycle = 0

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Bullet("sprites/bullet/redpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 39
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 74
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 12
            world.bulletlist[len(world.bulletlist)-1].xVelocity = ((world.playerlist[0].x - 13 - self.x + random.randint (-1, 1))/50)
            world.bulletlist[len(world.bulletlist)-1].yVelocity = ((world.playerlist[0].y - 13 - self.y + random.randint (-1, 1))/50)
            totalVelocity = math.sqrt(world.bulletlist[len(world.bulletlist)-1].xVelocity**2+world.bulletlist[len(world.bulletlist)-1].yVelocity**2)
            if totalVelocity != 0:
                world.bulletlist[len(world.bulletlist)-1].xVelocity = world.bulletlist[len(world.bulletlist)-1].xVelocity*(5/totalVelocity)
                world.bulletlist[len(world.bulletlist)-1].yVelocity = world.bulletlist[len(world.bulletlist)-1].yVelocity*(5/totalVelocity) 
            world.bulletlist[len(world.bulletlist)-1].damage = 7
            self.shotcycle = self.shotcycle + 1
            self.lastshotfired = tick_counter
            if self.shotcycle > 3:
                self.firerate = 20
                self.shotcycle = 0
            else:
                self.firerate = 10

    def die(self):
        world.misclist.append(ScreenObject('sprites/boss/gibs/burst_b_gib_1.png', screen))
        world.misclist[-1].x = self.x
        world.misclist[-1].y = self.y
        world.misclist[-1].yVelocity = -0.3
        world.misclist.append(ScreenObject('sprites/boss/gibs/burst_b_gib_2.png', screen))
        world.misclist[-1].x = self.x
        world.misclist[-1].y = self.y
        world.misclist[-1].xVelocity = -0.4
        world.misclist[-1].yVelocity = -0.2
        world.misclist.append(ScreenObject('sprites/boss/gibs/burst_b_gib_3.png', screen))
        world.misclist[-1].x = self.x
        world.misclist[-1].y = self.y
        world.misclist[-1].xVelocity = 0.3
        world.misclist[-1].yVelocity = -0.3
        world.misclist.append(ScreenObject('sprites/boss/gibs/burst_b_gib_4.png', screen))
        world.misclist[-1].x = self.x
        world.misclist[-1].y = self.y
        world.misclist[-1].xVelocity = -0.1
        world.misclist[-1].yVelocity = 0.3
        super().die()

#Shotgun boss. Shoots splashes randomly.
class enemy_shotgun_boss(Boss):
    def __init__(self):
        super().__init__("sprites/boss/shotgun_b2.png")
        self.health = 300
        self.h = 75
        self.w = 75
        self.stoppingpoint = 160
        self.firerate = 30
        
    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            randox = random.randint(-2, 2)
            randoy = random.randint(-2, 2)
            world.bulletlist.append(Bullet("sprites/bullet/cyanpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 35
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 75
            world.bulletlist[len(world.bulletlist)-1].xVelocity = 5 +randox
            world.bulletlist[len(world.bulletlist)-1].damage = 9
            world.bulletlist.append(Bullet("sprites/bullet/cyanpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 35
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 75
            world.bulletlist[len(world.bulletlist)-1].xVelocity = -5 +randox
            world.bulletlist[len(world.bulletlist)-1].damage = 9
            world.bulletlist.append(Bullet("sprites/bullet/cyanpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 35
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 75
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 5 +randoy
            world.bulletlist[len(world.bulletlist)-1].damage = 9
            world.bulletlist.append(Bullet("sprites/bullet/cyanpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 35
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 75
            world.bulletlist[len(world.bulletlist)-1].yVelocity = -5 +randoy
            world.bulletlist[len(world.bulletlist)-1].damage = 8
            world.bulletlist.append(Bullet("sprites/bullet/cyanpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 35
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 75
            world.bulletlist[len(world.bulletlist)-1].xVelocity = -3.53 +randox*1.41
            world.bulletlist[len(world.bulletlist)-1].yVelocity = -3.53 +randoy*1.41
            world.bulletlist[len(world.bulletlist)-1].damage = 9
            world.bulletlist.append(Bullet("sprites/bullet/cyanpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 35
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 75
            world.bulletlist[len(world.bulletlist)-1].xVelocity = 3.53 +randox*1.41
            world.bulletlist[len(world.bulletlist)-1].yVelocity = -3.53 +randoy*1.41
            world.bulletlist[len(world.bulletlist)-1].damage = 9
            world.bulletlist.append(Bullet("sprites/bullet/cyanpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 35
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 75
            world.bulletlist[len(world.bulletlist)-1].xVelocity = -3.53 +randox*1.41
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 3.53 +randoy*1.41
            world.bulletlist[len(world.bulletlist)-1].damage = 9
            world.bulletlist.append(Bullet("sprites/bullet/cyanpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 35
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 75
            world.bulletlist[len(world.bulletlist)-1].xVelocity = 3.53 +randox*1.41
            world.bulletlist[len(world.bulletlist)-1].yVelocity = 3.53 +randoy*1.41
            world.bulletlist[len(world.bulletlist)-1].damage = 9
            
            
            self.lastshotfired = tick_counter

#Improved shotgun boss, with nicer looking and harder to dodge splash attacks
class enemy_shotgun_boss_2(Boss):
    def __init__(self):
        super().__init__("sprites/boss/shotgun_b2.png")
        self.health = 300
        self.h = 75
        self.w = 75
        self.firerate = 30
        
    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:            
            #rando = random.randint(0,5)
            for i in range(20):
                rando = random.randint(0,5)
                world.bulletlist.append(Bullet("sprites/bullet/cyanpulse.png", screen, 8, 8, False))
                world.bulletlist[len(world.bulletlist)-1].x = self.x + 35
                world.bulletlist[len(world.bulletlist)-1].y = self.y + 75
                world.bulletlist[len(world.bulletlist)-1].xVelocity = math.sin(i*math.pi/10 + rando*math.pi/50)*5
                world.bulletlist[len(world.bulletlist)-1].yVelocity = math.cos(i*math.pi/10 + rando*math.pi/50)*5
                world.bulletlist[len(world.bulletlist)-1].damage = 9
            self.lastshotfired = tick_counter

#Trawler boss. Runs you down and crushes you to death.
class enemy_trawler_boss(EnemyShip):
    def __init__(self):
        super().__init__("sprites/boss/trawler_b.png", screen)
        self.health = 200
        self.yVelocity = 0.5
        self.firerate = 30
        self.lastpunch = 0
        self.punchrate = 12
        self.y = -64
        self.punchVelocity = 15
        self.punchDamage = 12
        self.h = 69
        self.w = 98
        self.health = 150
        self.firerate = 20
        self.maxspeed = 3
        self.punchVelocity = 50
        self.punchDamage = 8
        self.acceleration = 0.2
        

    def tick(self):
        super().tick()
        if self.punchrate + self.lastpunch < tick_counter:
            for i in world.playerlist:
                if colDet(self,i):
                    i.getHit(self.punchDamage)
                    dist = math.sqrt((self.x + (self.w/2) - i.x)**2 + (self.y - (self.h/2) - i.y)**2)
                    i.xVelocity = (self.punchVelocity/dist)*(i.x - self.x - (self.w/2))
                    i.yVelocity = (self.punchVelocity/dist)*(i.y - self.y - (self.h/2))
                    self.lastpunch = tick_counter
        if world.playerlist[0].x-26 < self.x:
            self.xVelocity = self.xVelocity - self.acceleration
        if world.playerlist[0].x-26 > self.x:
            self.xVelocity = self.xVelocity + self.acceleration
        if world.playerlist[0].y < self.y:
            self.yVelocity = self.yVelocity - self.acceleration
        if world.playerlist[0].y > self.y:
            self.yVelocity = self.yVelocity + self.acceleration
        #self.xVelocity = self.xVelocity + ((world.playerlist[0].x-26 - self.x)/100) 
        #self.yVelocity = self.yVelocity + ((world.playerlist[0].y - self.y)/100) 
        #totalVelocity = math.sqrt(self.xVelocity**2+self.yVelocity**2)
        #self.xVelocity = self.xVelocity*(self.maxspeed/totalVelocity)
        #self.yVelocity = self.yVelocity*(self.maxspeed/totalVelocity)
        if self.xVelocity > self.maxspeed:
            self.xVelocity = self.maxspeed
        if self.yVelocity > self.maxspeed:
            self.yVelocity = self.maxspeed
        if self.xVelocity < -1*self.maxspeed:
            self.xVelocity = -1*self.maxspeed
        if self.yVelocity < -1*self.maxspeed:
            self.yVelocity = -1*self.maxspeed
        pict = pygame.image.load('sprites/effects/hud/bar_segment.png')
        pict = pict.convert()
        for i in range(round(self.health/2)):
            screen.blit(pict, (i+10, 10))

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Bullet("sprites/bullet/devpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x - 4
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 8
            world.bulletlist[len(world.bulletlist)-1].xVelocity = -3
            world.bulletlist[len(world.bulletlist)-1].damage = 8
            world.bulletlist.append(Bullet("sprites/bullet/devpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 32
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 8
            world.bulletlist[len(world.bulletlist)-1].xVelocity = 3
            world.bulletlist[len(world.bulletlist)-1].damage = 8 
                
            self.lastshotfired = tick_counter


#Sprayer boss. Shoots heaps of bullets in random directions. RateOfFire: 14400 rounds per minute
class enemy_sprayer_boss(Boss):
    def __init__(self):
        super().__init__("sprites/boss/sprayer_b.png")
        self.firerate = 1
        self.health = 300
        
    def tick(self):
        super().tick()
        self.shoot()
        self.shoot()
        
    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            rando = (random.randint(1, 100)-50)/32 
            world.bulletlist.append(Bullet("sprites/bullet/pinkpulse.png", screen, 8, 8, False))
            world.bulletlist[-1].x = self.x + 35
            world.bulletlist[-1].y = self.y + 39
            world.bulletlist[-1].damage = 5
            world.bulletlist[len(world.bulletlist)-1].xVelocity = math.sin(rando)*6
            world.bulletlist[len(world.bulletlist)-1].yVelocity = math.cos(rando)*6
            world.bulletlist.append(Bullet("sprites/bullet/pinkpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 35
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 39
            world.bulletlist[len(world.bulletlist)-1].damage = 5
            world.bulletlist[len(world.bulletlist)-1].xVelocity = -1*math.sin(rando)*6
            world.bulletlist[len(world.bulletlist)-1].yVelocity = -1*math.cos(rando)*6
            
            self.lastshotfired = tick_counter

#Bomber boss. Fires a whole bunch of fireworks like it's new year's eve.
class enemy_bomber_boss(Boss):
    def __init__(self):
        super().__init__("sprites/boss/bomber_b.png")
        self.firerate = 16
        self.health = 250
        self.h = 63

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Firework("sprites/bullet/biggreenpulse.png", screen, 8, 8))
            world.bulletlist[-1].x = self.x + 35
            world.bulletlist[-1].y = self.y + 63
            world.bulletlist[-1].xVelocity = random.randint(-16,16)/4
            world.bulletlist[-1].yVelocity = random.randint(6,24)/4
            world.bulletlist[-1].rot = (math.pi/2)/random.randint(1,30)
            self.lastshotfired = tick_counter

#Moves quickly around random directions.
class enemy_quick_boss(Boss):
    def __init__(self):
        super().__init__("sprites/boss/quick_b.png")
        self.firerate = 24
        self.health = 200
        self.warptarget = [200,64]
        self.warpprogress = 0
        self.warpvector = [self.x-self.warptarget[0],
                           self.y-self.warptarget[1]]
        self.lastwarp = 0
        self.warprate = 175
        self.h = 75
        self.w = 60
        self.maxspeed = 12
        self.wiggle = False
        self.warpprogress = 0

    def tick(self):
        super().tick()
        self.warp()
        if self.warpprogress < 0.999:
            self.x = self.x-self.warpvector[0]*self.warpprogress
            self.y = self.y-self.warpvector[1]*self.warpprogress
            self.warpprogress = self.warpprogress + 0.1
            self.x = self.x+self.warpvector[0]*self.warpprogress
            self.y = self.y+self.warpvector[1]*self.warpprogress
            
    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(Spark("sprites/bullet/yellowpulse.png", screen, 8, 8)) #Erratic moving bullet
            world.bulletlist[-1].x = self.x + 26
            world.bulletlist[-1].y = self.y + 70
            world.bulletlist[-1].haste = 5
            world.bulletlist[-1].damage = 8
            self.lastshotfired = tick_counter

    def warp(self):
        if self.lastwarp + self.warprate < tick_counter:
            randox = random.randint(0, 325)
            randoy = random.randint(0, 128)
            self.warptarget = [randox,randoy]
            self.lastwarp = tick_counter
            self.warpprogress = 0
            self.warpvector = [self.warptarget[0]-self.x,
                               self.warptarget[1]-self.y]
        
    def die(self):
        world.misclist.append(ScreenObject('sprites/boss/gibs/quick_b_gib_1.png', screen))
        world.misclist[-1].x = self.x
        world.misclist[-1].y = self.y
        world.misclist[-1].xVelocity = -0.1
        world.misclist[-1].yVelocity = -0.4
        world.misclist.append(ScreenObject('sprites/boss/gibs/quick_b_gib_2.png', screen))
        world.misclist[-1].x = self.x
        world.misclist[-1].y = self.y
        world.misclist[-1].xVelocity = 0.2
        world.misclist[-1].yVelocity = 0.4
        world.misclist.append(ScreenObject('sprites/boss/gibs/quick_b_gib_3.png', screen))
        world.misclist[-1].x = self.x
        world.misclist[-1].y = self.y
        world.misclist[-1].xVelocity = -0.3
        world.misclist[-1].yVelocity = 0.3
        world.misclist.append(ScreenObject('sprites/boss/gibs/quick_b_gib_4.png', screen))
        world.misclist[-1].x = self.x
        world.misclist[-1].y = self.y
        world.misclist[-1].xVelocity = -0.1
        world.misclist[-1].yVelocity = 0.4
        super().die()

#Fires walls of bullets that span the whole screen and have strategically placed gaps.
class enemy_brickie_boss(Boss):
    def __init__(self):
        super().__init__("sprites/boss/devnemy_b.png")
        self.firerate = 85
        self.health = 250
        self.w = 84

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            rando = random.randint(0,20)
            rande = random.randint(0,20)
            for i in range(20):
                if i != rando and i!= rande:
                    world.bulletlist.append(Bullet("sprites/bullet/purplepulse.png", screen, 8, 8, False))
                    world.bulletlist[len(world.bulletlist)-1].x = i*20
                    world.bulletlist[len(world.bulletlist)-1].y = self.y + 78
                    world.bulletlist[len(world.bulletlist)-1].yVelocity = 2.5
                    world.bulletlist[len(world.bulletlist)-1].damage = 7
                    world.bulletlist.append(Bullet("sprites/bullet/purplepulse.png", screen, 8, 8, False))
                    world.bulletlist[len(world.bulletlist)-1].x = i*20
                    world.bulletlist[len(world.bulletlist)-1].y = self.y + 78
                    world.bulletlist[len(world.bulletlist)-1].yVelocity = -2.5
                    world.bulletlist[len(world.bulletlist)-1].damage = 7
            self.lastshotfired = tick_counter

#Secret boss
class enemy_seeker_sprayer_boss(Boss):
    def __init__(self):
        super().__init__("sprites/boss/sprayer_b.png")
        self.firerate = 1
        self.health = 300
        
    def tick(self):
        super().tick()
        self.shoot()
        self.shoot()
        
    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            rando = (random.randint(1, 100)-50)/32 
            world.bulletlist.append(SeekingBullet("sprites/bullet/pinkpulse.png", screen, 8, 8))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 35
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 39
            world.bulletlist[len(world.bulletlist)-1].damage = 5
            world.bulletlist[len(world.bulletlist)-1].xVelocity = math.sin(rando)*6
            world.bulletlist[len(world.bulletlist)-1].yVelocity = math.cos(rando)*6
            world.bulletlist[len(world.bulletlist)-1].accrate = 2000
            world.bulletlist.append(Bullet("sprites/bullet/pinkpulse.png", screen, 8, 8, False))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 35
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 39
            world.bulletlist[len(world.bulletlist)-1].damage = 5
            world.bulletlist[len(world.bulletlist)-1].xVelocity = -1*math.sin(rando)*6
            world.bulletlist[len(world.bulletlist)-1].yVelocity = -1*math.cos(rando)*6
            
            self.lastshotfired = tick_counter

# Seeker boss. Spams homing shots in all directions.
class enemy_seeker_boss(Boss):
    def __init__(self):
        super().__init__("sprites/boss/seeker_b.png")
        self.h = 48
        self.health = 180
        self.firerate = 20

    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(SeekingBullet("sprites/bullet/blackpulse.png", screen, 8, 8))
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 35
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 24
            world.bulletlist[len(world.bulletlist)-1].damage = 8
            dice = random.randint(0,3)
            if dice == 0:
                world.bulletlist[len(world.bulletlist)-1].yVelocity = 20
            if dice == 1:
                world.bulletlist[len(world.bulletlist)-1].yVelocity = -20
            if dice == 2:
                world.bulletlist[len(world.bulletlist)-1].xVelocity = 20
            if dice == 3:
                world.bulletlist[len(world.bulletlist)-1].xVelocity = -20
            self.lastshotfired = tick_counter

#Fires a whole bunch of bullets that orbit the boss
class enemy_hellion_boss(Boss):
    def __init__(self):
        super().__init__("sprites/boss/hellion_b.png")
        self.health = 250
        self.stoppingPoint = 140
        self.firerate = 8
        
    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:
            world.bulletlist.append(OrbitingBullet("sprites/bullet/greenpulse.png", screen, 8, 8, False))
            rando = random.randint(-2,2)
            world.bulletlist[len(world.bulletlist)-1].x = self.x + 30
            world.bulletlist[len(world.bulletlist)-1].y = self.y + 78 + rando
            world.bulletlist[len(world.bulletlist)-1].xtarget = self.x + 33
            world.bulletlist[len(world.bulletlist)-1].ytarget = self.y + 78
            world.bulletlist[len(world.bulletlist)-1].damage = 4
            world.bulletlist[len(world.bulletlist)-1].fanspeed = 2
            world.bulletlist[len(world.bulletlist)-1].maxspeed = 3
            copyBullets(world.bulletlist[len(world.bulletlist)-1],
                        [[self.x + 36, self.y + 78 - rando],
                         [self.x + 33 - rando, self.y + 75],
                         [self.x + 33 + rando, self.y + 81],
                         ],
                        [[0,0],[0,0],[0,0]])
            self.lastshotfired = tick_counter

#AA
class enemy_time_boss(Boss):
    def __init__(self):
        super().__init__("sprites/boss/shotgun_b.png")
        self.health = 240
        self.h = 75
        self.w = 75
        self.firerate = 1
        self.i = 0
        
    def shoot(self):
        if tick_counter - self.firerate >  self.lastshotfired:     
            #for i in range(20):
            #i = random.randint(0,19)
            i = self.i
            world.bulletlist.append(DyingBullet("sprites/bullet/cyanpulse.png", screen, 8, 8, False))
            world.bulletlist[-1].x = player.x - 500*math.sin(i*math.pi/10)
            world.bulletlist[-1].y = player.y - 500*math.cos(i*math.pi/10)
            world.bulletlist[-1].xVelocity = math.sin(i*math.pi/10)*5
            world.bulletlist[-1].yVelocity = math.cos(i*math.pi/10)*5
            world.bulletlist[-1].damage = 2
            world.bulletlist[-1].despawn = False
            self.i = (self.i + 1)%20
            self.lastshotfired = tick_counter
#STRONGBOSS------------------------------------------------------------------------------------------#
class enemy_sniper_boss_strong(enemy_sniper_boss_2):
    def __init__(self):
        super().__init__()
        self.lastspawn = tick_counter
        self.spawnrate = 240
        self.damage = 8
        self.child = enemy_sniper_wave

    def tick(self):
        super().tick()
        if self.spawnrate + self.lastspawn < tick_counter:
            world.enemylist.append(self.child())
            world.enemylist[-1].y = -30
            world.enemylist[-1].x = random.randint(30,360)
            self.lastspawn = tick_counter

class enemy_burst_boss_strong(enemy_burst_boss):
    def __init__(self):
        super().__init__()
        self.lastspawn = tick_counter
        self.spawnrate = 240
        self.child = enemy_burst

    def tick(self):
        super().tick()
        if self.spawnrate + self.lastspawn < tick_counter:
            world.enemylist.append(self.child())
            world.enemylist[-1].y = -30
            world.enemylist[-1].x = random.randint(30,360)
            self.lastspawn = tick_counter

class enemy_trawler_boss_strong(enemy_trawler_boss):
    def __init__(self):
        super().__init__()
        self.lastspawn = tick_counter
        self.spawnrate = 720
        self.firerate = 30
        self.child = enemy_trawler
    
    def tick(self):
        super().tick()
        if self.spawnrate + self.lastspawn < tick_counter:
            world.enemylist.append(self.child())
            world.enemylist[-1].y = -30
            world.enemylist[-1].x = self.x + 36
            self.lastspawn = tick_counter

class enemy_shotgun_boss_strong(enemy_shotgun_boss_2):
    def __init__(self):
        super().__init__()
        self.lastspawn = tick_counter
        self.spawnrate = 240
        self.child = enemy_shotgun_wave

    def tick(self):
        super().tick()
        if self.spawnrate + self.lastspawn < tick_counter:
            world.enemylist.append(self.child())
            world.enemylist[-1].y = -30
            world.enemylist[-1].x = random.randint(30,360)
            self.lastspawn = tick_counter

class enemy_brickie_boss_strong(enemy_brickie_boss):
    def __init__(self):
        super().__init__()
        self.lastspawn = tick_counter - 400
        self.spawnrate = 480
        self.child = enemy_brickie_wave

    def tick(self):
        super().tick()
        if self.spawnrate + self.lastspawn < tick_counter:
            world.enemylist.append(self.child())
            world.enemylist[-1].y = -30
            world.enemylist[-1].x = random.randint(30,360)
            self.lastspawn = tick_counter

class enemy_quick_boss_strong(enemy_quick_boss):
    def __init__(self):
        super().__init__()
        self.lastspawn = tick_counter
        self.spawnrate = 180
        self.child = enemy_quick

    def tick(self):
        super().tick()
        if self.spawnrate + self.lastspawn < tick_counter:
            world.enemylist.append(self.child())
            world.enemylist[-1].y = -30
            world.enemylist[-1].x = self.x + 30
            self.lastspawn = tick_counter

class enemy_sprayer_boss_strong(enemy_sprayer_boss):
    def __init__(self):
        super().__init__()
        self.lastspawn = tick_counter
        self.spawnrate = 240
        self.child = enemy_bomber

    def tick(self):
        super().tick()
        if self.spawnrate + self.lastspawn < tick_counter:
            world.enemylist.append(self.child())
            world.enemylist[-1].y = -30
            world.enemylist[-1].x = random.randint(30,360)
            self.lastspawn = tick_counter

class enemy_bomber_boss_strong(enemy_bomber_boss):
    def __init__(self):
        super().__init__()
        self.lastspawn = tick_counter
        self.spawnrate = 240
        self.child = enemy_sprayer

    def tick(self):
        super().tick()
        if self.spawnrate + self.lastspawn < tick_counter:
            world.enemylist.append(self.child())
            world.enemylist[-1].y = -30
            world.enemylist[-1].x = random.randint(30,360)
            self.lastspawn = tick_counter

class enemy_seeker_boss_strong(enemy_seeker_boss):
    def __init__(self):
        super().__init__()
        self.lastspawn = tick_counter
        self.spawnrate = 480
        self.child = enemy_hellion_wave

    def tick(self):
        super().tick()
        if self.spawnrate + self.lastspawn < tick_counter:
            world.enemylist.append(self.child())
            world.enemylist[-1].y = -30
            world.enemylist[-1].x = random.randint(30,360)
            self.lastspawn = tick_counter

class enemy_hellion_boss_strong(enemy_hellion_boss):
    def __init__(self):
        super().__init__()
        self.lastspawn = tick_counter
        self.spawnrate = 480
        self.child = enemy_seeker

    def tick(self):
        super().tick()
        if self.spawnrate + self.lastspawn < tick_counter:
            world.enemylist.append(self.child())
            world.enemylist[-1].y = -30
            world.enemylist[-1].x = random.randint(30,360)
            self.lastspawn = tick_counter
            
#----------------------------------------------------------------------------------------------------#
#Endlessly spawns enemies. Spawn rates gradually get faster.
class endlessLevel(Entity):
    def __init__(self):
        self.nextspawn = 90
        self.pool = [enemy_sniper, enemy_sniper_wave, enemy_burst, enemy_burst_wave,
                     enemy_shotgun, enemy_shotgun_wave, enemy_trawler, enemy_trawler_wave,
                     enemy_sprayer, enemy_sprayer_wave, enemy_bomber, enemy_bomber_wave,
                     enemy_brickie, enemy_brickie_wave, enemy_quick, enemy_quick_wave,
                     enemy_seeker, enemy_seeker_wave, enemy_hellion, enemy_hellion_wave
                     ]
        self.bosses = [enemy_sniper_boss(), enemy_shotgun_boss(), enemy_trawler_boss(),
                       enemy_burst_boss(), enemy_sprayer_boss(), enemy_seeker_boss()
                       ]
        self.finished = False
        self.delay = 120

    def tick(self):
        if len(world.enemylist) == 0 and (self.nextspawn - 105) > tick_counter:
            self.nextspawn = tick_counter + 105
        if self.nextspawn < tick_counter:
            if random.randint(0,3):
                self.spawn()
            else:
                self.spawn
                self.spawn
                
    def spawn(self):
        enemySpawn(self.pool[random.randint(0,len(self.pool)-1)],random.randint(30,360))
        self.nextspawn = tick_counter + self.delay + random.randint(0,10)
        if self.delay > 60:
            self.delay = self.delay - 3

#/---------------------------------------------------------------------------------------------------\
#\---------------------------------------------------------------------------------------------------/
test = [5,
        [enemy_time_boss, 40, 0],
       ]

endless_bg = 128, 32, 192
#/---------------------------------------------------------------------------------------------------\
#\------------------------------------------!!LEVEL LISTS!!------------------------------------------/

geolyte = [5,
           [tutorial_move, 0, 5],

           [enemy_sniper_weak, 55, 0],
           [tutorial_shoot, 30, 30],
           
           [enemy_sniper_weak, 25, 0],
           [enemy_sniper_weak, 75, 30],
           
           [tutorial_health_1, 0, 0],
           [tutorial_health_2, 0, 0],
           [enemy_sniper_weak, 8,  1],
           [enemy_sniper_weak, 50, 1],
           [enemy_sniper_weak, 92, 30],

           [enemy_sniper_weak, 44, 2],
           [enemy_sniper_weak, 12, 2],
           [enemy_sniper_weak, 84, 2],
           [enemy_sniper_weak, 31, 2],
           [enemy_sniper_weak, 71, 2],
           [enemy_sniper_weak, 90, 20],

           [tutorial_kit, 0, 0],
           [enemy_sniper_health, 66, 30],
           
           [enemy_sniper_weak, 10, 0],
           [enemy_sniper_weak, 20, 4],
           [tutorial_alt, 0, 0],
           [enemy_sniper_weak, 80, 0],
           [enemy_sniper_weak, 90, 4],
           [enemy_sniper_weak, 40, 0],
           [enemy_sniper_weak, 50, 30],
           
           [tutorial_cooldown_1, 0, 0],
           [tutorial_cooldown_2, 0, 0],

           [enemy_sniper_weak, 28, 3],
           [enemy_sniper_weak, 58, 30],
           
           [enemy_sniper_weak, 8,  0],
           [enemy_sniper_weak, 92, 0.5],
           [enemy_sniper_weak, 31, 0],
           [enemy_sniper_weak, 66, 0.5],
           [enemy_sniper_weak, 50, 0.5],
           [enemy_sniper_weak, 16, 0],
           [enemy_sniper_weak, 84, 150],
           
           [enemy_sniper_health, 64, 20],

           [blank, 5, 5],

           [enemy_sniper_weak_boss, 40, 0],
          ]

geolyte_bg = 90,160,170

ignius = [5,
         [enemy_burst, 45, 15],

         [enemy_burst, 60, 15],

         [enemy_burst_wave, 30, 15],

         [enemy_burst_wave, 30, 2],
         [enemy_burst_wave, 50, 2],
         [enemy_burst_wave, 80, 2],

         [enemy_sniper_wave, 80, 15],

         [enemy_burst_wave, 15, 0],
         [enemy_burst_wave, 80, 2],
         [enemy_sniper_wave, 50, 5],

         [enemy_trawler,50,15],

         [enemy_trawler_wave,40,2],
         [enemy_burst_health,60,15],##

         [enemy_burst, 21, 0],
         [enemy_burst, 79, 1],
         [enemy_burst, 45, 1],
         [enemy_trawler, 45, 2],
         [enemy_sniper_wave, 30, 0],
         [enemy_sniper_wave, 63, 12],

         [enemy_burst, 10, 0.5],
         [enemy_burst, 30, 0.5],
         [enemy_burst, 50, 0.5],
         [enemy_burst, 70, 0.5],
         [enemy_burst, 90, 12],

         [enemy_burst_wave, 23, 0],
         [enemy_burst_wave, 46, 1],
         [enemy_sniper, 5, 0],
         [enemy_sniper, 90, 1],
         [enemy_trawler_health, 50, 60],##

         [enemy_burst_boss, 40, 0],
        ]

ignius_bg = 180,120,100

oleana = [5,
          [enemy_shotgun, 30, 20],

          [enemy_shotgun, 30, 0],
          [enemy_shotgun, 65, 2],
          [enemy_shotgun_wave, 42, 20],

          [enemy_shotgun, 15, 0],
          [enemy_shotgun, 75, 2],
          [enemy_trawler, 40, 2],
          [enemy_shotgun, 40, 5],
          [enemy_burst_wave, 50, 20],
          
          [enemy_shotgun, 75, 0],
          [enemy_shotgun, 35, 2],
          [enemy_shotgun, 45, 5],

          [enemy_burst_wave, 45, 2],
          [enemy_burst, 45, 12],

          [enemy_shotgun_health, 22, 30],##

          [enemy_shotgun_wave, 52, 2],
          [enemy_shotgun_wave, 32, 1],
          [enemy_shotgun_wave, 12, 20],

          [enemy_burst, 30, 0],
          [enemy_burst, 64, 1],
          [enemy_shotgun, 15, 0],
          [enemy_shotgun, 82, 2],
          [enemy_burst_wave, 47, 10],

          [enemy_burst_wave, 45, 0],
          [enemy_shotgun_health, 22, 1],##
          [enemy_burst_wave, 45, 1],
          [enemy_shotgun, 71, 8],

          [enemy_shotgun_wave, 72, 2],
          [enemy_shotgun_wave, 12, 2],
          [enemy_shotgun_wave, 30, 2],
          [enemy_trawler_wave, 45, 3],
          [enemy_shotgun_wave, 64, 2],
          [enemy_trawler_wave, 45, 12],
          
          [enemy_burst_wave, 82, 1],
          [enemy_burst_wave, 12, 24],
        
          [enemy_trawler_wave, 45, 1],
          [enemy_shotgun_health, 45, 60],##
          
          [enemy_shotgun_boss_2, 40, 0]
         ]

oleana_bg = 100, 120, 180

anasaze = [7,
           [enemy_trawler, 21, 0],
           [enemy_trawler, 46, 0],
           [enemy_trawler, 71, 5],

           [enemy_burst_wave, 33, 0],
           [enemy_burst_wave, 67, 30],

           [enemy_brickie, 45, 30],

           [enemy_trawler, 44, 1],
           [enemy_brickie, 45, 10],

           [enemy_burst_wave, 23, 1],
           [enemy_burst_wave, 72, 15],

           [enemy_burst_wave, 24, 0.5],
           [enemy_burst_wave, 14, 0],
           [enemy_brickie_wave, 72, 0.5],
           [enemy_burst_wave, 69, 4],
           [enemy_trawler, 46, 9],

           [enemy_burst, 12, 1],
           [enemy_trawler_health, 55, 1],##
           [enemy_burst, 86, 1],
           [enemy_trawler, 40, 3],
           [enemy_brickie_wave, 47, 9],

           [enemy_trawler, 30, 0],
           [enemy_trawler, 64, 3.5],
           [enemy_brickie_wave, 30, 0],
           [enemy_brickie_wave, 64, 7],

           [enemy_burst, 40, 12],

           [enemy_brickie, 12, 1],
           [enemy_brickie_wave, 70, 1],
           [enemy_trawler_wave, 52, 1],
           [enemy_trawler_wave, 31, 10],

           [enemy_burst, 10, 0],
           [enemy_burst, 85, 0.5],
           [enemy_burst, 25, 0],
           [enemy_burst, 60, 1],
           [enemy_trawler_health, 46, 30],##

           [blank, 0, 3],

           [enemy_trawler_boss, 45, 0],

           
          ]

anasaze_bg = 180, 160, 100

megadom = [5,
           [enemy_sprayer, 21, 10],

           [enemy_sprayer, 53, 0],
           [enemy_sprayer, 12, 10],
           
           [enemy_sprayer, 66, 0],
           [enemy_sprayer, 30, 3],
           [enemy_shotgun, 47, 3],
           [enemy_sniper, 72, 12],

           [enemy_sprayer, 76, 0],
           [enemy_sprayer, 16, 1],
           [enemy_shotgun, 46, 4],
           [enemy_sniper_wave, 30, 0],
           [enemy_sniper_wave, 63, 9],

           [enemy_sprayer_wave, 23, 0.5],
           [enemy_shotgun_wave, 80, 6],

           [enemy_sprayer_wave, 44, 1],
           [enemy_sniper_wave, 15, 0],
           [enemy_sniper_wave, 75, 0],
           [enemy_sniper, 45, 8],

           [enemy_shotgun_health, 23, 8],##

           [enemy_sprayer, 35, 0],
           [enemy_sprayer, 55, 2],
           [enemy_sniper, 35, 0],
           [enemy_sniper, 55, 15],

           [enemy_sprayer, 16, 0],
           [enemy_sprayer, 46, 0],
           [enemy_sprayer, 76, 2],
           [enemy_shotgun, 46, 8],

           [enemy_shotgun_wave, 34, 1],
           [enemy_sniper_wave, 34, 1],
           [enemy_shotgun_wave, 68, 1],
           [enemy_sniper_wave, 68, 7],

           [enemy_sprayer_wave, 46, 2],
           [enemy_sprayer_health, 46, 15],##

           [blank, 2, 1],

           [enemy_sprayer_boss, 40, 0]
           ]

megadom_bg = 120, 160, 120

grannest = [5,
            [enemy_quick, 46, 30], #1
            
            [enemy_quick, 21, 0],
            [enemy_quick, 71, 10], #2
            
            [enemy_quick, 61, 0],
            [enemy_quick, 31, 1],
            [enemy_brickie, 46, 10], #3

            [enemy_quick_wave, 23, 5],
            [enemy_quick_wave, 85, 5],
            [enemy_quick_wave, 38, 10], #4
            
            [enemy_quick_wave, 16, 2],
            [enemy_quick_wave, 45, 2],
            [enemy_quick_wave, 76, 2],
            [enemy_quick_wave, 45, 2],
            [enemy_quick_wave, 16, 6], #5

            [enemy_quick_wave, 24, 0.3],
            [enemy_quick_wave, 24, 0.3],
            [enemy_quick_wave, 24, 10], #6

            [enemy_brickie_health, 44, 5],

            [enemy_quick_wave, 76, 0.3],
            [enemy_quick_wave, 76, 0.3],
            [enemy_quick_wave, 76, 5], #7

            [enemy_quick_wave, 45, 0.3],
            [enemy_quick_wave, 45, 0.3],
            [enemy_quick_wave, 45, 7],  #8

            [enemy_quick_health, 60, 1],
            [enemy_burst, 40, 2],
            [enemy_burst, 12, 3],
            [enemy_quick, 77, 2],
            [enemy_burst_wave, 34, 0],
            [enemy_quick_wave, 68, 3],
            [enemy_burst_wave, 14, 2], #9
            [enemy_quick, 20, 0],
            [enemy_quick, 76, 10],

            [enemy_quick, 16, 0],
            [enemy_quick, 76, 0.5],
            [enemy_quick_wave, 32, 0], #10
            [enemy_quick_wave, 61, 2],
            [enemy_brickie, 22, 0],
            [enemy_brickie, 82, 8],

            [enemy_burst_wave, 73, 0.3], #11
            [enemy_brickie_health, 22, 0],
            [enemy_burst_wave, 73, 0.3],
            [enemy_burst_wave, 73, 0.3],
            [enemy_quick_wave, 73, 60],

            [enemy_quick_boss, 40, 0], #12
            ]

grannest_bg = 120, 100, 140

bavoom = [5,
          [enemy_sniper, 32, 3],
          [enemy_sniper, 64, 7],

          [enemy_sniper, 12, 0],
          [enemy_sniper, 80, 1],
          [enemy_sniper, 46, 5],

          [enemy_burst, 29, 0],
          [enemy_burst, 62, 3],
          [enemy_sniper, 29, 0],
          [enemy_sniper, 62, 12],

          [enemy_burst, 12, 1],
          [enemy_burst, 62, 1],
          [enemy_burst, 88, 1],
          [enemy_burst, 35, 1],
          [enemy_sniper, 12, 1],
          [enemy_sniper, 62, 1],
          [enemy_sniper, 88, 1],
          [enemy_sniper, 35, 12],
          
          [enemy_sniper_health, 21, 6],
          [blank, 0, 2],

          [enemy_sniper,  6, 0.5],
          [enemy_sniper, 16, 0.5],
          [enemy_sniper, 26, 0.5],
          [enemy_sniper, 36, 0.5],
          [enemy_sniper, 46, 0.5],
          [enemy_sniper, 56, 0.5],
          [enemy_sniper, 66, 0.5],
          [enemy_sniper, 76, 0.5],
          [enemy_sniper, 86, 20],

          [enemy_sniper_health, 46, 12],

          [enemy_sniper, 24, 0.5],
          [enemy_sniper, 67, 0.5],
          [enemy_sniper, 24, 0.5],
          [enemy_sniper, 67, 0.5],
          [enemy_sniper, 20, 0.5],
          [enemy_sniper, 71, 0.5],
          [enemy_sniper, 20, 0.5],
          [enemy_sniper, 71, 15],

          [enemy_brickie, 46, 3],
          [enemy_sniper_wave, 46, 1],
          [enemy_sniper_health, 46, 8],

          [enemy_brickie, 36, 0],
          [enemy_brickie, 56, 2],
          [enemy_sniper, 36, 0],
          [enemy_sniper, 56, 2],
          [enemy_brickie, 46, 12],

          [enemy_sniper, 14, 0],
          [enemy_sniper, 78, 1],
          [enemy_brickie, 14, 0],
          [enemy_brickie, 78, 1],
          [enemy_brickie_wave, 44, 9],

          [enemy_brickie, 14, 0.5],
          [enemy_sniper_health, 14, 30],
          
          [enemy_sniper_boss_2, 40, 0],
         ]

bavoom_bg = 170, 180, 140

boggob = [5,
          [enemy_bomber, 45, 10],#1
          
          [enemy_bomber_wave, 24, 8], #2

          [enemy_bomber, 31, 1],
          [enemy_shotgun, 59, 8], #3

          [enemy_shotgun_wave, 25, 0],
          [enemy_shotgun_wave, 65, 1],
          [enemy_bomber_wave, 45, 4],
          [enemy_trawler, 45, 10], #4

          [enemy_trawler_wave, 20, 1.5],
          [enemy_bomber_wave, 30, 0],
          [enemy_shotgun_wave, 80, 2],
          [enemy_trawler, 50, 10], #5

          [enemy_shotgun, 82, 0],
          [enemy_shotgun, 10, 1],
          [enemy_bomber, 46, 10], #6

          [enemy_bomber, 16, 1],
          [enemy_bomber, 76, 1],
          [enemy_bomber_health, 20, 1],
          [enemy_bomber, 72, 16],#7

          [enemy_shotgun, 32, 0.5],
          [enemy_shotgun, 5, 0.5],
          [enemy_shotgun, 70, 1],
          [enemy_bomber, 33, 1],
          [enemy_bomber, 69, 12], #8

          [enemy_bomber, 8,  0],
          [enemy_bomber, 92, 0.5],
          [enemy_shotgun_health, 31, 0],
          [enemy_shotgun, 66, 0.5],
          [enemy_shotgun, 50, 5],   #9
          [enemy_trawler_wave, 46, 12],
          
          [enemy_bomber, 94, 1],
          [enemy_bomber_wave, 34, 2],
          [enemy_bomber, 78, 1],
          [enemy_bomber_wave, 54, 2],
          [enemy_bomber, 20, 1],
          [enemy_bomber_wave, 85, 19], #10


          [enemy_trawler_health, 15, 15], #11
          [blank, 1, 0],

          [enemy_bomber_boss, 45, 0], #12
         ]
boggob_bg = 90, 160, 100

freaze = [5,
          [enemy_brickie, 46, 10],

          [enemy_brickie, 20, 1],
          [enemy_shotgun, 75, 10],

          [enemy_shotgun, 46, 1],
          [enemy_brickie, 46, 2],
          [enemy_shotgun, 26, 0],
          [enemy_shotgun, 79, 10],

          [enemy_brickie, 40, 1],
          [enemy_shotgun, 78, 1],
          [enemy_brickie, 23, 2],
          [enemy_brickie, 68, 1],
          [enemy_shotgun, 82, 3],
          [enemy_sniper, 31, 2],
          [enemy_brickie, 46, 2],
          [enemy_brickie, 41, 1],
          [enemy_shotgun, 52, 3],
          [enemy_brickie_wave, 28, 2],
          [enemy_sniper_wave, 71, 1],
          [enemy_shotgun, 27, 2],
          [enemy_shotgun, 56, 3],
          [enemy_sniper, 60, 8],

          [enemy_brickie_health, 21, 10],

          [enemy_brickie, 35, 0],
          [enemy_shotgun, 69, 1],
          [enemy_sniper,  24, 1],
          [enemy_shotgun, 19, 2],
          [enemy_brickie_wave, 55, 0],
          [enemy_brickie_wave, 76, 2],
          [enemy_shotgun_wave, 30, 1],
          [enemy_sniper_wave,  89, 1],
          [enemy_shotgun, 29, 0],
          [enemy_shotgun, 62, 2],
          [enemy_brickie, 82, 1],
          [enemy_shotgun, 13, 1],
          [enemy_shotgun, 90, 16],

          [enemy_brickie, 20, 1],
          [enemy_brickie, 40, 1],
          [enemy_brickie, 60, 1],
          [enemy_brickie, 80, 10],

          [enemy_shotgun_health, 46, 10],

          [enemy_brickie_boss, 44, 0],
          ]

freaze_bg = 140, 140, 180

layazero = [5,
            [enemy_hellion, 30, 12],

            [enemy_hellion, 26, 1],
            [enemy_hellion, 66, 10],

            [enemy_hellion, 55, 1],
            [enemy_shotgun, 80, 10],

            [enemy_shotgun, 20, 0],
            [enemy_shotgun, 80, 1],
            [enemy_hellion, 46, 10],
            
            [enemy_hellion_wave, 26, 3],
            [enemy_hellion_wave, 66, 10],

            [enemy_quick_wave, 56, 0],
            [enemy_hellion, 67, 10],

            [enemy_hellion, 21, 0],
            [enemy_hellion, 71, 2],
            [enemy_hellion_health, 56, 10],

            [enemy_shotgun, 46, 1],
            [enemy_quick_wave, 76, 1],
            [enemy_quick_wave, 23, 2],
            [enemy_hellion_wave, 46, 1],
            [enemy_quick_wave, 46, 10],

            [enemy_shotgun, 32, 0],
            [enemy_shotgun, 60, 2],
            [enemy_hellion, 21, 0],
            [enemy_hellion_health, 71, 10],

            [enemy_hellion, 80, 2],
            [enemy_shotgun, 80, 0],
            [enemy_hellion, 30, 2],
            [enemy_shotgun, 30, 0],
            [enemy_hellion, 50, 2],
            [enemy_quick_wave, 46, 10],

            [enemy_shotgun, 43, 1],
            [enemy_quick_wave, 62, 0.5],
            [enemy_quick_wave, 32, 1],
            [enemy_shotgun_wave, 20, 2],
            [enemy_shotgun, 82, 1],
            [enemy_hellion_wave, 54, 10],

            [enemy_hellion_health, 34, 60],
            
            [enemy_hellion_boss, 45, 0],
            ]

layazero_bg = 50, 120, 30

dawndus = [5,
           [enemy_seeker, 25, 10],

           [enemy_seeker_wave, 70, 10],

           [enemy_sniper, 24, 2],
           [enemy_seeker, 61, 10],

           [enemy_sniper, 32, 1],
           [enemy_sniper_wave, 56, 1],
           [enemy_sniper, 80, 1],
           [enemy_seeker, 46, 10],

           [enemy_seeker, 20, 0],
           [enemy_seeker, 72, 10],

           [enemy_sprayer_wave, 40, 2],
           [enemy_seeker, 15, 2],
           [enemy_seeker_wave, 72, 10],

           [enemy_sniper, 44, 1],
           [enemy_sprayer, 72, 0],
           [enemy_sniper, 24, 1],
           [enemy_seeker_health, 58, 2],
           [enemy_sniper_wave, 65, 10],

           [enemy_seeker_wave, 31, 1],
           [enemy_seeker_wave, 67, 1],
           [enemy_sprayer_wave, 46, 5],
           [enemy_seeker, 10, 10],

           [enemy_seeker, 23, 1],
           [enemy_seeker, 82, 1],
           [enemy_seeker, 46, 1],
           [enemy_seeker, 64, 2],
           [enemy_sniper_wave, 46, 3],

           [enemy_sprayer, 29, 0],
           [enemy_sprayer, 62, 2],
           [enemy_seeker, 46, 2],
           [enemy_sniper_wave, 46, 10],

           [enemy_sprayer, 46, 2],
           [enemy_seeker, 25, 0],
           [enemy_seeker, 67, 2],
           [enemy_sprayer_wave, 46, 10],

           [enemy_seeker_health, 27, 10],

           [enemy_seeker_boss, 44, 10],
        ]

dawndus_bg = 180, 70, 130

def formatObject(button, x, y, w=64, h=32):
    button.x = x
    button.y = y
    button.h = h
    button.w = w

#____________________________________________MAIN LOOP____________________________________________#

clock = pygame.time.Clock()
tick_counter = 0
startgame = False
thislevel = None
bg = None
scrap = 0
reward = 0

#Special type of button that loads a new level when clicked
class Planet(Button):
    def __init__(self, imageFileName, screen, level, background, spoils=0):
        super().__init__(imageFileName, screen)
        self.level = level
        self.bg = background
        self.spoils = spoils
        self.completed = False
        self.prereq = []

    def tick(self):
        unlocked = True
        for i in self.prereq:
            if not i.completed:
                unlocked = False
            else:
                unlocked = True
                break
        if unlocked:
            super().tick()
            global startgame
            global thislevel
            global bg
            global reward
            if self.pressed:
                startgame = True 
                thislevel = Level(self.level)
                thislevel.planet = self
                bg = self.bg
                reward = self.spoils
            if self.completed:
                pict = pygame.image.load("sprites\effects\hud\\altfire_ready.png")
                pict = pict.convert()
                pict.set_colorkey((255,0,255))
                screen.blit(pict, (self.x, self.y))

#Planet map list
geo_map = Planet('sprites/buttons/planet_geolyte.png', screen, geolyte, geolyte_bg, 30)
formatObject(geo_map, 184, 50, 32)
ign_map = Planet('sprites/buttons/planet_ignius.png', screen, ignius, ignius_bg, 20)
ign_map.prereq = [geo_map]
formatObject(ign_map, 184, 100, 32)
ana_map = Planet('sprites/buttons/planet_anasaze.png', screen, anasaze, anasaze_bg, 10)
ana_map.prereq = [ign_map]
formatObject(ana_map, 140, 150, 32)
ole_map = Planet('sprites/buttons/planet_oleana.png', screen, oleana, oleana_bg, 10)
ole_map.prereq = [ign_map]
formatObject(ole_map, 224, 150, 32)
meg_map = Planet('sprites/buttons/planet_megadom.png', screen, megadom, megadom_bg, 10)
meg_map.prereq = [ole_map]
formatObject(meg_map, 315, 170, 32)
gra_map = Planet('sprites/buttons/planet_grannest.png', screen, grannest, grannest_bg, 20)
gra_map.prereq = [ana_map]
formatObject(gra_map, 104, 220, 32)
bav_map = Planet('sprites/buttons/planet_bavoom.png', screen, bavoom, bavoom_bg, 10)
bav_map.prereq = [ana_map]
formatObject(bav_map, 46, 170, 32)
bog_map = Planet('sprites/buttons/planet_boggob.png', screen, boggob, boggob_bg, 20)
bog_map.prereq = [ole_map]
formatObject(bog_map, 264, 220, 32)
laz_map = Planet('sprites/buttons/planet_layazero.png', screen, layazero, layazero_bg, 30)
laz_map.prereq = [gra_map, bav_map]
formatObject(laz_map, 30, 250, 32)
daw_map = Planet('sprites/buttons/planet_dawndus.png', screen, dawndus, dawndus_bg, 30)
daw_map.prereq = [bog_map, meg_map]
formatObject(daw_map, 333, 250, 32)
fre_map = Planet('sprites/buttons/planet_freaze.png', screen, freaze, freaze_bg, 20)
fre_map.prereq = [gra_map, bog_map]
formatObject(fre_map, 184, 240, 32)
endless = Button('sprites/buttons/planet_endless.png', screen)
endless.x = 368
endless.y = 568
endless.w = 32
upgrade = Button('sprites/buttons/button_generic.png', screen)
upgrade.x = 300
upgrade.y = 10
testmap = Button('sprites/buttons/planet_generic.png', screen)
formatObject(testmap, 0, 500, 32)
maplist = [ geo_map, ign_map, ana_map, ole_map, meg_map, gra_map, bav_map,
            bog_map, laz_map, daw_map, fre_map,
            ]
maplist_2 = [ endless, upgrade, testmap]
equippedWep = weapon_generic
equippedAlt = altfire_rocket



class ItemSelect(Button):
    def __init__(self, imageFileName, screen, mainslot=True):
        super().__init__(imageFileName, screen)
        self.weapon = weapon_orbiter
        self.mainslot = mainslot
        
    def tick(self):
        super().tick()
        global equippedWep
        global equippedAlt
        pict = pygame.image.load("sprites/buttons/equip_overlay.png")
        pict = pict.convert()
        pict.set_colorkey((255,0,255))
        if self.weapon == equippedWep:
            screen.blit(pict, (self.x, self.y))
        if self.weapon == equippedAlt:
            screen.blit(pict, (self.x, self.y))
            
        if self.pressed:
            if self.mainslot:
                equippedWep = self.weapon
            else:
                equippedAlt = self.weapon

#Applies the upgrades to the player ship
def applyUpgrades(player, gun, hull, thrust, alt):
    if gun > 1:
        player.fireratemod = 0.8
    if gun > 2:
        player.shotspeedmod = 1.5
    if gun > 3:
        player.damagemod = 1.25
    if gun > 4:
        player.damagemod = 1.5
    if hull > 1:
        player.maxhealth = 120
        player.health = 120
    if hull > 2:
        player.barrierallowed = True
    if hull > 3:
        player.maxhealth = 140
        player.health = 140
    if hull > 4:
        player.barrierchargerate = 300
    if thrust > 1:
        player.maxspeed = 6
    if thrust > 2:
        player.candodge = True
        player.dodgerate = 3
        player.dodgedistance = 12
    if thrust > 3:
        player.dodgedistance = 24
    if thrust > 4:
        player.gravitywell = True
    if alt > 1:
        player.altfiremod = 1.5
    if alt > 2:
        player.cooldownmod = 0.8
    if alt > 3:
        player.altfiremod = 2
    if alt > 4:
        player.cooldownmod = 0.6

class Upgrade(Button):
    def __init__(self, imageFileName, screen):
        super().__init__(imageFileName, screen)
        self.upgrade = None
        self.active = False
        self.cost = 0
        self.held = False

    def tick(self):
        super().tick()
        global scrap
        pict = pygame.image.load("sprites/buttons/upgrade_overlay.png")
        pict = pict.convert()
        pict.set_colorkey((255,0,255))        
        label = mainfont.render("ϕ"+str(self.cost), 1, (255,255,200))
        screen.blit(label, (self.x + 16, self.y+16))
        if self.active:
            screen.blit(pict, (self.x, self.y))
        if self.held:
            if not self.pressed:
                self.held = False
        if self.pressed and not self.held:
            self.held = True
            if self.active:
                self.active = False
                scrap = scrap + self.cost
            elif scrap >= self.cost:
                self.active = True
                scrap = scrap - self.cost
        
    def check(self, player):
        pass


class DifficultySwitch(Button):
    def __init__(self, imageFileName, screen):
        super().__init__(imageFileName, screen)
        self.held = False

    def tick(self):
        super().tick()
        global hardmode
        pict = pygame.image.load("sprites/buttons/hardmode_overlay.png")
        pict = pict.convert()
        pict.set_colorkey((255,0,255))        
        if hardmode:
            screen.blit(pict, (self.x, self.y))
        if not self.pressed:
            self.held = False
        if self.pressed and not self.held:
            self.held = True
            if hardmode:
                hardmode = False
            else:
                hardmode = True

    
#gun upgrades
class upgrade_power(Upgrade):
    def __init__(self):
        super().__init__("sprites/buttons/button_upgrade_power.png", screen)
        self.cost = 100

    def check(self, player):
        player.damagemod = 1.35

class upgrade_firerate(Upgrade):
    def __init__(self):
        super().__init__("sprites/buttons/button_upgrade_firerate.png", screen)
        self.cost = 80

    def check(self, player):
        player.fireratemod = 0.8

class upgrade_shotspeed(Upgrade):
    def __init__(self):
        super().__init__("sprites/buttons/button_upgrade_shotspeed.png", screen)
        self.cost = 50

    def check(self, player):
        player.shotspeedmod = 1.5
        
#hull upgrades
class upgrade_hull(Upgrade):
    def __init__(self):
        super().__init__("sprites/buttons/button_upgrade_armour.png", screen)
        self.cost = 100

    def check(self, player):
        player.maxhealth  = 125
        player.health = 125
        
class upgrade_barrier(Upgrade):
    def __init__(self):
        super().__init__("sprites/buttons/button_upgrade_barrier.png", screen)
        self.cost = 80

    def check(self, player):
        player.barrierallowed = True
        player.barrierchargerate = 300

class upgrade_revive(Upgrade):
    def __init__(self):
        super().__init__("sprites/buttons/button_upgrade_revive.png", screen)
        self.cost = 100

    def check(self, player):
        player.revive = True

#thruster upgrades
class upgrade_speed(Upgrade):
    def __init__(self):
        super().__init__("sprites/buttons/button_upgrade_movespeed.png", screen)
        self.cost = 50

    def check(self, player):
        player.maxspeed = 7
        player.acceleration = 1
        player.deceleration = 1
        
class upgrade_warp(Upgrade):
    def __init__(self):
        super().__init__("sprites/buttons/button_upgrade_warpdrive.png", screen)
        self.cost = 80

    def check(self, player):
        player.candodge = True
        player.dodgerate = 3
        player.dodgedistance = 24

class upgrade_autopilot(Upgrade):
    def __init__(self):
        super().__init__("sprites/buttons/button_upgrade_autododge.png", screen)
        self.cost = 100

    def check(self, player):
        player.gravitywell = True

#alt upgrades
class upgrade_cooldown(Upgrade):
    def __init__(self):
        super().__init__("sprites/buttons/button_upgrade_cooldown.png", screen)
        self.cost = 80

    def check(self, player):
        player.cooldownmod = 0.6
        
class upgrade_altfire(Upgrade):
    def __init__(self):
        super().__init__("sprites/buttons/button_upgrade_altfire.png", screen)
        self.cost = 80

    def check(self, player):
        player.altfiremod = 1.75

#############
class upgrade_reflect(Upgrade):
    def __init__(self):
        super().__init__("sprites/buttons/button_upgrade_counter.png", screen)
        self.cost = 100

    def check(self, player):
        player.retaliate = True

upgradelist = []
upgradelist.append(upgrade_speed())
upgradelist[-1].x = 50
upgradelist[-1].y = 480
upgradelist.append(upgrade_cooldown())
upgradelist[-1].x = 50
upgradelist[-1].y = 520
upgradelist.append(upgrade_firerate())
upgradelist[-1].x = 125
upgradelist[-1].y = 400
upgradelist.append(upgrade_autopilot())
upgradelist[-1].x = 125
upgradelist[-1].y = 440
upgradelist.append(upgrade_reflect())
upgradelist[-1].x = 125
upgradelist[-1].y = 480
upgradelist.append(upgrade_barrier())
upgradelist[-1].x = 125
upgradelist[-1].y = 520
upgradelist.append(upgrade_power())
upgradelist[-1].x = 50
upgradelist[-1].y = 400
upgradelist.append(upgrade_hull())
upgradelist[-1].x = 50
upgradelist[-1].y = 440
upgradelist.append(upgrade_warp())
upgradelist[-1].x = 200
upgradelist[-1].y = 400
upgradelist.append(upgrade_revive())
upgradelist[-1].x = 200
upgradelist[-1].y = 520
upgradelist.append(upgrade_altfire())
upgradelist[-1].x = 200
upgradelist[-1].y = 480
upgradelist.append(upgrade_shotspeed())
upgradelist[-1].x = 200
upgradelist[-1].y = 440

def save():
    f = open("save", "w+")
    savelist = []
    if equippedWep == weapon_generic:
        savelist.append("0")
    elif equippedWep == weapon_gatling:
        savelist.append("1")
    elif equippedWep == weapon_missile:
        savelist.append("2")
    else:
        savelist.append("3")
    if equippedAlt == altfire_rocket:
        savelist.append("0")
    elif equippedAlt == altfire_backblast:
        savelist.append("1")
    else:
        savelist.append("2")
    for i in upgradelist:
        if i.active:
            savelist.append("1")
        else:
            savelist.append("0")
    for i in maplist:
        if i.completed:
            savelist.append("1")
        else:
            savelist.append("0")
    savestring = "".join(savelist)
    f.write(savestring)
    f.close

def load():
    global scrap
    f = open("save", "r")
    loadlist = f.read(25)
    if loadlist[0] == "0":
        equippedWep = weapon_generic
    elif loadlist[0] == "1":
        equippedWep = weapon_gatling
    elif loadlist[0] == "2":
        equippedWep = weapon_missile
    elif loadlist[0] == "3":
        equippedWep = weapon_shotgun
    if loadlist[1] == "0":
        equippedAlt = altfire_rocket
    elif loadlist[1] == "1":
        equippedAlt = altfire_backblast
    elif loadlist[1] == "2":
        equippedAlt = altfire_reflect
    for i in range(12):
        if loadlist[i+2] == "0":
            upgradelist[i].active = False
        else:
            upgradelist[i].active = True
            scrap = scrap - upgradelist[i].cost
    for i in range(11):
        if loadlist[i+14] == "0":
            maplist[i].completed = False
        else:
            maplist[i].completed = True
            scrap = scrap + maplist[i].spoils
            maplist[i].spoils = 0
    f.close

try:
    load()
except:
    print("Save game failed to load! User file is either corrupt or nonexistent")
while not False:# Main loop!
    startgame = False #Leaves the main menu when true
    endgame = False   #Leaves the gameplay loop when true
    inmenu = False    #Leaves the upgrade menu when true
    while not startgame:
        screen.fill((0,0,128))
        for i in maplist:
            i.tick()
        for i in maplist_2:
            i.tick()
        label = mainfont.render("ϕ"+str(scrap), 1, (255,255,255))
        screen.blit(label, (365,20))
        pygame.display.flip()
        if testmap.pressed:
            startgame = True
            thislevel = Level(test)
            bg = endless_bg
        elif endless.pressed:
            startgame = True
            thislevel = endlessLevel()
            bg = endless_bg
        elif upgrade.pressed:
            startgame = True
            inmenu = True
            thislevel = None
            bg = (0,0,0)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
        clock.tick(60)
    world = World()
    world.levellist = thislevel
    endgame = False
    startgame = False
    player = PlayerShip("sprites/playership.png", screen)
    player.x = 200
    player.y = 384
    player.attack = equippedWep
    player.altfire = equippedAlt
    world.playerlist.append(player)
    
    #applyUpgrades(player, 1, 1, 1, 1)
    for i in upgradelist:
        if i.active:
            i.check(player)
    wrappingup = False
    
    if inmenu:
        buttonlist = []
        w_gatling_button = ItemSelect('sprites/buttons/button_gatling.png', screen)
        w_gatling_button.x = 0+50
        w_gatling_button.y = 64+50
        w_gatling_button.weapon = weapon_gatling
        w_generic_button = ItemSelect('sprites/buttons/button_generigun.png', screen)
        w_generic_button.x = 0+50
        w_generic_button.y = 0+50
        w_generic_button.weapon = weapon_generic
        w_missile_button = ItemSelect('sprites/buttons/button_missile.png', screen)
        w_missile_button.x = 0+50
        w_missile_button.y = 128+50
        w_missile_button.weapon = weapon_missile
        w_shotgun_button = ItemSelect('sprites/buttons/button_shotgun.png', screen)
        w_shotgun_button.x = 50
        w_shotgun_button.y = 192+50
        w_shotgun_button.weapon = weapon_shotgun
        a_rocket_button = ItemSelect('sprites/buttons/button_bomb.png', screen,False)
        a_rocket_button.x = 96+50
        a_rocket_button.y = 0+50
        a_rocket_button.weapon = altfire_rocket
        a_backblast_button = ItemSelect('sprites/buttons/button_backblast.png', screen,False)
        a_backblast_button.x = 96+50
        a_backblast_button.weapon = altfire_backblast
        a_backblast_button.y = 64+50
        a_reflect_button = ItemSelect('sprites/buttons/button_reflect.png', screen,False)
        a_reflect_button.x = 96+50
        a_reflect_button.y = 128+50
        a_reflect_button.weapon = altfire_reflect
        hardmode_button = DifficultySwitch('sprites/buttons/button_hardmode.png', screen)
        hardmode_button.x = 96+50
        hardmode_button.y = 192+50
        a_reflect_button.weapon = altfire_reflect
        exit_button = Button('sprites/buttons/button_return.png', screen)
        exit_button.x = 368
        exit_button.w = 32
        buttonlist.append(w_gatling_button)
        buttonlist.append(w_generic_button)
        buttonlist.append(w_missile_button)
        buttonlist.append(w_shotgun_button)
        buttonlist.append(a_rocket_button)
        buttonlist.append(a_reflect_button)
        buttonlist.append(a_backblast_button)
        buttonlist.append(hardmode_button)
        buttonlist.append(exit_button)

        
        while inmenu:
            screen.fill((80,0,0))
            for i in buttonlist:
                i.tick()
            for i in upgradelist:
                i.tick()
            label = mainfont.render("FUNDS: ϕ"+str(scrap), 1, (255,255,255))
            screen.blit(label, (50,380))
            pygame.display.flip()
            clock.tick(60)
            
            if exit_button.pressed:
                inmenu = False
                save()
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
    else:
        paused = False
        while not endgame:
            deathcounter = 0
            for event in pygame.event.get():
                if event.type == QUIT:
                    endgame = True
                    screen.fill((0,0,0))
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        player.upPress = True
                    if event.key == K_DOWN:
                        player.downPress = True
                    if event.key == K_RIGHT:
                        player.leftPress = True
                    if event.key == K_LEFT:
                        player.rightPress = True
                    if event.key == K_z:
                        player.shootPress = True
                    if event.key == K_x:
                        player.altPress = True
                    if event.key == K_LSHIFT:
                        player.dodgePress = True
                    #if event.key == K_q:
                    #    world.enemylist = []
                    #    world.levellist.nextspawn = tick_counter
                    #if event.key == K_w:
                    #    player.cooldown = 0
                if event.type == KEYUP:
                    if event.key == K_UP:
                        player.upPress = False
                    if event.key == K_DOWN:
                        player.downPress = False
                    if event.key == K_RIGHT:
                        player.leftPress = False
                    if event.key == K_LEFT:
                        player.rightPress = False
                    if event.key == K_z:
                        player.shootPress = False
                    if event.key == K_x:
                        player.altPress = False
                    if event.key == K_LSHIFT:
                        player.dodgePress = False
                    if event.key == K_p:
                        if paused:
                            paused = False
                        else:
                            paused = True
                        
            screen.fill(bg)
            if not paused:
                world.tick()
                pygame.display.flip()
            clock.tick(60)
            if not paused:
                tick_counter = tick_counter + 1
            
            if not wrappingup:
                if type(world.playerlist[0]) != PlayerShip:
                    endtime = tick_counter
                    wrappingup = True
            else:
                if tick_counter > endtime + 240:
                    endgame = True
                    screen.fill((0,0,0))
                    
            if world.levellist.finished:
                if not wrappingup:
                    endtime = tick_counter
                    wrappingup = True
                elif tick_counter > endtime + 150:
                    endgame = True
                    screen.fill((0,0,0))
        save()
