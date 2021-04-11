class walker():
    
    # Default walker properties
    def __init__(self, wSize, hSize, x0, y0, vx_0, vy_0, ax_0, ay_0, printSize, printColor):
        self.Pos = PVector(x0, y0)
        self.Spd = PVector(vx_0, vy_0)
        self.Acc = PVector(ax_0, ay_0)
        
        self.MaxSpd = 6
        self.MaxForce = 0.5
               
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
                                
        deltaPath = PVector.sub(currWP, self.Pos)     
        captureStatus = deltaPath.mag()
        
        desSpd = deltaPath.copy().limit(self.MaxSpd) # Desired Speed
        steering = PVector.sub(desSpd,self.Spd).limit(self.MaxForce)
        
        outAcc = PVector.add(self.Acc, steering)
        outSpd = PVector.add(self.Spd, outAcc).limit(self.MaxSpd)
        if flag_useAcc == 0:
            outPos = PVector.add(self.Pos, desSpd)
        else:
            outPos = PVector.add(self.Pos, outSpd)
        
        return outAcc, outSpd, outPos, captureStatus
               
    def plotWalker(self):
        global pi
        
        
        theta = self.Spd.heading() + PI/2
        pushMatrix()
        translate(self.Pos.x, self.Pos.y)
        rotate(theta)
        fill(self.Color[0], self.Color[1], self.Color[2])
        
        triangle(   0    , -self.wh,
                 -self.wh,  self.wh,
                 self.wh ,  self.wh)
        
        #triangle(self.Pos.x - self.wh/2, self.Pos.y - (((3)**(0.5))/6)*(self.wh),
        #         self.Pos.x            , self.Pos.y + (((3)**(0.5))/3)*(self.wh),
        #         self.Pos.x + self.wh/2, self.Pos.y - (((3)**(0.5))/6)*(self.wh))
        popMatrix()
        #ellipse(self.Pos.x, self.Pos.y, self.wh, self.wh)
        fill(255)
        
        print(self.Spd)
