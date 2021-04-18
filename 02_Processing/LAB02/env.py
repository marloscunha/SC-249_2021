class FlowField():
    def __init__(self, Resolution):
        
         # Resolution of grid relative to window width and height in pixels
        self.resolution = resolution
        
        # Grid information
        self.cols = width/Resolution
        self.rows = height/Resolution
        
        #Vector that will store the field components:
        field = [[PVector(0,0)]*cols]*rows
        
    # Sets up the flow field
    # fieldID = 0: stationary flow field.
    # fieldID = 1: random flow field.
    # fieldID = 3: perlin noise.
    def setField(self, fieldID):
        xoff = 0
        yoff = 0
        for row in len(range(self.rows)): 
            for col in len(range(self.cols)):
                if fieldID == 0: # No flow field
                    field[row][col] = PVector(0,0)

                elif fieldID == 1: # Random values from 0 to 10.
                    field[row][col] = PVector.mult(PVector.random2D(),10)
                
                elif fieldID == 2: #Perlin noise
                    theta = map(noise(xoff,yoff), 0, 1, 0, TWO_PI)
                    field[row][col] = PVector(cos(theta), sin(theta))
                    yoff += 0.1
            if fieldID == 2:
                xoff += 0.1
                yoff = 0
    
    # Returns the field value at a given position:
    def getField(self, Pose):
        col = constrain(Pose.x/self.resolution, 0, self.cols-1)
        row = constrain(Pose.x/self.resolution, 0, self.rows-1)
        
        return self.field[row][col].copy()

class env():

    def __init__(self):
        self.windVec = PVector(0,0)
    
    def wind(self, flag_wind):
        if flag_wind == 1:
            self.windVec.set(-0.5,0.5)
        elif flag_wind == -1:
            self.windVec.set(-1,1)
    
    def generateForces(self):
        
        windForce = self.windVec
        return windForce
    
    
            
    def updateEnv(self, WP, walker, flag_wind=0):
        windForce = self.generateForces()
        #print(windForce, flag_wind)
        
        # Inner forces and commands:    
        InnLoop_outAcc, InnLoop_outSpd, InnLoop_outPos, distTarget_mag = walker.generateCommands(WP)
        
        WP.updateTarget(distTarget_mag)
        
        # Outer forces and commands:
        outerAcc, outerSpd, outerPos = PVector(0,0), PVector(0,0), windForce
        
        # Overall effect:
        outAcc = InnLoop_outAcc + outerAcc
        outSpd = InnLoop_outSpd + outerSpd
        outPos = InnLoop_outPos + outerPos
            
        walker.updatePose(outAcc, outSpd, outPos)
        
