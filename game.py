import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 7
GAME_HEIGHT = 7

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Gem(GameElement):
    IMAGE="BlueGem"
    SOLID = False
    
    def interact(self, player):
        
        player.inventory.append(self)
        print "added to inventory"
        print player.inventory
        GAME_BOARD.draw_msg("You just aquired a gem! You have %d items!" %(len(player.inventory)))


class OrangeGem(Gem):
    IMAGE="OrangeGem"

    

class Door(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True

    def interact(self, player):
        keycount = player.inventory
        if keycount >= 1:
            self.SOLID = False
            self.change_image("DoorOpen")
           

class Wall(GameElement):
    IMAGE = "TallWall"
    SOLID = True

class Water(GameElement):
    IMAGE= "WaterBlock"
    SOLID= True


class Chest(GameElement):
    IMAGE="ChestClosed"
    SOLID=True    

    def interact(self, player):
        keycount = player.inventory
        if keycount >= 1:
            self.SOLID = False
            
            self.change_image("ChestOpen")

class Key(GameElement):
    IMAGE = "Key"

    def interact(self, player):
        player.inventory.append(self)
        print "added to inventory"
        print player.inventory
        GAME_BOARD.draw_msg("You just aquired a key and have %d items! Maybe you should use it hmmmm?" %(len(player.inventory)))

        
        keycount = 0 
        for item in player.inventory:
            if type(item) == Key:
                keycount += 1
            
            print keycount
            if keycount >= 1:
                print keycount


class Character(GameElement):
    IMAGE = "HornGirl"
    
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def keyboard_handler(self, symbol, modifier):

            direction = None
            if symbol == key.UP:
                direction = "up"
            elif symbol == key.DOWN:
                direction = "down"
            elif symbol == key.LEFT:
                direction = "left"
            elif symbol == key.RIGHT:
                direction = "right"

            self.board.draw_msg("[%s] moves %s" % (self.IMAGE, direction))

            if direction:
                next_location = self.next_pos(direction)
                if next_location:
                    next_x = next_location[0]
            
                
                    next_y = next_location[1]

                    existing_el = self.board.get_el(next_x, next_y)
                    if existing_el:
                        self.board.draw_msg("Get out of my way you punk!")
                        existing_el.interact(self)
                    
                    if existing_el is None or not existing_el.SOLID:
                        self.board.del_el(self.x, self.y)
                        self.board.set_el(next_x, next_y, self)

    def next_pos(self, direction):
        if direction == "up":
            if self.y - 1 < 0:
                self.board.draw_msg("You can't go any further in this direction!") 
                return (self.x, self.y)
            else:
                return (self.x, self.y - 1)
        elif direction == "down":
            if self.y + 1 > (GAME_HEIGHT - 1):
                self.board.draw_msg("You can't go any further in this direction!")
                return (self.x, self.y)
            else:
                return (self.x, self.y + 1)
        elif direction == "left":
            if self.x - 1 < 0:
                self.board.draw_msg("You can't go any further in this direction!") 
                return (self.x, self.y)
            else:
                return (self.x - 1, self.y)  
        elif direction == "right":
            if self.x + 1 > (GAME_WIDTH - 1):
                self.board.draw_msg("You can't go any further in this direction!")
                return (self.x, self.y)
            else:
                return (self.x + 1, self.y)
        return None

#### Put class definitions here ####

####   End class definitions    ####
class Enemy(GameElement):
    IMAGE= "OrangeDragon"
    direction = 1

    def update(self, dt):
        next_y = self.y + self.direction

        if next_y < 1 or next_y >= self.board.height - 1:
            self.direction *= -1
            next_y = self.y
        self.board.del_el(self.x, self.y)
        self.board.set_el(self.x, next_y, self)

class Tree(GameElement):
    IMAGE = "TallTree"
    SOLID = True

def initialize():
    """Put game initialization code here"""
    #Initialize and register rock 1
    rock_positions = [
            (2,2),
            (1,2),
            (2,4),
            (2,3),
    ]
    rocks=[]
    water_pos= [
            (0,0),
            (1,0),
            (2,0),
            (3,0),
            (4,0),
            (5,0),
            (6,0),
            (1,6),
            (2,6),
            (3,6),
            (4,6),
            (5,6),
            (0,2),
            (0,3),
            (0,4),
            (0,5),
            (6,2),
            (6,3),
            (6,4),
            (6,5),   
    ]
    waters=[]
    for pos in water_pos:
        water = Water()
        GAME_BOARD.register(water)
        GAME_BOARD.set_el(pos[0],pos[1], water)
        waters.append(water)

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0],pos[1],rock)
        rocks.append(rock)
    rocks[-1].SOLID = False

    for rock in rocks:
        print rock

    player=Character()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(1,1,player)
    print player

    GAME_BOARD.draw_msg("This game is wicked awesome.")

    gem = OrangeGem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(4,3, gem)

    door = Door()
    GAME_BOARD.register(door)
    GAME_BOARD.set_el(4,4, door)

    wall = Wall()
    GAME_BOARD.register(wall)
    GAME_BOARD.set_el(6,6,wall)

    enemy = Enemy()
    GAME_BOARD.register(enemy)
    GAME_BOARD.set_el(3,3, enemy)

    chest= Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(1,4,chest)

    wall = Wall()
    GAME_BOARD.register(wall)
    GAME_BOARD.set_el(6,1, wall)

    wall = Wall()
    GAME_BOARD.register(wall)
    GAME_BOARD.set_el(0,6, wall)

    wall = Wall()
    GAME_BOARD.register(wall)
    GAME_BOARD.set_el(0,1, wall)

    gem = OrangeGem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(1,3, gem)


    key_pos = [
            (4,5),
            (1,5),
    ]
    for pos in key_pos:
        keys= []
        key = Key()
        GAME_BOARD.register(key)
        GAME_BOARD.set_el(pos[0], pos[1], key)
        keys.append(key) 

    tree = Tree()
    GAME_BOARD.register(tree)
    GAME_BOARD.set_el(5,1, tree)