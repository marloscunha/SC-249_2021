class walker():
    # Default walker properties
    def __init__(self, wSize, hSize, x0, y0, vx_0, vy_0, ax_0, ay_0, printSize, printColor):
        self.Pos = PVector(x0, y0)
        self.Spd = PVector(vx_0, vy_0)
        self.Acc = PVector(ax_0, ay_0)
               
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
               
    def plotWalker(self):
        fill(self.Color[0], self.Color[1], self.Color[2])
        ellipse(self.Pos.x, self.Pos.y, self.wh, self.wh)
        fill(255)
        
        print(self.Spd)
