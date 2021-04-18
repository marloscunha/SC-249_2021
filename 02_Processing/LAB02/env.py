import pdb

class FlowField():
    def __init__(self, Resolution):
        
         # Resolution of grid relative to window width and height in pixels
        self.resolution = Resolution
        
        # Grid information
        self.rows = int(height/Resolution)
        self.cols = int(width/Resolution)
        
        #Vector that will store the field components:
        self.field = [[PVector(0,0)]*self.cols]*self.rows
        
        #Flow Status
        self.status = 0
        
    # Sets up the flow field
    # fieldID = 0: stationary flow field.
    # fieldID = 1: random flow field.
    # fieldID = 3: perlin noise.
    def setField(self, fieldID, maxMag=1):
        xoff = 0
        yoff = 0
        self.status = fieldID

        for row in range(self.rows): 
            for col in range(self.cols):
                if fieldID == 0: # No flow field
                    self.field[row][col] = PVector(0,0)

                elif fieldID == 1: # Random 
                    self.field[row][col] = PVector.mult(PVector.random2D(),maxMag)
                
                elif fieldID == 2: #Perlin noise
                    theta = map(noise(xoff,yoff), 0, 1, 0, TWO_PI)
                    self.field[row][col] = PVector(cos(theta), sin(theta))
                    yoff += 0.1
            if fieldID == 2:
                xoff += 0.1
                yoff = 0
    
    # Returns the field value at a given position:
    def getField(self, Pose=PVector(0,0)):
        col = int(constrain(Pose.x/self.resolution, 0, self.cols-1))
        row = int(constrain(Pose.y/self.resolution, 0, self.rows-1))

        return self.field[row][col].copy()

class env():
    def __init__(self, resolution=10):
        self.envResolution = 10 # Resolution set to 10 pixels.
        self.windFlow = FlowField(self.envResolution)
    
    def activateWind(self, flag_wind):
        self.windFlow.setField(flag_wind)        
            
    def updateEnv(self, WP, vehicle, flag_wind=0):
        # Vehicle's inner forces and commands:    
        InnLoop_outAcc, InnLoop_outSpd, InnLoop_outPos, distTarget_mag = vehicle.generateCommands(WP)
        
        WP.updateTarget(distTarget_mag)
        
        # Outer forces and commands:
        outerAcc, outerSpd, outerPos = PVector(0,0), PVector(0,0), self.windFlow.getField(vehicle.Pos)
        
        # Overall effect:
        outAcc = InnLoop_outAcc + outerAcc
        outSpd = InnLoop_outSpd + outerSpd
        outPos = InnLoop_outPos + outerPos
            
        vehicle.updatePose(outAcc, outSpd, outPos)
        
