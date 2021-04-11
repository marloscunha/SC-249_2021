from walker import walker
from waypoint import waypoint
from env import env

def setup():
    size(800, 600)
    background(255)
    
    global walker01, walker02, t0, tn, sim_time, sim_step, WP, Env, flag_wind
    walker01 = walker(width, height, x0=100 , y0=100, vx_0=1, vy_0=3.3, ax_0 = 0, ay_0 = 0, printSize=16, printColor=[255, 192, 203])
    walker02 = walker(width, height, x0=200 , y0=200, vx_0=0, vy_0=0, ax_0 = 0, ay_0 = 0, printSize=16, printColor=[0, 255, 00])
    WP = waypoint(width, height)
    Env = env()
    flag_wind = 1
    
    WP.generateTarget('first')
    print(WP.currWP)
    
def draw():    
    Env.updateForces(WP, walker02, flag_wind)
    
    walker02.plotWalker()
           
    fill(255)      
    ellipse(WP.currWP[0], WP.currWP[1], 5, 5)
    
            
def mouseClicked():
    global flag_wind
    WP.updateTarget(-1, PVector(mouseX,mouseY))
    flag_wind *= -1
    print(flag_wind)
