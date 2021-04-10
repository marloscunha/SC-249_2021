class walker():
    # Default walker properties
    def __init__(self, wSize, hSize, x0, y0, vx_0, vy_0, printSize, printColor):
        self.xpos = x0
        self.ypos = y0
        self.xspeed = vx_0
        self.yspeed = vy_0
        self.wh = printSize
        self.Color = printColor
        self.window_wSize = wSize
        self.window_hSize = hSize
    
    def updatePose(self): 
        #Linear Walker with Bouncing:
        self.xpos += self.xspeed * 1
        self.ypos += self.yspeed * 1
        if (self.xpos > self.window_wSize or  self.xpos < 0):
            self.xspeed *= -1
        if (self.ypos > self.window_hSize or self.ypos < 0): 
            self.yspeed *= -1
    
    # Will teleport the Walker to a new position and/or change its velocity vector.
    def overridePose(self, x_over=None, y_over=None, xspd_over=None, yspd_over=None):
        if x_over != None:
            self.xpos = x_over
        if y_over != None:
            self.ypos = y_over
        if xspd_over != None:
            self.xspeed = xspd_over
        if yspd_over != None:
            self.yspeed = yspd_over
            
    def plotWalker(self):
        self.updatePose()
        fill(self.Color[0], self.Color[1], self.Color[2])
        ellipse(self.xpos, self.ypos, self.wh, self.wh)
        fill(255)
