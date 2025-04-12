import time,os
from random import *
logo=(
"  dN   i I   Mb    NMH   Gb",
" K     l l   N D   I     F D",
"  Mb   I i   Hp    NME   HY",
"   l   q p   T     l     W q",
" jp     U    I     NMH   M  b"
)
def menu():
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
    		print("# - walls\n@ is you and others entity\n= is chest, ? is loot.\n to grab loot - stay on loot and press g.\n/ - your weapon\n* - magic effects\nu , . - decorates\n")
    return input("enter your name to start a quest!\n")
#generate world==================
def generate(atk_layer):
    world=[]
    for i in range(128):
    	world.append([])
    	atk_layer.append([])
    	for j in range(128):
    		atk_layer[i].append(0)
    		r=int(random()*100)%3
    		world[i].append(".")
    #borders
    for j in range(128):
    	world[j][0]="|"
    	world[j][127]="|"
    	world[0][j]="-"
    	world[127][j]="-"
    	
    return world