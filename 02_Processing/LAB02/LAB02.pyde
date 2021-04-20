from vehicle import vehicle
from waypoint import waypoint
from env import env

def setup():
    # Global variables:
    global vehicle, WP, Env, flag_wind, stateEnum, subStateEnum, windType, rotationType
    
    # Simulation definitions:
    size(800, 800) # Window display size
    resolution = 10 # Amount of pixels to be used as simulation resolution.
    background(255) # Background colour    
        
    # Initial Values
    initPos       = PVector(0,0)
    initSpd       = PVector(0,0)
    initAcc       = PVector(0,0)
    vehicleColour = [0, 255, 0]
    vehicleSize   = 6
    
    # Object instantiation:
    Env       = env(resolution)                                             # Creates the simulationational environment
    WP = waypoint()    
    WP.generateTarget('first')
    vehicle   = vehicle(x0=initPos.x , y0=initPos.y,                        # Creates a vehicle
                        vx_0=initSpd.x, vy_0=initSpd.y, 
                        ax_0 = initAcc.x, ay_0 = initAcc.y, 
                        printSize=vehicleSize, printColor=vehicleColour)
    
    # Simulation flags:
    flag_wind = 0 
    
    # Needs to be corrected.  
    
    # Simulation display info
    stateEnum    = ["None", "Waypoint capture", "Circle Around", "8 Navigation"]
    subStateEnum = [[""],[""], [""], ["Entering through C1", "Circling around C1", "From C1 to C2", "Circling around C2", "From C2 to C1"]]
    rotationType = ["Anticlockwise", "Clockwise"]
    windType     = ["None", "Random values", "Perlin Noise"]

    
def draw():
    background(255)
    Env.updateEnv(WP, vehicle, flag_wind)
    
    # Simulation status:
    fill(255,0,0)
    textSize(12)
    text("Current state      : " + str(vehicle.state) + " (" + str(stateEnum[vehicle.state])  + ")", 30, 30)
    text("Current substate : " + str(vehicle.subState)+ " (" + str(subStateEnum[vehicle.state][vehicle.subState])  + ")", 30, 42)
    
    text("Rotation : " +  rotationType[constrain(vehicle.rotClockwise,0,1)], 30, 66)
    text("Distance to target: " + str(vehicle.tgtDist), 30, 78)
    text("Wind: " + str(windType[Env.windFlow.status]), 30, 90)
    
    text("Speed: " + str(round(vehicle.Spd.mag())), 30, 102)
    
    fill(255)
            
def mouseClicked():
    if mouseButton == LEFT:
        # Sets target at the clicked location
        WP.updateTarget(-1, PVector(mouseX,mouseY))
    elif mouseButton == RIGHT:
        # Random target
        WP.updateTarget(-1)
    
def keyPressed():
    global flag_wind
    
    if key == 'w':
        if flag_wind == 2:
            flag_wind = 0
        else:
            flag_wind +=1
        Env.activateWind(flag_wind)
        
    if key == 'm':
        if vehicle.state == 3:
            vehicle.state = 1
            vehicle.subState = 0
        else:
            vehicle.state +=1 
