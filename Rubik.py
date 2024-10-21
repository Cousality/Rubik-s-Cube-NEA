from vpython import *
import numpy as np
import random
import optimal.solver as sv
from Decoder import *
#first line of the text file with default cube 
save = open("Save.txt" , "r")
Savefile = int(input("enter your save file number, Enter 0 for a solved cube"))
check = len(save.readlines())-1
while Savefile > check-1 or Savefile < -1:
        print("You have" ,check, "savefiles")
        Savefile = int(input("Please re enter savefile"))


class Rubik():
    def __init__(self):
        self.running = True
        self.tiles = []
        self.turn = np.pi/40
#center
        sphere(pos=vector(0,0,0),size=vector(3.1,3.1,3.1),color=vector(0,0,0))
##################################################
##ALL possible positons of the tiles on the cube##
##################################################        
        tile_pos = [[vector(-1, 1, 1.5),vector(0, 1, 1.5),vector(1, 1, 1.5),           #front,red 
                     vector(-1, 0, 1.5),vector(0, 0, 1.5),vector(1, 0, 1.5),
                     vector(-1, -1, 1.5),vector(0, -1, 1.5),vector(1, -1, 1.5), ],
                    [vector(1.5, 1, -1), vector(1.5, 1, 0), vector(1.5, 1, 1),         # right,yellow
                     vector(1.5, 0, -1), vector(1.5, 0, 0), vector(1.5, 0, 1),
                     vector(1.5, -1, -1), vector(1.5, -1, 0), vector(1.5, -1, 1), ],
                    [vector(-1, 1, -1.5), vector(0, 1, -1.5), vector(1, 1, -1.5),       # back,orange
                     vector(-1, 0, -1.5), vector(0, 0, -1.5), vector(1, 0, -1.5),
                     vector(-1, -1, -1.5), vector(0, -1, -1.5), vector(1, -1, -1.5), ],
                    [vector(-1.5, 1, -1), vector(-1.5, 1, 0), vector(-1.5, 1, 1),          # left,white 
                     vector(-1.5, 0, -1), vector(-1.5, 0, 0), vector(-1.5, 0, 1),
                     vector(-1.5, -1, -1), vector(-1.5, -1, 0), vector(-1.5, -1, 1), ],
                    [vector(-1, 1.5, -1), vector(0, 1.5, -1), vector(1, 1.5, -1),          # up,blue 
                     vector(-1, 1.5, 0), vector(0, 1.5, 0), vector(1, 1.5, 0),
                     vector(-1, 1.5, 1), vector(0, 1.5, 1), vector(1, 1.5, 1), ],
                    [vector(-1, -1.5, -1), vector(0, -1.5, -1), vector(1, -1.5, -1),          # down,green
                     vector(-1, -1.5, 0), vector(0, -1.5, 0), vector(1, -1.5, 0),
                     vector(-1, -1.5, 1), vector(0, -1.5, 1), vector(1, -1.5, 1), ],
                    ]
#################################
##END OF ALL POSSIBLE POSITIONS##
#################################
        colors = [vector(1,0,0),vector(1,1,0),vector(1,0.5,0),vector(1,1,1),vector(0,0,1),vector(0,1,0)] #red,yellow,orange,blue,blue,green
        angle = [(0,vector(0,0,0)),(np.pi/2,vector(0,1,0)),(0,vector(0,0,0)),(np.pi/2,vector(0,1,0)),(np.pi/2,vector(1,0,0)),(np.pi/2,vector(1,0,0))]
        save = open("Save.txt" , "r")
        save2 = save.readlines()
        save2 = save2[Savefile]
        length = 0
        save.close()
        #sides
        for rank,side in enumerate(tile_pos):
            for vec in side:
                exact = save2[length]
                length += 1
                if exact == "U":
                    tile = box(pos=vec,size=vector(0.98,0.98,0.1),color=colors[0])
                elif exact == "R":
                    tile = box(pos=vec,size=vector(0.98,0.98,0.1),color=colors[1])
                elif exact == "F":
                    tile = box(pos=vec,size=vector(0.98,0.98,0.1),color=colors[2])
                elif exact == "D":
                     tile = box(pos=vec,size=vector(0.98,0.98,0.1),color=colors[3])
                elif exact == "L":
                    tile = box(pos=vec,size=vector(0.98,0.98,0.1),color=colors[4])
                elif exact == "B":
                    tile = box(pos=vec,size=vector(0.98,0.98,0.1),color=colors[5])

                tile.rotate(angle = angle[rank][0],axis=angle[rank][1])
                self.tiles.append(tile)
#variables
        self.rotate = [None,0,0]
        self.moves = []
#Setting sides of the cube 
    def reset_positions(self):
        self.positions = {'front': [], 'right': [], 'back': [], 'left': [], 'top': [], 'bottom': []}
        for tile in self.tiles:
            if tile.pos.z > 0.4:
                self.positions['front'].append(tile)
            if tile.pos.x > 0.4:
                self.positions['right'].append(tile)
            if tile.pos.z < -0.4:
                self.positions['back'].append(tile)
            if tile.pos.x < -0.4:
                self.positions['left'].append(tile)
            if tile.pos.y > 0.4:
                self.positions['top'].append(tile)
            if tile.pos.y < -0.4:
                self.positions['bottom'].append(tile)
        
#Defines all the buttons 
    def control(self):
        button(bind=self.rotate_front_clock, text='F')
        button(bind=self.rotate_front_counter,text="F'")
        button(bind=self.rotate_right_clock, text='R')
        button(bind=self.rotate_right_counter, text="R'")
        button(bind=self.rotate_back_clock, text='B')
        button(bind=self.rotate_back_counter, text="B'")
        button(bind=self.rotate_left_clock, text='L')
        button(bind=self.rotate_left_counter, text="L'")
        button(bind=self.rotate_top_clock, text='U')
        button(bind=self.rotate_top_counter, text="U'")
        button(bind=self.rotate_bottom_clock, text='D')
        button(bind=self.rotate_bottom_counter, text="D'")
        button(bind=self.save, text="Save")
        button(bind=self.Notation, text="Notation")
        button(bind=self.scramble, text="Scramble")
        button(bind=self.solve, text="Solve")
        button(bind=self.Exit, text="Exit")
        
#activate the buttons ;p;
    def rotate_front_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['front_counter',0,np.pi/2]
    def rotate_right_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['right_counter',0,np.pi/2]
    def rotate_back_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['back_counter',0,np.pi/2]
    def rotate_left_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['left_counter',0,np.pi/2]
    def rotate_top_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['top_counter',0,np.pi/2]
    def rotate_bottom_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['bottom_counter',0,np.pi/2]
    def rotate_front_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['front_clock',0,np.pi/2]
    def rotate_right_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['right_clock',0,np.pi/2]
    def rotate_back_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['back_clock',0,np.pi/2]
    def rotate_left_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['left_clock',0,np.pi/2]
    def rotate_top_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['top_clock',0,np.pi/2]
    def rotate_bottom_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['bottom_clock',0,np.pi/2]
    def save(self):
        values = get_save(self.tiles)
        save = open("Save.txt" , "a")
        save.write("\n" + values)
    def get_save(self):
        value = get_save(self.tiles)
        return value
    def Exit(self):
        exit()   
    def solve(self):
        r = get_save(self.tiles)
        solution = sv.solve(r)
        print(solution)
    def Notation(self):
        print("R is Right \nL is Left \nF is Front \nB is Back \nU is Up\nD is down \nif there is an apostrophie that is prime and that means the cube turns anti-clockwise")   
#selects 20 random moves and applies them to self.
    def scramble(self):
        possible_moves = ["F","R","B","L","U","D","F'","R'","B'","L'","U'","D'"]
        for i in range(20):
            self.moves.append(random.choice(possible_moves))
        
            
        
        
#Move function 
    def move(self):
        possible_moves = ["F", "R", "B", "L", "U", "D", "F'", "R'", "B'", "L'", "U'", "D'"]
        if self.rotate[0] == None and len(self.moves) > 0:
            if self.moves[0] == possible_moves[0]:
                self.rotate_front_clock()
            elif self.moves[0] == possible_moves[1]:
                self.rotate_right_clock()
            elif self.moves[0] == possible_moves[2]:
                self.rotate_back_clock()
            elif self.moves[0] == possible_moves[3]:
                self.rotate_left_clock()
            elif self.moves[0] == possible_moves[4]:
                self.rotate_top_clock()
            elif self.moves[0] == possible_moves[5]:
                self.rotate_bottom_clock()
            elif self.moves[0] == possible_moves[6]:
                self.rotate_front_counter()
            elif self.moves[0] == possible_moves[7]:
                self.rotate_right_counter()
            elif self.moves[0] == possible_moves[8]:
                self.rotate_back_counter()
            elif self.moves[0] == possible_moves[9]:
                self.rotate_left_counter()
            elif self.moves[0] == possible_moves[10]:
                self.rotate_top_counter()
            elif self.moves[0] == possible_moves[11]:
                self.rotate_bottom_counter()
            self.moves.pop(0)
#pieces actaully turn
    def animations(self):
        if self.rotate[0] == 'front_counter' :
            pieces = self.positions['front']
            for tile in pieces:
                tile.rotate(angle=(self.turn),axis = vector(0,0,1),origin=vector(0,0,0))
            self.rotate[1] += self.turn
        elif self.rotate[0] == 'right_counter' :
            pieces = self.positions['right']
            for tile in pieces:
                tile.rotate(angle=(self.turn),axis = vector(1,0,0),origin=vector(0,0,0))
            self.rotate[1] += self.turn
        elif self.rotate[0] == 'back_counter' :
            pieces = self.positions['back']
            for tile in pieces:
                tile.rotate(angle=(self.turn),axis = vector(0,0,-1),origin=vector(0,0,0))
            self.rotate[1] += self.turn
        elif self.rotate[0] == 'left_counter' :
            pieces = self.positions['left']
            for tile in pieces:
                tile.rotate(angle=(self.turn),axis = vector(-1,0,0),origin=vector(0,0,0))
            self.rotate[1] += self.turn
        elif self.rotate[0] == 'top_counter' :
            pieces = self.positions['top']
            for tile in pieces:
                tile.rotate(angle=(self.turn),axis = vector(0,1,0),origin=vector(0,0,0))
            self.rotate[1] += self.turn
        elif self.rotate[0] == 'bottom_counter' :
            pieces = self.positions['bottom']
            for tile in pieces:
                tile.rotate(angle=(self.turn),axis = vector(0,-1,0),origin=vector(0,0,0))
            self.rotate[1] += self.turn
        elif self.rotate[0] == 'front_clock' :
            pieces = self.positions['front']
            for tile in pieces:
                tile.rotate(angle=(-self.turn),axis = vector(0,0,1),origin=vector(0,0,0))
            self.rotate[1] += self.turn
        elif self.rotate[0] == 'right_clock' :
            pieces = self.positions['right']
            for tile in pieces:
                tile.rotate(angle=(-self.turn),axis = vector(1,0,0),origin=vector(0,0,0))
            self.rotate[1] += self.turn
        elif self.rotate[0] == 'back_clock' :
            pieces = self.positions['back']
            for tile in pieces:
                tile.rotate(angle=(-self.turn),axis = vector(0,0,-1),origin=vector(0,0,0))
            self.rotate[1] += self.turn
        elif self.rotate[0] == 'left_clock' :
            pieces = self.positions['left']
            for tile in pieces:
                tile.rotate(angle=(-self.turn),axis = vector(-1,0,0),origin=vector(0,0,0))
            self.rotate[1] += self.turn
        elif self.rotate[0] == 'top_clock' :
            pieces = self.positions['top']
            for tile in pieces:
                tile.rotate(angle=(-self.turn),axis = vector(0,1,0),origin=vector(0,0,0))
            self.rotate[1] += self.turn
        elif self.rotate[0] == 'bottom_clock' :
            pieces = self.positions['bottom']
            for tile in pieces:
                tile.rotate(angle=(-self.turn),axis = vector(0,-1,0),origin=vector(0,0,0))
            self.rotate[1] += self.turn
        if self.rotate[1] + self.turn/2 > self.rotate[2] and \
            self.rotate[1] - self.turn/2 < self.rotate[2]:
            self.rotate = [None,0,0]
            self.reset_positions()
#makes the cube turn, plus fps and move function 
    def update(self):
        rate(120)
        self.move()
        self.animations()

#Starts the program lol
    def start(self):
        self.reset_positions()
        self.control()
        while self.running:
            self.update()
    
#to change later

def Main():
    cube = Rubik()
    cube.start()
Main()












