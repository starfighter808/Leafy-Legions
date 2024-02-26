import pygame as pg
import json
from plant import Plant
from zombie import Zombie
from world import World
import constants as c
from button import Button

#initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()

#create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))

#text windows name
pg.display.set_caption("Leafy Legions")


#game varaibles
placing_plants = False

#Image Creation Step
# load map image
map_image = pg.image.load('levels/level.png').convert_alpha() # get map image from following the folder path

#load plant image
plantImage = pg.image.load('PlantsImages/machineGunPlant.png').convert_alpha() # get plant image from following the folder path

#load zombie image
zombieImage = pg.image.load('ZombieImages/zombieDefault.png').convert_alpha() # get plant image from following the folder path

# button image
buy_Plant_image = pg.image.load('PlantsImages/machineGunPlant.png').convert_alpha()
cancel_image = pg.image.load('Buttons/cancelButtonImage.png').convert_alpha()

#load json data for level
with open('levels/level2.tmj') as file:
  world_data = json.load(file)

# create/call world map
world = World(world_data, map_image) # pass map image into the world class then store results in world variable
world.process_data()


#create individual zombie paths
waypoints1 = [(1407, 190), (-1407, 190)]
waypoints2 = [(1407, 317), (-1407, 317)]
waypoints3 = [(1407, 452), (-1407, 452)]
waypoints4 = [(1407, 575), (-1407, 575)]
waypoints5 = [(1407, 700), (-1407, 700)]

#create plant
def create_plant(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    #calculate the sequential number of the tile
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
    #check if tile is grass
    if world.tile_map[mouse_tile_num] == 25:
        #check for another object
        freeSpace = True
        for plant in plantGroup:
            if(mouse_tile_x, mouse_tile_y) == (plant.tile_x, plant.tile_y):
                freeSpace = False
        if freeSpace == True:
            newPlant = Plant(plantImage, mouse_tile_x, mouse_tile_y) #pass information to plant
            plantGroup.add(newPlant)   #create the "package" to be placed


#create_groups/instence
plantGroup = pg.sprite.Group()

#zombie group/instence
zombieGroup = pg.sprite.Group()
zombieGroup2 = pg.sprite.Group()
zombieGroup3 = pg.sprite.Group()
zombieGroup4 = pg.sprite.Group()
zombieGroup5 = pg.sprite.Group()

#Pass the waypoint and image for the zombie that coresponds with the row/path they need to spawn at
zombie = Zombie(waypoints1, zombieImage)
zombieGroup.add(zombie)

zombie2 = Zombie(waypoints2, zombieImage)
zombieGroup2.add(zombie2)

zombie3 = Zombie(waypoints3, zombieImage)
zombieGroup3.add(zombie3)

zombie4 = Zombie(waypoints4, zombieImage)
zombieGroup4.add(zombie4)

zombie5 = Zombie(waypoints5, zombieImage)
zombieGroup5.add(zombie5)

#create button
plant_button = Button(c.SCREEN_WIDTH + 30, 100, buy_Plant_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 400, cancel_image, False)


#game run/loop
run = True
while run:

  clock.tick(c.FPS)

  ###############################
  #   UPDATNG SECTION           #
  ###############################

  #update groups, create the move function
  zombieGroup.update()
  zombieGroup2.update()
  zombieGroup3.update()
  zombieGroup4.update()
  zombieGroup5.update()

  ###############################
  #   DRAWING SECTION           #
  ###############################
  screen.fill("grey100")

  #draw level
  world.draw(screen)

  #draw buttons
  #button for placing turrets
  if plant_button.draw(screen):
      placing_plants = True

  #if placing turrets then show the cancel button as well
  if placing_plants == True:
     #show plant while placing
     cursor_rect = plantImage.get_rect()
     cursor_pos = pg.mouse.get_pos()
     cursor_rect.center = cursor_pos
     if cursor_pos[0] <= c.SCREEN_WIDTH:
        screen.blit(plantImage, cursor_rect)
     if cancel_button.draw(screen):
         placing_plants = False

  #draw zombie path
  #pg.draw.lines(screen, "grey0", False, waypoints1)
  #pg.draw.lines(screen, "grey0", False, waypoints2)
  #pg.draw.lines(screen, "grey0", False, waypoints3)
  #pg.draw.lines(screen, "grey0", False, waypoints4)
  #pg.draw.lines(screen, "grey0", False, waypoints5)

  #draw groups/the zombie
  zombieGroup.draw(screen)
  zombieGroup2.draw(screen)
  zombieGroup3.draw(screen)
  zombieGroup4.draw(screen)
  zombieGroup5.draw(screen)

  #draw the plantGroup/image
  plantGroup.draw(screen)

  #event handler
  for event in pg.event.get():
    #quit program
    if event.type == pg.QUIT:
      run = False
    #mouse click
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: #create turret if this is met
        mouse_pos = pg.mouse.get_pos() # get location of the mouse
        #check if mouse is in the area
        if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
            if placing_plants == True:
                create_plant(mouse_pos)

  #update display
  pg.display.flip()

pg.quit()
