from walker import walker
from waypoint import waypoint
from env import env
from math import pi
import pdb

def setup():
    size(1200, 800)
    background(255)
    
    global walker01, walker02, t0, tn, sim_time, sim_step, WP, Env, flag_wind, stateEnum, subStateEnum
    walker01 = walker(width, height, x0=100 , y0=100, vx_0=1, vy_0=3.3, ax_0 = 0, ay_0 = 0, printSize=6, printColor=[255, 192, 203])
    walker02 = walker(width, height, x0=200 , y0=200, vx_0=0, vy_0=0.0, ax_0 = 0, ay_0 = 0, printSize=6, printColor=[000, 255, 00])
    WP = waypoint(width, height)
    Env = env()
    flag_wind = 0    
    
    WP.generateTarget('first')
    stateEnum = ["Position Hold", "Waypoint capture", "Circle Around", "8 Navigation"]
    subStateEnum = ["NA","Circling around C1", "Transitioning to C2", "Circling around C2", "Transitioning to C1"]

    
def draw():
    background(255)
    Env.updateEnv(WP, walker02, flag_wind)
    walker02.plotWalker()
    
    
    
    
    
    fill(255,0,0)
    textSize(12)
    text("Current state      : " + str(walker02.state) + " (" + str(stateEnum[walker02.state])  + ")", 30, 30)
    text("Current substate : " + str(walker02.subState)+ " (" + str(subStateEnum[walker02.subState])  + ")", 30, 42)
    fill(255)
            
def mouseClicked():
    global flag_wind
    if mouseButton == LEFT:
        WP.setWPtype(1) # Random
        WP.updateTarget(-1, PVector(mouseX,mouseY))
    elif mouseButton == RIGHT:
        WP.setWPtype(2) # Eight Figure
        WP.updateTarget(-1, PVector(mouseX,mouseY))
    flag_wind *= -1
