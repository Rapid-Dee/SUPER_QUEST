import curses,time,os
from random import *
resume=True
game_over=False
import menu
# print menu
coll =["-","|"]
name = menu.menu()
msg = ""

#generate world
world=menu.generate()

# setup window
screen_height=32
screen_width=50
curses.initscr()
win = curses.newwin(screen_height+1, screen_width+1, 0, 0) # y,x
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.nodelay(1)


#behaviors and logic

#effects
class Effect:
    def __init__(self,dmg,freeze,res,atk):
        self.dmg = dmg
        self.freeze = freeze
        self.res = res
        self.atk = atk
EFFECTS = {
"normal":Effect(0,False,0,0)
}
NORMAL = "normal"
#init bullets/projectiles
projectiles=[]
class Projectile:
    def __init__(self,x,y,nx,ny,dmg,magic_dmg,effect,cnt=-1,pierce=False):
        self.x=x
        self.y=y
        self.nx=nx
        self.ny=ny
        self.dmg=dmg
        self.magic_dmg=magic_dmg
        self.effect=effect
        self.cnt=cnt
        self.pierce=pierce
    def update(self):
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
    def __init__(self,x,y,symbol):
        self.symbol = symbol
        self.x=x
        self.y=y
        self.hp=10
        self.effect=EFFECTS[NORMAL]

    def update(self):
        if self.hp<1:
            entities.remove(self)
items=[]
#player
class Player(Entity):

    def attack(self,entity):
        global msg
        msg = f"-{self.name} attacked a {entity.symbol}!"

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

    def __init__(self,x,y,name,symbol="@"):
        self.score = 0
        self.symbol = symbol
        self.name=name
        self.x=x
        self.y=y
        self.inventory=list(0 for x in range(10))
        self.equiped=list(False for x in range(10))
        self.can_g=False
        self.hp=10
        self.mp=0
        self.atk_melee=0
        self.atk_range=0
        self.atk_magic=0
        self.max_mp=0
        self.res=0
        self.res_magic=0
        self.res_effect=0
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
                    self.atk_melee=1+self.inventory[slot].atk_melee
                    self.atk_range=self.inventory[slot].atk_range
                    self.atk_magic=self.inventory[slot].atk_magic
                    self.res=self.inventory[slot].res
                    self.res_magic=self.inventory[slot].res_magic
                    self.res_range=self.inventory[slot].res_effect
        else:
            self.atk_melee=1
            self.atk_range=0
            self.atk_magic=0
            self.res=0
            self.res_magic=0
            self.res_effect=0
            if self.hp<1:
                game_over=True

#spawn player
player=Player(8,4,name)
entities.append(player)
entities.append(Entity(2,4,"H"))


#game=======================
open_inventory = False
for i in range(0,18):
    for j in range(0,50):
        win.addch(i,j,"+")
while game_over==False:
    if resume==True:
        win.refresh()

		#menu screen
        for i in range(1,17):
            for j in range(34,49):
                win.addch(i,j," ")
        win.addstr(1,35,"HP:")
        win.addstr(1,38,str(player.hp))

        win.addstr(2,35,"MP:")
        win.addstr(2,38,str(player.mp))

        win.addstr(3,35,"ATK:")
        
        win.addstr(4,35,"MLE:")
        win.addstr(4,39,str(player.atk_melee))
        win.addstr(5,35,"RNG:")
        win.addstr(5,39,str(player.atk_range))
        win.addstr(6,35,"MGC:")
        win.addstr(6,39,str(player.atk_magic))

        win.addstr(7,35,"RES:")
        win.addstr(8,35,"PHY:")
        win.addstr(8,39,str(player.res))

        win.addstr(9,35,"MGC:")
        win.addstr(9,39,str(player.res_magic))

        win.addstr(10,35,"EFF:")
        win.addstr(10,39,str(player.res_effect))

        win.addstr(14,35,"SCORE:")
        win.addstr(15,35,str(player.score))
        
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
        
        #spec message
        win.addstr(16,1,msg)
        msg = ""
        
        #draw weapons
        for i in items:
            xx=-player.x+i.x+17
            yy=-player.y+i.y+9
            if i.x==player.x and i.y==player.y and player.can_g:
                player.grab(i)
            if xx>0 and xx<32 and yy>0 and yy<16:
                win.addch(yy,xx,"?")
        if not(world[player.y+player.aim_y][player.x+player.aim_x] in coll):
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
                win.addch(yy,xx,i.symbol)

    #input
        player.can_g=False
    i=win.getch()
    if i!=-1:
        resume=True
    else: resume=False

    if i==curses.KEY_DOWN:
        is_free = len(tuple(filter(lambda e: e.x==player.x and e.y==player.y+1,entities)))==0
        if not(world[player.y+1][player.x] in coll):
            player.aim_y=1
            player.aim_x=0
            if is_free:
                player.y+=1
            else:
                player.attack(tuple(filter(lambda e: e.x==player.x and e.y==player.y+1,entities))[0])

    elif i==curses.KEY_LEFT:
        is_free = len(tuple(filter(lambda e: e.x==player.x-1 and e.y==player.y,entities)))==0
        if not(world[player.y][player.x-1] in coll):
            player.aim_y=0
            player.aim_x=-1
            if is_free:
                player.x-=1
            else:
                player.attack(tuple(filter(lambda e: e.x==player.x-1 and e.y==player.y,entities))[0])

    elif i==curses.KEY_RIGHT:
        is_free = len(tuple(filter(lambda e: e.x==player.x+1 and e.y==player.y,entities)))==0
        if not(world[player.y][player.x+1] in coll):
            player.aim_y=0
            player.aim_x=1
            if is_free:
                player.x+=1
            else:
                player.attack(tuple(filter(lambda e: e.x==player.x+1 and e.y==player.y,entities))[0])

    elif i==curses.KEY_UP:
        is_free = len(tuple(filter(lambda e: e.x==player.x and e.y==player.y-1,entities)))==0
        if not(world[player.y-1][player.x] in coll):
            player.aim_y=-1
            player.aim_x=0
            if is_free:
                player.y-=1
            else:
                player.attack(tuple(filter(lambda e: e.x==player.x and e.y==player.y-1,entities))[0])

    elif i==103:#g
        player.can_g=True

    elif i==113:#q
        player.drop()

    elif i==97:#a
        player.attack()

    if i==105:
        open_inventory = True

#game over screen
win.addstr(9,0," "*50)
win.addstr(9,17,"GAME OVER")
win.refresh()
time.sleep(1)
curses.endwin()