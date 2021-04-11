class walker():
    
    # Default walker properties
    def __init__(self, wSize, hSize, x0, y0, vx_0, vy_0, ax_0, ay_0, printSize, printColor):
        self.Pos = PVector(x0, y0)
        self.Spd = PVector(vx_0, vy_0)
        self.Acc = PVector(ax_0, ay_0)
        
        self.angSpd = 1
        self.MaxSpd = 4
        self.MaxForce = 0.1
        
        self.state = 3
        
        self.stayAtRadius = 100
        self.stayAtThreshold = 30
        self.hop_ahead = 25
                      
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
        
        if self.state == 1: # Waypoint capture with Stay at
            distTarget     = PVector.sub(currWP, self.Pos)     
            distTarget_mag = distTarget.mag()
            
            # Desired Speed:
            if distTarget_mag < 100:             
                m = map(distTarget_mag, 0, 100, 2, self.MaxSpd)
                desSpd = PVector.mult(distTarget.normalize(), m)
            else:
                desSpd = PVector.mult(distTarget.normalize(), self.MaxSpd) # Desired Speed
                
        elif self.state == 2: # Circle around
            distToCenter   = PVector.sub(currWP, self.Pos)
            centerToBorder = distToCenter.copy().normalize().mult(-self.stayAtRadius)
            distToBorder   = PVector.add(distToCenter,centerToBorder)
            ellipse(currWP.x,currWP.y,2*self.stayAtRadius,2*self.stayAtRadius)
            
            distTarget_mag = 9999999 # This will ensure that the WP-capture is bypassed.

            if distToBorder.mag() > self.stayAtThreshold:
                m = map(distToBorder.mag(), self.stayAtThreshold, self.stayAtThreshold+2 , 0.1, self.MaxSpd)
                desSpd = PVector.mult(distToBorder.normalize(), m)
                
            else:
                theta = atan2(centerToBorder.y,centerToBorder.x)
                theta += self.angSpd
                target = PVector(self.stayAtRadius * cos(theta), self.stayAtRadius * sin(theta)).add(currWP)
                
                fill(0, 0, 255)
                line(currWP.x, currWP.y, target.x, target.y)
                ellipse(target.x, target.y, 6, 6)
                fill(255)
                
                desSpd = PVector.sub(target, self.Pos).limit(self.MaxSpd)
            print(distToBorder.mag())
            fill(0, 255, 0)
            line(currWP.x, currWP.y, currWP.x+centerToBorder.x,currWP.y+centerToBorder.y)
            ellipse(currWP.x+centerToBorder.x,currWP.y+centerToBorder.y, 6, 6)
            fill(255)
            
        elif self.state == 3:
            
            fut_Pos = self.Spd.copy().normalize().mult(self.hop_ahead)
            fut_Pos.add(self.Pos)
               
            distToCenter   = PVector.sub(currWP, fut_Pos)
            centerToBorder = distToCenter.copy().normalize().mult(-self.stayAtRadius)
            distToBorder   = PVector.add(distToCenter,centerToBorder)
            ellipse(currWP.x,currWP.y,2*self.stayAtRadius,2*self.stayAtRadius)
            
            distTarget_mag = 9999999 # This will ensure that the WP-capture is bypassed.

            if distToBorder.mag() > self.stayAtThreshold:
                m = map(distToBorder.mag(), self.stayAtThreshold, self.stayAtThreshold+2 , 0.1, self.MaxSpd)
                desSpd = PVector.mult(distToBorder.normalize(), m)
                
            else:
                theta = atan2(centerToBorder.y,centerToBorder.x)
                theta += self.angSpd
                target = PVector(self.stayAtRadius * cos(theta), self.stayAtRadius * sin(theta)).add(currWP)
                
                fill(0, 0, 255)
                line(currWP.x, currWP.y, target.x, target.y)
                ellipse(target.x, target.y, 6, 6)
                fill(255)
                
                desSpd = PVector.sub(target, self.Pos).limit(self.MaxSpd)
            print(distToBorder.mag())
            fill(0, 255, 0)
            line(currWP.x, currWP.y, currWP.x+centerToBorder.x,currWP.y+centerToBorder.y)
            ellipse(currWP.x+centerToBorder.x,currWP.y+centerToBorder.y, 6, 6)
            fill(255)
            
                                                        
            
        steering = PVector.sub(desSpd, self.Spd).limit(self.MaxForce)
            
        outAcc = PVector.add(PVector(0), steering)
        outSpd = PVector.add(self.Spd, outAcc).limit(self.MaxSpd)
        outPos = PVector.add(self.Pos, outSpd)
                
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
