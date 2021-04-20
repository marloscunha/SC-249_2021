import pdb

class vehicle():
    
    # Default walker properties
    def __init__(self, x0, y0, vx_0, vy_0, ax_0, ay_0, printSize, printColor):
        self.Pos = PVector(x0, y0)
        self.Spd = PVector(vx_0, vy_0)
        self.Acc = PVector(ax_0, ay_0)
        
        self.angProj = 0
        self.rotClockwise = 1
        self.refDeptAngle = 'target' # 'target' or 'self'
        
        self.angSpd = 1
        self.MaxSpd = 4
        self.MaxForce = 0.1
        
        self.state = 3
        self.subState = 0
        
        self.WPtol = 2
        
        self.stayAtRadius = 100
        self.stayAtThreshold = 30
        self.hop_ahead = 25
        
        self.tgtAngPos = 0
        self.tgtDist = 0
        
        self.prevWP = PVector(0,0,0)
        self.nextWP = PVector(0,0,0)
        self.currWP = PVector(0,0,0)
                      
        self.wh = printSize
        self.Color = printColor
    
    def updatePose(self, outAcc, outSpd, outPos): 
        self.Acc = outAcc
        self.Spd = outSpd
        self.Pos = outPos
        
        self.Pos.x = (self.Pos.x+width)  % width
        self.Pos.y = (self.Pos.y+height) % height
        
    def generateCommands(self, WPlist):
        
        if self.state == 1: # Waypoint capture with Stay at
            pathToFollow           = self.genPath(WPlist)
            desSpd, distTarget_mag = self.captureWP(pathToFollow[0])
                
        elif self.state == 2: # Circle around with or without Future Position
            #pathToFollow                   = self.genPath(WPlist)
            desSpd, distTarget_mag, thrash = self.circleAround(flag_futurePos=1)
            
        elif self.state == 3: # Figure 8 Navigation. (2D implementation)

            pathToFollow           = self.genPath(WPlist, flag_rotClockwise=self.rotClockwise)
            desSpd, distTarget_mag = self.eightNav(pathToFollow, flag_rotClockwise=self.rotClockwise)            
            
        steering = PVector.sub(desSpd, self.Spd).limit(self.MaxForce)
            
        outAcc = PVector.add(PVector(0), steering)
        outSpd = PVector.add(self.Spd, outAcc).limit(self.MaxSpd)
        outPos = PVector.add(self.Pos, outSpd)
                
        return outAcc, outSpd, outPos, distTarget_mag
        
    def eightNav(self, pathToFollow, flag_rotClockwise=1):
        
        # Unpacking of the trajectory points
        C1_in, C1_out, C2_in, C2_out, C1, Target, C2, Cout_deg = pathToFollow
                                            
        # Enters C1 through C1_in:
        if self.subState == 0: # Circle around C1
            self.currWP = C1_in
            self.nextWP = C1
            desSpd, distTarget_mag  = self.captureWP(self.currWP)
            if distTarget_mag <= self.WPtol:
                self.currWP = C1
                self.subState += 1
                
        # Go to C1 and circle around it until C1_out is reached
        elif self.subState == 1: # Circle around C1
            self.currWP = C1
            self.nextWP = C2_in
            desSpd, distTarget_mag, tgtAngPos  = self.circleAround(flag_futurePos=1, flag_direction=flag_rotClockwise,flag_plot=0)
            self.tgtAngPos = tgtAngPos
            if self.checkAngCapture(Cout_deg, tgtAngPos):
                self.currWP = C2_in
                self.subState += 1
        
        elif self.subState == 2: # Move from C1_out to C2_in
            self.currWP = C2_in
            self.nextWP = C2
            desSpd, distTarget_mag  = self.captureWP(self.currWP)
            if distTarget_mag <= self.WPtol:
                self.currWP = C2
                self.subState += 1
                
        elif self.subState == 3: # Circle around C2
            self.currWP = C2
            self.nextWP = C1_in
            desSpd, distTarget_mag, tgtAngPos  = self.circleAround(flag_futurePos=1, flag_direction=-flag_rotClockwise, flag_plot=0)
            self.tgtAngPos = tgtAngPos
            if self.checkAngCapture(Cout_deg, tgtAngPos):
                self.currWP = C1_in
                self.subState += 1
        
        elif self.subState == 4: # Move from C2_out to C1_in
            self.currWP = C1_in
            self.nextWP = C1
            desSpd, distTarget_mag  = self.captureWP(self.currWP)
            if distTarget_mag <= self.WPtol:
                self.currWP = C1
                self.subState = 1
        else:
            desSpd = PVector(0,0,0)
        
        distTarget_mag = PVector(9999,0,0).mag() # infinite looping
        
        return  desSpd, distTarget_mag

    def checkAngCapture(self, Cout_deg, tgtAngPos):
        if self.refDeptAngle == 'target':
            ref_departureAngle = tgtAngPos
        else:
            ref_departureAngle = self.angProj
            
        return ref_departureAngle >= (Cout_deg - PI/18) and ref_departureAngle <= (Cout_deg + PI/18)
    
    def alongPathDist(self, path):
        # Returns the distance from the vehicle to the target along the trajectory path.
        a = 1
    
    def captureWP(self, Target):
        distTarget     = PVector.sub(Target, self.Pos)
        distTarget_mag = distTarget.mag()
        self.tgtDist = distTarget_mag
        
        # Desired Speed:
        if distTarget_mag < 100:             
            m = map(distTarget_mag, 0, 100, 2, self.MaxSpd)
            desSpd = PVector.mult(distTarget.normalize(), m)
        else:
            desSpd = PVector.mult(distTarget.normalize(), self.MaxSpd) # Desired Speed
                        
        return desSpd, distTarget_mag
    
    def circleAround(self, flag_futurePos=1, flag_direction=1, flag_plot=1):
        # flag_futurePos =  1 : use future position;  0 : don't use future position
        # flag_direction =  1 : clockwise rotation ; -1 : anti clockwise rotation 
        
        if flag_futurePos == 1:
            fut_Pos = self.Spd.copy().normalize().mult(self.hop_ahead)
            fut_Pos.add(self.Pos)
            
            print(fut_Pos, self.Pos, PVector.sub(fut_Pos,self.Pos))
            distToCenter   = PVector.sub(self.currWP, fut_Pos)
        else:
            distToCenter   = PVector.sub(self.currWP, self.Pos)
        
        centerToBorder = distToCenter.copy().normalize().mult(-self.stayAtRadius)
        distToBorder   = PVector.add(distToCenter,centerToBorder)
        theta = atan2(centerToBorder.y,centerToBorder.x)
        target = PVector(self.stayAtRadius * cos(theta), self.stayAtRadius * sin(theta)).add(self.currWP)

        # Vehicle's angular projection onto the circle 
        vehicleProjection = PVector.sub(self.currWP, self.Pos).normalize().mult(-self.stayAtRadius)
        self.angProj = atan2(vehicleProjection.y, vehicleProjection.x) 
        
        if distToBorder.mag() > self.stayAtThreshold:
            m = map(distToBorder.mag(), self.stayAtThreshold, self.stayAtThreshold+2 , 0.1, self.MaxSpd)
            desSpd = PVector.mult(distToBorder.normalize(), m)
            distToTarget = distToBorder.mag()            
        else:
                   
            theta += flag_direction*self.angSpd          
            vectToTarget = PVector.sub(target, self.Pos)
            distToTarget = vectToTarget.mag()
            desSpd = vectToTarget.copy().limit(self.MaxSpd)
        
        if flag_plot == 1:        
                ellipse(self.currWP.x,self.currWP.y,2*self.stayAtRadius,2*self.stayAtRadius)
                fill(0, 0, 255)
                line(self.Pos.x, self.Pos.y, target.x, target.y)
                ellipse(target.x, target.y, 6, 6)
                fill(0, 255, 0)
                ellipse(self.currWP.x+vehicleProjection.x,self.currWP.y+vehicleProjection.y, 6, 6)
                fill(255)
        
        changeWP = 9999999 # This will ensure that the WP-capture is bypassed
        self.tgtDist = distToTarget
        return desSpd, changeWP, theta
                                   
    def genPath(self, WPlist, flag_rotClockwise=1, plot_path=1, flag_futurePos=1):
        if self.state == 1: # Waypoint capture with Stay at
            Target = WPlist.currWP
            if plot_path:
                line(self.Pos.x, self.Pos.y, Target.x, Target.y)
                ellipse(Target.x, Target.y, 6, 6)
            
            return [Target]
                
        elif self.state == 2: # Circle around with or without Future Position
            if flag_futurePos == 1:
                fut_Pos = self.Spd.copy().normalize().mult(hop_ahead)
                fut_Pos.add(self.Pos)
                distToCenter   = PVector.sub(self.currWP, fut_Pos)
            else:
                distToCenter   = PVector.sub(self.currWP, self.Pos)
        
            centerToBorder = distToCenter.copy().normalize().mult(-self.stayAtRadius)
            distToBorder   = PVector.add(distToCenter,centerToBorder) 
            
            
            
            
            if plot_path == 1:        
                ellipse(self.currWP.x,self.currWP.y,2*self.stayAtRadius,2*self.stayAtRadius)
                fill(0, 0, 255)
                line(self.Pos.x, self.Pos.y, target.x, target.y)
                ellipse(target.x, target.y, 6, 6)
                fill(0, 255, 0)
                ellipse(self.currWP.x+centerToBorder.x,self.currWP.y+centerToBorder.y, 6, 6)
                fill(255)
            
        elif self.state == 3: # Figure 8 Navigation. (2D implementation)
            Target = WPlist.currWP
            C1     = WPlist.nextWP
            
            # Generates the position vector and its unitary vector.
            C1_to_Target = PVector.sub(C1, Target)
            C1_to_Target_unit = C1_to_Target.copy().normalize()
            
            # If C1 is located more than a given threshold, 
            # re-generate C1 at a 2*radius distance from the Target
            if C1_to_Target.mag() > 2 * self.stayAtRadius:
                C1 = PVector(Target.x + 2 * self.stayAtRadius * C1_to_Target_unit.x,
                            Target.y + 2 * self.stayAtRadius * C1_to_Target_unit.y) 
            
            # Space definition of other needed elements for the 8 Navigation.
            C2     = PVector(Target.x - 2 * self.stayAtRadius * C1_to_Target_unit.x,
                            Target.y - 2 * self.stayAtRadius * C1_to_Target_unit.y) 
            
            pahtPoints = [PVector(C1.x + self.stayAtRadius * -C1_to_Target_unit.y, C1.y + self.stayAtRadius *  C1_to_Target_unit.x), 
                        PVector(C1.x - self.stayAtRadius * -C1_to_Target_unit.y, C1.y - self.stayAtRadius *  C1_to_Target_unit.x),
                        PVector(C2.x + self.stayAtRadius * -C1_to_Target_unit.y, C2.y + self.stayAtRadius *  C1_to_Target_unit.x),
                        PVector(C2.x - self.stayAtRadius * -C1_to_Target_unit.y, C2.y - self.stayAtRadius *  C1_to_Target_unit.x)]
            
            if flag_rotClockwise == 1:   # Clockwise rotation
                C1_out = pahtPoints[0]
                C1_in  = pahtPoints[1]
                C2_out = pahtPoints[2]
                C2_in  = pahtPoints[3]
                Cout_deg = PI/2
            
            elif flag_rotClockwise == -1: # Anticlockwise rotation
                C1_in  = pahtPoints[0]
                C1_out = pahtPoints[1]
                C2_in  = pahtPoints[2]
                C2_out = pahtPoints[3]
            
                Cout_deg = -PI/2
            
            if plot_path:
                arc(C1.x, C1.y, 2*self.stayAtRadius, 2*self.stayAtRadius, 3*PI/2, 5*PI/2, OPEN)
                arc(C2.x, C2.y, 2*self.stayAtRadius, 2*self.stayAtRadius, PI/2, 3*PI/2, OPEN)
                line(C1_out.x, C1_out.y, C2_in.x, C2_in.y)
                line(C2_out.x, C2_out.y, C1_in.x, C1_in.y)
                line(self.Pos.x, self.Pos.y, self.currWP.x, self.currWP.y)
            
        return [C1_in, C1_out, C2_in, C2_out, C1, Target, C2, Cout_deg] 
    
    def plotVehicle(self):       
        
        Heading = self.Spd.heading() + PI/2
        pushMatrix()
        translate(self.Pos.x, self.Pos.y)
        rotate(Heading)
        fill(self.Color[0], self.Color[1], self.Color[2])
        triangle(   0    , -self.wh,
                 -self.wh,  self.wh,
                 self.wh ,  self.wh)
        popMatrix()
