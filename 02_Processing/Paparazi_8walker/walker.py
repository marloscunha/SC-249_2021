class walker():
    # Default walker properties
    def __init__(self, wSize, hSize, x0, y0, vx_0, vy_0, printSize, printColor):
        self.Pos = PVector(x0, y0)
        self.Spd = PVector(vx_0, vy_0)
        
        self.Tgt_Pos = PVector(wSize/2, hSize/2)
        
        self.wh = printSize
        self.Color = printColor
        
        self.window_wSize = wSize
        self.window_hSize = hSize
    
    def updatePose(self, sim_time): 
        #Linear Walker with Bouncing:
        self.Pos = PVector.mult(self.Pos, 1 - sim_time)
        self.Pos = self.Pos.add(PVector.mult(self.Tgt_Pos,sim_time))

        if (self.Pos.x > self.window_wSize or self.Pos.x < 0):
            self.Spd.x *= -1
        if (self.Pos.y > self.window_hSize or self.Pos.y < 0): 
            self.Spd.y *= -1
    
    # Will teleport the Walker to a new position and/or change its velocity vector.
    def overridePose(self, x_over=None, y_over=None, xspd_over=None, yspd_over=None):
        if x_over != None:
            self.Pos.x = x_over
        if y_over != None:
            self.Pos.y = y_over
        if xspd_over != None:
            self.Spd.x  = xspd_over
        if yspd_over != None:
            self.Spd.y  = yspd_over
            
    def plotWalker(self, sim_time):
        self.updatePose(sim_time)
        fill(self.Color[0], self.Color[1], self.Color[2])
        ellipse(self.Pos.x, self.Pos.y, self.wh, self.wh)
        fill(255)
        #print(self.Spd.heading())
