class walker():
    # Default walker properties
    def __init__(self, wSize, hSize, x0, y0, vx_0, vy_0, printSize, printColor):
        self.Pos = PVector(x0, y0)
        self.Spd = PVector(vx_0, vy_0)
               
        self.wh = printSize
        self.Color = printColor
        
        self.window_wSize = wSize
        self.window_hSize = hSize
    
    def updatePose(self, sim_time, WP): 
       
        self.Pos = self.Pos.add(WP.generateCommands(self.Pos))
        
        # Implements a bouncing if boundaries are exceeded: 
        if (self.Pos.x > self.window_wSize or self.Pos.x < 0):
            self.Spd.x *= -1
        if (self.Pos.y > self.window_hSize or self.Pos.y < 0): 
            self.Spd.y *= -1
               
    def plotWalker(self, sim_time, WP):
        self.updatePose(sim_time, WP)
        
        fill(self.Color[0], self.Color[1], self.Color[2])
        ellipse(self.Pos.x, self.Pos.y, self.wh, self.wh)
        fill(255)
