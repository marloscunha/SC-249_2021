from vehicle import vehicle
from waypoint import waypoint
from env import env
from math import pi
import pdb

def setup():
    size(1200, 800)
    resolution = 10 # Amount of pixels to be used as simulation resolution.
    background(255)
    
    global vehicle, WP, Env, flag_wind, stateEnum, subStateEnum, windType
    
    Env = env(resolution)
    vehicle = vehicle(x0=200 , y0=200, vx_0=0, vy_0=0.0, ax_0 = 0, ay_0 = 0, printSize=6, printColor=[000, 255, 00])
    flag_wind = 0 
    
    # Needs to be corrected.
    WP = waypoint(width, height)    
    WP.generateTarget('first')
    
    stateEnum    = ["Position Hold", "Waypoint capture", "Circle Around", "8 Navigation"]
    subStateEnum = ["NA","Circling around C1", "Transitioning to C2", "Circling around C2", "Transitioning to C1"]
    
    windType = ["None", "Random values", "Perlin Noise"]

    
def draw():
    background(255)
    Env.updateEnv(WP, vehicle, flag_wind)
    vehicle.plotVehicle()
    
    # Simulation status:
    fill(255,0,0)
    textSize(12)
    text("Current state      : " + str(vehicle.state) + " (" + str(stateEnum[vehicle.state])  + ")", 30, 30)
    text("Current substate : " + str(vehicle.subState)+ " (" + str(subStateEnum[vehicle.subState])  + ")", 30, 42)
    text("Target position  : " + str(vehicle.tgtAngPos), 30, 54)
    text("Distance to target: " + str(vehicle.tgtDist), 30, 66)
    text("Wind: " + str(windType[Env.windFlow.status]), 30, 78)
    
    fill(255)
            
def mouseClicked():
    if mouseButton == LEFT:
        WP.setWPtype(1) # Random
        WP.updateTarget(-1, PVector(mouseX,mouseY))
    elif mouseButton == RIGHT:
        WP.setWPtype(2) # Eight Figure
        WP.updateTarget(-1, PVector(mouseX,mouseY))
    
def keyPressed():
    global flag_wind
    if key == 'w':
        if flag_wind == 2:
            flag_wind = 0
        else:
            flag_wind +=1
        Env.activateWind(flag_wind)
