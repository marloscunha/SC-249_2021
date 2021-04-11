from walker import walker
from waypoint import waypoint
import pdb

r = 400
theta = 0
angVel = 0.9
maxspeed = 6
maxforce = 2

center = PVector()
vel = PVector()
accel = PVector()
pos = PVector()
ballRed = False

def setup():
    size(800, 800)
    background(255)
    smooth()
    
    global pos, center, maxspeed, vel, maxforce
    pos.set(400.5, 400.5)
    center.set(width/2, height/2)
    
    seek_around(center, r)
 
def seek_around(center, radius):
    
    global maxspeed
    
    desired = PVector()
    posToCenter = PVector.sub(center, pos)
    centerToPerimeter = posToCenter.normalize().mult(-radius)
    posToPerimeter = PVector.add(posToCenter, centerToPerimeter)
    
    if posToPerimeter.mag() > 60:
        desired = posToPerimeter.limit(maxspeed)
        ballRed = False
        
    else:
        print("aqui")
    
    steer = PVector.sub(desired, vel)
    steer.limit(maxforce)
    return steer

def update():
    vel.add(accel)
    vel.limit(maxspeed)
    pos.add(vel)

 
def draw():
    background(255)
    stroke(0)
    fill(255)
    ellipse(center.x, center.y, r*2, r*2)
    accel.set(0,0)
    
    steer = seek_around(center, r) 
    accel.add(steer)

    update() 
    noStroke()
    if ballRed:
        fill(255,0,0)
    else:
        fill(0)
    ellipse(pos.x, pos.y, 6, 6)

def mouseClicked():
    center.set(mouseX, mouseY)
    r = 50
    
