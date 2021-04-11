class walker():
    
    # Default walker properties
    def __init__(self, wSize, hSize, x0, y0, vx_0, vy_0, ax_0, ay_0, printSize, printColor):
        self.Pos = PVector(x0, y0)
        self.Spd = PVector(vx_0, vy_0)
        self.Acc = PVector(ax_0, ay_0)
        
        self.MaxSpd = 4
        self.MaxForce = 0.1
               
        self.wh = printSize
        self.Color = printColor
        
        self.window_wSize = wSize
        self.window_hSize = hSize
    
    def updatePose(self, outAcc, outSpd, outPos): 
        self.Acc = outAcc
        self.Spd = outSpd
        self.Pos = outPos
        
        self.Pos.x = (self.Pos.x+self.window_wSize) % self.window_wSize
        self.Pos.y = (self.Pos.y+self.window_hSize) % self.window_hSize
        
        
    def generateCommands(self, currWP):
        flag_useAcc = 0         # Temporary
        
        #Distance between Target and Vehicle.                        
        distTarget     = PVector.sub(currWP, self.Pos)     
        distTarget_mag = distTarget.mag()
                 
        # Desired Speed:
        if distTarget_mag < 100:
            m = map(distTarget_mag, 0, 100, 0, self.MaxSpd)
            desSpd = PVector.mult(distTarget.normalize(), m)
        else:
            desSpd = PVector.mult(distTarget.normalize(), self.MaxSpd) # Desired Speed

        steering = PVector.sub(desSpd,self.Spd).limit(self.MaxForce)
        
        outAcc = PVector.add(PVector(0), steering)
        outSpd = PVector.add(self.Spd, outAcc).limit(self.MaxSpd)
        outPos = PVector.add(self.Pos, outSpd)
        
        print(distTarget_mag, self.Spd)
        return outAcc, outSpd, outPos, distTarget_mag
               
    def plotWalker(self):       
        
        theta = self.Spd.heading() + PI/2
        pushMatrix()
        translate(self.Pos.x, self.Pos.y)
        rotate(theta)
        fill(self.Color[0], self.Color[1], self.Color[2])
        triangle(   0    , -self.wh,
                 -self.wh,  self.wh,
                 self.wh ,  self.wh)
        popMatrix()        
        #print(self.Spd.heading())
