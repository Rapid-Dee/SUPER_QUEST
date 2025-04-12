import curses,time,os
from random import *
resume=True
game_over=False
import menu
# print menu
coll =["-","|"]
name = menu.menu()
#create atk_layer
atk_layer=[]
def atk_refresh():
    for i in range(128):
    	for j in range(128):
    		atk_layer[i][j]=0
#generate world
world=menu.generate(atk_layer)

# setup window
screen_height=32
screen_width=50
curses.initscr()
win = curses.newwin(screen_height+1, screen_width+1, 0, 0) # y,x
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.nodelay(1)


#behaviors and logic==============

#init bullets/projectiles
projectiles=[]
class Projectile:
	def __init__(self,x,y,nx,ny,dmg,cnt=-1,pierce=False):
		self.x=x
		self.y=y
		self.nx=nx
		self.ny=ny
		self.dmg=dmg
		self.cnt=cnt
		self.pierce=pierce
	def update(self):
		atk_layer[self.y%128][self.x%128]=self.dmg
		for i in entities:
			if self.pierce==False and i.x==self.x and i.y==self.y:
				self.cnt=0
		if (world[self.y%128][self.x%128] in coll) or self.cnt==0:
			projectiles.remove(self)
			return 0
		self.cnt-=1
		self.x+=self.nx
		self.y+=self.ny
#init entities
entities=[]
class Entity:

	global entities
	def __init__(self,x,y):

		self.x=x
		self.y=y
		self.hp=10
		self.effect=EFFECTS.normal

	def update(self):

		self.hp-=atk_layer[self.y][self.x]
		if self.hp<1:
			entities.remove(self)
items=[]
#player
class Player(Entity):
    def special(self):
        for i in self.equiped:
            if self.equiped:
                slot = self.inventory[self.equiped.index(i)]
                if self.inventory[slot]!=0 and self.mp>=self.inventory[slot].mcost:
                    self.mp-=self.inventory[slot].mcost
                    self.inventory[slot].special(self.x,self.y,self.aim_x,self.aim_y)

    def attack(self):
        atk_layer[self.y+self.aim_y][self.x+self.aim_x]=self.atk

    def grab(self,item):
        is_full = len(list(filter(lambda x: x==0,self.inventory)))>0
        if is_full:
	        pass
        else:
            slot_id=self.inventory.find(0)
            if self.inventory[slot_id]==0:
                self.inventory[slot_id]=item
                items.remove(item)

    def drop(self,slot):
        if self.inventory[slot]!=0:
            self.inventory[slot].x=self.x
            self.inventory[slot].y=self.y
            items.append(self.inventory[slot])
            self.inventory[slot]=0
        else:
            pass

    def __init__(self,x,y,name):
        self.name=name
        self.x=x
        self.y=y
        self.inventory=list(0 for x in range(10))
        self.equiped=list(False for x in range(10))
        self.can_g=False
        self.hp=10
        self.mp=0
        self.atk=0
        self.max_mp=20
        self.res=0
        self.aim_x=1
        self.aim_y=0

    def update(self):
        global game_over
        if self.mp<self.max_mp:
            self.mp+=1
        for i in self.equiped:
            if self.equiped:
                slot = self.inventory[self.equiped.index(i)]
                if self.inventory[slot]!=0:
                    self.atk=1+self.inventory[slot].atk
                    self.res=self.inventory[slot].res
        else:
            self.atk=1
            self.res=0
            self.hp-=atk_layer[self.y][self.x]
            if self.hp<1:
                game_over=True

#spawn player
player=Player(8,4,name)
entities.append(player)
entities.append(Entity(2,4))


#game=======================
while game_over==False:
	if resume==True:
		win.refresh()

		#menu screen
		for i in range(1,17):
			for j in range(35,49):
				win.addch(i,j," ")
		win.addstr(1,35,"HP:")
		win.addstr(1,38,str(player.hp))

		win.addstr(2,35,"MP:")
		win.addstr(2,38,str(player.mp))

		win.addstr(3,35,"ATK:")
		win.addstr(3,39,str(player.atk))

		win.addstr(4,35,"RES:")
		win.addstr(5,35,"INVENTORY:")

		win.addstr(4,40,str(player.res))

		win.addstr(16,35,"X:")
		win.addstr(16,37,str(player.x))

		win.addstr(16,40,"Y:")
		win.addstr(16,42,str(player.y))

		#game screen
		for i in range(-8,8):
			for j in range(-16,16):
				if j+player.x<128 and j+player.x>=0 and i+player.y>=0 and i+player.y<=127:
					win.addch(i+9,j+17,world[i+player.y][j+player.x])
				else:
					win.addch(i+9,j+17," ")

		#draw weapons
		for i in items:
			xx=-player.x+i.x+17
			yy=-player.y+i.y+9
			if i.x==player.x and i.y==player.y and player.can_g:
				player.grab(i)
			if xx>0 and xx<32 and yy>0 and yy<16:
				win.addch(yy,xx,"?")
		win.addch(9+player.aim_y,17+player.aim_x,"/")

		#player
		for i in projectiles:
			i.update()
			xx=-player.x+i.x+17
			yy=-player.y+i.y+9
			if xx>0 and xx<32 and yy>0 and yy<16:
				win.addch(yy,xx,"*")
		for i in entities:
			i.update()
			xx=-player.x+i.x+17
			yy=-player.y+i.y+9
			if xx>0 and xx<32 and yy>0 and yy<16:
				win.addch(yy,xx,"@")

	#input
		player.can_g=False
		atk_refresh()
	i=win.getch()
	if i!=-1:
		resume=True
	else: resume=False
	if i==115:

		#s
			if not(world[player.y+1][player.x] in coll):
				player.y+=1
				player.aim_y=1
				player.aim_x=0
	elif i==97:

		#a
			if not(world[player.y][player.x-1] in coll):
				player.x-=1
				player.aim_y=0
				player.aim_x=-1
	elif i==100:

		#d
			if not(world[player.y][player.x+1] in coll):
				player.x+=1
				player.aim_y=0
				player.aim_x=1
	elif i==119:

		#w
			if not(world[player.y-1][player.x] in coll):
				player.y-=1
				player.aim_y=-1
				player.aim_x=0
	elif i==103:

		#g
			player.can_g=True
	elif i==113:

		#q
			player.drop()
	elif i==102:

		#f
			player.attack()
	elif i==117:

		#u
			player.special()
	if i>48 and i<58:

	#1-9
		entities[0].slot=i-49

#game over screen=================
win.addstr(9,0," "*50)
win.addstr(9,17,"GAME OVER")
win.refresh()
time.sleep(1)
curses.endwin()