import pygame as pg
import json
import random as r
import math as m
import Constants as c
from Enemy import Zombie
from world import Battle_Map
from plants import Plant
#Initialize Pygame

pg.init()

#Create a Ingame Clock
PClock = pg.time.Clock()

#Create Game Window
Screen = pg.display.set_mode((c.SCREEN_WIDTH,c.SCREEN_HIGHT))
pg.display.set_caption("Leafy Legions")




#Load Battle Map
B_Map = pg.image.load('LDG_Assets/Battle_Map.png').convert_alpha()

#load Json Data for level
with open('LDG_Assets/Battle Map.tmj') as file:
    Battle_Map_Data = json.load(file)

def create_plant(pos):
    MTX = m.ceil(pos[0] / c.TILE_SIZE)
    MTY = m.ceil(pos[1] / c.TILE_SIZE)
    MTN = (MTY *c.COLUMNS) + MTX
    #Check for Plant
    SIF = True
    for PCboy in Plant_Group:
        if (MTX, MTY) == (PCboy.tile_X,PCboy.tile_Y):
            SIF = False
    if SIF == True:
        HighFlora = Plant(plant, MTX, MTY)
        Plant_Group.add(HighFlora)  

#Attacking plant
#def  attack_plant():
#TitleScreen = pg.image.load().convert_alpha()
#Create Map
BMap = Battle_Map(Battle_Map_Data, B_Map)
BMap.process_map_data()




#Load enemy Sprite
Zombie_Img = pg.image.load('LDG_Assets/Sprite/Screenshot 2024-02-20 133021.png').convert_alpha()


#Create Zombie Group
#Checks for Collision 

        
     
    
Zombie_Group = pg.sprite.Group()
def SpawnZombie(WC):
    for k in range(0,WC):
        if(r.randint(1,5) == 1):
            Zomboy = Zombie(BMap.Path1, Zombie_Img)
        elif(r.randint(1,5) == 2):
            Zomboy = Zombie(BMap.Path2, Zombie_Img)
        elif(r.randint(1,5) == 3):
            Zomboy = Zombie(BMap.Path3, Zombie_Img)
        elif(r.randint(1,5) == 4):
            Zomboy = Zombie(BMap.Path4, Zombie_Img)
        else:
            Zomboy = Zombie(BMap.Path5, Zombie_Img)

        Zombie_Group.add(Zomboy)
    

#Create a Plant
plant = pg.image.load('LDG_Assets/Sprite/Screenshot 2024-02-20 184238.png').convert_alpha()
Plant_Group = pg.sprite.Group()

#Runs the Screen
Screen_Run = True
Collision = False
waveCounter = 1
flag = False
while Screen_Run:

    #Framerate
    PClock.tick(c.FPS)

    Screen.fill("grey100")

    #Draw Battle Map
    BMap.draw(Screen)

    
    if(Zombie_Group.__len__() == 0):
        SpawnZombie(waveCounter)
        waveCounter += 1
                
           
            

         
    
    #Checks for Collision    
    for Pg in Plant_Group:
        for Zg in Zombie_Group:
            if(Zg.rect.center == Pg.rect.center):
                Pg.attackedByZombie(1)
                Collision = True
                flag = True
                break
                
            else:
                Collision = False
        if flag:
            flag = False
            break   
                       

            
                
            
            
                

    #Move the enemy
    
    if Plant_Group.__len__() == 0:
        Collision = False
    
    if Collision != True :
        for Zg in Zombie_Group:
            Zg.update()
    
    



    #Draw Zombie on the map
    
    for Zg in Zombie_Group:
        Zg.draw(Screen)
    Plant_Group.draw(Screen)

 

    #Exit Screen
    for event in pg.event.get():
        #To Quit the Program
        if event.type == pg.QUIT:
            Screen_Run = False
        #Event Monitor
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #check  if mouse is in game area
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HIGHT:
                create_plant(mouse_pos)
    #________________________________________________________________________________________________
    #Update the Screen
    
    pg.display.update()
    


pg.quit()