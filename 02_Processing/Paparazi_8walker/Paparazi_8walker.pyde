from walker import walker
from waypoint import waypoint

def setup():
    size(800, 600)
    background(255)
    
    global walker01, walker02, t0, tn, sim_time, sim_step, WP
    walker01 = walker(width, height, x0=100 , y0=100, vx_0=1, vy_0=3.3, printSize=16, printColor=[255, 255, 255])
    walker02 = walker(width, height, x0=200 , y0=200, vx_0=1, vy_0=3.3, printSize=16, printColor=[255, 192, 203])
    WP = waypoint(width, height)
       
    # Simulation properties
    sim_step = 1.0/60.0
    sim_time = 0.0
    
    
def draw():
    global t0, tn, sim_time, sim_step  
        
    WP.updateWP(sim_time)
    
    # Will run the simulation for 1 seccond.
    sim_time += sim_step
    if (sim_time > 1):
        sim_time = 1
    
    fill(255)
    ellipse(WP.posNow.x, WP.posNow.y, 16, 16)
    
    walker02.plotWalker()
            
def mouseClicked():
    global sim_time
    WP.posNow.set(WP.posToGo)
    
    WP.posToGo.x = mouseX
    WP.posToGo.y = mouseY
    
    # Teleports the Walker
    #walker02.overridePose(x_over=mouseX, y_over=mouseY)
    
    # Tells the walker to go to the mouse cursor.
    

    sim_time = 0   
    
    
# Como criar uma classe ao clicar o mouse o draw() entender isso e seguir plotando esse novo walker?    
