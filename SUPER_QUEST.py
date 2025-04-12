import curses,time,os
from random import *
#UNIX VERSION
#logo
logo=(
"  dN   i I   Mb    NMH   Gb",
" K     l l   N D   I     F D",
"  Mb   I i   Hp    NME   HY",
"   l   q p   T     l     W q",
" jp     U    I     NMH   M  b"
)

for i in logo:
	print(i)
	time.sleep(0.1)
print("[=--------------------------=]")
print(" "*12+"QUEST")
print("wasd - move\nq - drop weapon\ng - grab from floor\nf -attack\nu - special attack")
print("~~~~~~~~~~~~~~")
x="0"
while x!="1":
	if x=="":
		print("please, enter the number.")
	x=input("1.Play\n2.Guide\n3.Exit\n")
	if x=="3":
		os.abort()
	if x=="2":
		print("# X - walls\n@ is you and others entity\n= is chest, ? is loot.\n to grab loot - stay on loot and press g.\n/ - your weapon\n* - magic effects\nu , . - decorates\n")
name=input("enter your name to start a quest!\n")
#generate world==================
resume=True
game_over=False
flr=(" ",".",",")
coll=("#","X")
world=[]
atk_field=[]
def atk_refresh():
	for i in range(128):
		for j in range(128):
			atk_field[i][j]=0
for i in range(128):
	world.append([])
	atk_field.append([])
	for j in range(128):
		atk_field[i].append(0)
		r=int(random()*100)%3
		world[i].append(flr[r])

for i in range(128):
	for j in range(128):
		r=int(random()*100)%100
		if r>70 and (world[i-1][j]=="#" or world[i][j%127+1]=="#" or world[i][j-1]=="#" or world[i%127+1][j]=="#"):
			world[i][j]="u"
		if r>80 and (world[i-1][j]=="#" or world[i][j%127+1]=="#" or world[i][j-1]=="#" or world[i%127+1][j]=="#"):
			world[i][j]="="
		if r>40 and (j%16==0 or i%8==0):
			world[i][j]="#"
		if r>70 and (world[i-1][j] in coll or world[i][j%127+1] in coll or world[i-1][j%126+2] in coll):
			world[i][j]="X"

#borders
for j in range(128):
	world[j][0]="#"
	world[j][127]="#"
	world[0][j]="#"
	world[127][j]="#"
	
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
b=[]
class projectile:

	def __init__(self,x,y,nx,ny,dmg,cnt=-1,pierce=False):

		self.x=x
		self.y=y
		self.nx=nx
		self.ny=ny
		self.dmg=dmg
		self.cnt=cnt
		self.pierce=pierce

	def update(self):

		atk_field[self.y%128][self.x%128]=self.dmg
		for i in p:
			if self.pierce==False and i.x==self.x and i.y==self.y:
				self.cnt=0
		if (world[self.y%128][self.x%128] in coll) or self.cnt==0:
			b.remove(self)
			return 0
		self.cnt-=1
		self.x+=self.nx
		self.y+=self.ny

#init weapons
class weapon:

	def special(self,x,y,nx,ny):

		pass

	def set(self,x,y):

		self.x=x
		self.y=y

	def __init__(self,name,atk,res,mcost=0):

		self.atk=atk
		self.res=res
		self.x=0
		self.y=0
		self.name=name
		self.mcost=mcost

#weapon childs 
class heal_rod(weapon): #heal

		def special(self,x,y,nx,ny):

			b.append(projectile(x+nx,y+ny,nx,ny,-3,5))
			b.append(projectile(x,y,0,0,-3,3))

class rod(weapon): #rod

	def special(self,x,y,nx,ny):

		for i in range(1,3):
			b.append(projectile(x+i*nx,y+i*ny,nx,ny,4,4,True))
			b.append(projectile(x+(nx-ny)*i,y+(ny-nx)*i,(nx-ny)*i,(ny-nx)*i,4,4))
			b.append(projectile(x+(ny+nx)*i,y+(nx+ny)*i,(ny+nx)*i,(nx+ny)*i,4,4))

class spear(weapon): #spear

	def special(self,x,y,nx,ny):

		for i in range(3):
			b.append(projectile(x+(1+i)*nx,y+(1+i)*ny,nx,ny,3,5,True))

class bomb(weapon): #bomb

	def special(self,x,y,nx,ny):

		b.append(projectile(x+nx,y+ny,0,0,2))

class bow(weapon): #bow

	def special(self,x,y,nx,ny):

		b.append(projectile(x+nx,y+ny,nx,ny,2))

class hammer(weapon): #hammer

	def special(self,x,y,nx,ny):

		for i in range(-1,2):
			for j in range(-1,2):
				if not(i==0 and j==0):
					b.append(projectile(x+i,y+j,i,j,3,4,True))

class sword(weapon): #sword

	pass

class katana(weapon): #katana

	def special(self,x,y,nx,ny):

		b.append(projectile(x,y,0,0,20,1,True))

#generate weapon
w=[]
w.append(katana("joke press u",0,0,0))
w[-1].set(5,5)

for i in range(127):
	for j in range(127):
		if world[i+1][j]=="=" and not(world[i][j] in coll):
			r=int(random()*100)%13
			if r==0:
					w.append(bow("bow",1,0,3))
			elif r==1:
					w.append(spear("spear",9,0,10))
			elif r==2:
					w.append(hammer("hammer",8,0,8))
			elif r==3:
					w.append(rod("flame rod",0,0,4))
			elif r==4:
					w.append(heal_rod("heal rod",0,0,20))
			elif r==5:
					w.append(bomb("bomb",0,1,5))
			elif r==6:
					w.append(sword("sword",5,1))
			elif r==7:
					w.append(hammer("mace",5,0,15))
			elif r==8:
					w.append(bow("stone",0,0,20))
			elif r==9:
					w.append(sword("blade",10,2))
			elif r==10:
					w.append(sword("knife",2,1))
			elif r==11:
					w.append(sword("shield",2,5))
			elif r==12:
					w.append(katana("katana",7,0,1))
			w[-1].set(j,i)

#init entities
p=[]
class entity:

	global p
	def __init__(self,x,y):

		self.x=x
		self.y=y
		self.hp=10

	def update(self):

		self.hp-=atk_field[self.y][self.x]
		if self.hp<1:
			p.remove(self)

#player
class player(entity):

	def special(self):

		if self.inventory[self.slot]!=0 and self.mp>=self.inventory[self.slot].mcost:
			self.mp-=self.inventory[self.slot].mcost
			self.inventory[self.slot].special(self.x,self.y,self.aim_x,self.aim_y)

	def attack(self):

		atk_field[self.y+self.aim_y][self.x+self.aim_x]=self.atk

	def grab(self,n):

		if self.inventory[self.slot]==0:
			self.inventory[self.slot]=n
			w.remove(n)

	def drop(self):

		if self.inventory[self.slot]!=0:
			self.inventory[self.slot].x=self.x
			self.inventory[self.slot].y=self.y
			w.append(self.inventory[self.slot])
			self.inventory[self.slot]=0

	def __init__(self,x,y,name):

		self.name=name
		self.x=x
		self.y=y
		self.inventory=[0,0,0,0,0,0,0,0,0]
		self.can_g=False
		self.slot=0
		self.hp=10
		self.mp=0
		self.atk=0
		self.res=0
		self.aim_x=1
		self.aim_y=0

	def update(self):

		global game_over
		if self.mp<20:
			self.mp+=1
		if self.inventory[self.slot]!=0:
			self.atk=1+self.inventory[self.slot].atk
			self.res=self.inventory[self.slot].res
		else:
			self.atk=1
			self.res=0
		self.hp-=atk_field[self.y][self.x]
		if self.hp<1:
			game_over=True

#spawn player
p.append(player(8,4,name))
p.append(entity(2,4))

#menu
gui=["[","]"]
for i in range(50):
	for j in range(18):
		win.addch(j,i,gui[i%2])

#game=======================
while game_over==False:
	if resume==True:
		win.refresh()

		#menu screen
		for i in range(1,17):
			for j in range(35,49):
				win.addch(i,j," ")
		win.addstr(1,35,"HP:")
		win.addstr(1,38,str(p[0].hp))

		win.addstr(2,35,"MP:")
		win.addstr(2,38,str(p[0].mp))

		win.addstr(3,35,"ATK:")
		win.addstr(3,39,str(p[0].atk))

		win.addstr(4,35,"RES:")
		win.addstr(5,35,"INVENTORY:")

		win.addstr(4,40,str(p[0].res))
		win.addch(p[0].slot+6,36,"~")

		for i in range(9):
			win.addch(6+i,35,str(i+1))

			if p[0].inventory[i]!=0:
				win.addstr(6+i,37,p[0].inventory[i].name)

		win.addstr(16,35,"X:")
		win.addstr(16,37,str(p[0].x))

		win.addstr(16,40,"Y:")
		win.addstr(16,42,str(p[0].y))

		#game screen
		for i in range(-8,8):
			for j in range(-16,16):
				if j+p[0].x<128 and j+p[0].x>=0 and i+p[0].y>=0 and i+p[0].y<=127:
					win.addch(i+9,j+17,world[i+p[0].y][j+p[0].x])
				else:
					win.addch(i+9,j+17," ")

		#draw weapons
		for i in w:
			xx=-p[0].x+i.x+17
			yy=-p[0].y+i.y+9
			if i.x==p[0].x and i.y==p[0].y and p[0].can_g:
				p[0].grab(i)
			if xx>0 and xx<32 and yy>0 and yy<16:
				win.addch(yy,xx,"?")
		win.addch(9+p[0].aim_y,17+p[0].aim_x,"/")

		#player
		for i in b:
			i.update()
			xx=-p[0].x+i.x+17
			yy=-p[0].y+i.y+9
			if xx>0 and xx<32 and yy>0 and yy<16:
				win.addch(yy,xx,"*")
		for i in p:
			i.update()
			xx=-p[0].x+i.x+17
			yy=-p[0].y+i.y+9
			if xx>0 and xx<32 and yy>0 and yy<16:
				win.addch(yy,xx,"@")

	#input
		p[0].can_g=False
		atk_refresh()
	i=win.getch()
	if i!=-1:
		resume=True
	else: resume=False
	if i==115:

		#s
			if not(world[p[0].y+1][p[0].x] in coll):
				p[0].y+=1
				p[0].aim_y=1
				p[0].aim_x=0
	elif i==97:

		#a
			if not(world[p[0].y][p[0].x-1] in coll):
				p[0].x-=1
				p[0].aim_y=0
				p[0].aim_x=-1
	elif i==100:

		#d
			if not(world[p[0].y][p[0].x+1] in coll):
				p[0].x+=1
				p[0].aim_y=0
				p[0].aim_x=1
	elif i==119:

		#w
			if not(world[p[0].y-1][p[0].x] in coll):
				p[0].y-=1
				p[0].aim_y=-1
				p[0].aim_x=0
	elif i==103:

		#g
			p[0].can_g=True
	elif i==113:

		#q
			p[0].drop()
	elif i==102:

		#f
			p[0].attack()
	elif i==117:

		#u
			p[0].special()
	if i>48 and i<58:

	#1-9
		p[0].slot=i-49

#game over screen=================
win.addstr(9,0," "*50)
win.addstr(9,17,"GAME OVER")
win.refresh()
time.sleep(1)
curses.endwin()