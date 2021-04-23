'''


'''
class vehicle():
    
    def __init__(self, x0, y0, vx_0, vy_0, ax_0, ay_0, printSize, printColor):
        self.Pos = PVector(x0, y0)
        self.Spd = PVector(vx_0, vy_0)
        self.Acc = PVector(ax_0, ay_0)
        
        self.angProj = 0
        self.rotClockwise = 1
        self.refDepartureAngle = 'target' # 'target' or 'self'
        
        self.angSpd = 1
        self.MaxSpd = 4
        self.MaxForce = 0.1
        
        self.state = 3
        self.subState = 0
        
        self.Nav8_WParcTol = 2
        self.Nav8_WPlinTol = 50
        self.Nav_WPtol = 2
        
        self.stayAtRadius = 80
        self.stayAtThreshold = 40
        self.hop_ahead = 10
        
        self.tgtAngPos = 0
        self.tgtDist = 0
        
        self.refWP      = PVector(0,0,0) 
        self.nextTarget = PVector(0,0,0)
        self.currTarget = PVector(0,0,0)
                      
        self.wh = printSize
        self.Color = printColor
       
    def updatePose(self, outAcc, outSpd, outPos): 
        self.Acc = outAcc
        self.Spd = outSpd
        self.Pos = outPos
        
        self.Pos.x = (self.Pos.x+width)  % width
        self.Pos.y = (self.Pos.y+height) % height
        
    def generateCommands(self, WPlist):    
        # If a new WP has been generated, subState shall be reseted. This implies that the 
        # vehicle will enter the 8-Navigation through C1_in point, in case self.state = 3.
        # If other states are active, no change will be seen.
        if self.refWP != WPlist.currWP:
            self.subState = 0
            self.refWP = WPlist.currWP
             
        if self.state == 1: # Waypoint capture with Stay at
            pathToFollow           = self.genPath(WPlist)
            desSpd, distTarget_mag = self.singleWPCapture(pathToFollow[0])
                
        elif self.state == 2: # Circle around with or without Future Position
            pathToFollow                   = self.genPath(WPlist)
            desSpd, distTarget_mag, _      = self.circleAround(pathToFollow[0], flag_futurePos=1)
            
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
        if self.subState == 0: # Heads toward point C1_in.
            self.currTarget = C1_in
            self.nextTarget = C1
            desSpd, distTarget_mag  = self.singleWPCapture(self.currTarget, captureSpeed=2)
            if distTarget_mag <= self.Nav_WPtol:
                self.currTarget = C1
                self.subState += 1
                
        # Go to C1 and circle around it until C1_out is reached
        elif self.subState == 1: # Circle around C1
            self.currTarget = C1
            self.nextTarget = C1_out
            desSpd, distTarget_mag, tgtAngPos  = self.circleAround(self.currTarget, flag_futurePos=1, flag_direction=flag_rotClockwise,flag_plot=0)
            self.tgtAngPos = tgtAngPos
            if self.checkAngCapture(Cout_deg, tgtAngPos):
                self.currTarget = C2_in
                self.subState += 1
        
        # Move C1_out to C2_in                
        elif self.subState == 2: 
            self.currTarget = C2_in
            self.nextTarget = C2
            desSpd, distTarget_mag  = self.singleWPCapture(self.currTarget, captureSpeed=2)
            if distTarget_mag <= self.Nav_WPtol:
                self.currTarget = C2
                self.subState += 1
                
        elif self.subState == 3: # Circle around C2
            self.currTarget = C2
            self.nextTarget = C2_out
            desSpd, distTarget_mag, tgtAngPos  = self.circleAround(self.currTarget, flag_futurePos=1, flag_direction=-flag_rotClockwise, flag_plot=0)
            self.tgtAngPos = tgtAngPos
            if self.checkAngCapture(Cout_deg, tgtAngPos):
                self.currTarget = C1_in
                self.subState += 1
        
        elif self.subState == 4: # Move from Target to C2_in
            self.currTarget = C1_in
            self.nextTarget = C1
            desSpd, distTarget_mag  = self.singleWPCapture(self.currTarget, captureSpeed=2)
            if distTarget_mag <= self.Nav_WPtol:
                self.currTarget = C1
                self.subState = 1
        
        else:
            desSpd = PVector(0,0,0)
        
        distTarget_mag = PVector(9999,0,0).mag() # infinite looping
        
        return  desSpd, distTarget_mag

    def checkAngCapture(self, Cout_deg, tgtAngPos):
        if self.refDepartureAngle == 'target':
            ref_departureAngle = tgtAngPos
        else:
            ref_departureAngle = self.angProj
            
        return ref_departureAngle >= (Cout_deg - PI/18) and ref_departureAngle <= (Cout_deg + PI/18)
    
    def alongPathDist(self, path):
        # Returns the distance from the vehicle to the target along the trajectory path.
        # Not implemented yet
        a = 1
    
    def singleWPCapture(self, Target, captureSpeed=0):
        # Performs a single waypoint capture, using a speed reducting approach while arriving at the
        # target destination. If no other waypoint is given after the capture, vehicle shall stay at
        # the captured waypoint position.
        # 'captureSpeed' variable allow the desired waypoint to be reached with a given velocity - 
        # if enabled, vehicle will not stop at reaching the WP position.
        distTarget     = PVector.sub(Target, self.Pos)
        distTarget_mag = distTarget.mag()
        self.tgtDist   = distTarget_mag
        
        # Desired Speed:
        if distTarget_mag < 100:             
            m = map(distTarget_mag, 2, 100, captureSpeed, self.MaxSpd)
            desSpd = PVector.mult(distTarget.normalize(), m)
        else:
            desSpd = PVector.mult(distTarget.normalize(), self.MaxSpd) # Desired Speed
                        
        return desSpd, distTarget_mag
        
    def circleAround(self, pathToFollow, flag_futurePos=1, flag_direction=1, flag_plot=1):
        # flag_futurePos =  1 : use future position;  0 : don't use future position
        # flag_direction =  1 : clockwise rotation ; -1 : anti clockwise rotation 
        
        Center = pathToFollow
    
        if flag_futurePos == 1:
            ref_Pos = self.Spd.copy().normalize().mult(self.hop_ahead)
            ref_Pos.add(self.Pos)
        else:
            ref_Pos = self.Pos.copy()
        
        distToCenter   = PVector.sub(Center, ref_Pos)
        
        centerToBorder = distToCenter.copy().normalize().mult(-self.stayAtRadius)
        distToBorder   = PVector.add(distToCenter,centerToBorder)
        
        theta = atan2(centerToBorder.y,centerToBorder.x)
        theta += flag_direction*self.angSpd
        target = PVector(self.stayAtRadius * cos(theta), self.stayAtRadius * sin(theta)).add(Center)

        # Vehicle's angular projection onto the circle 
        vehicleProjection = PVector.sub(Center, self.Pos).normalize().mult(-self.stayAtRadius)
        self.angProj = atan2(vehicleProjection.y, vehicleProjection.x) 
        
        if distToBorder.mag() > self.stayAtThreshold:
            desSpd = distToBorder.limit(self.MaxSpd)
            distToTarget = distToBorder.mag()            
        else:         
            vectToTarget = PVector.sub(target, ref_Pos)
            distToTarget = vectToTarget.mag()
            desSpd = vectToTarget.copy().limit(self.MaxSpd)
        
        if flag_plot == 1:        
                    ellipse(Center.x,Center.y,2*self.stayAtRadius,2*self.stayAtRadius)
                    fill(0, 0, 255)
                    line(self.Pos.x, self.Pos.y, target.x, target.y)
                    ellipse(target.x, target.y, 6, 6)
                    fill(0, 255, 0)
                    ellipse(Center.x+vehicleProjection.x,Center.y+vehicleProjection.y, 6, 6)
                    fill(255)
                    line(self.Pos.x, self.Pos.y, ref_Pos.x, ref_Pos.y)
                    ellipse(Center.x, Center.y, 6, 6)
                
        changeWP = 9999999 # This will ensure that the WP-capture is bypassed
        self.tgtDist = distToTarget
        return desSpd, changeWP, theta
                                   
    def genPath(self, WPlist, flag_rotClockwise=1, plot_path=1, flag_futurePos=1):
        # 1 = Waypoint capture with Stay-At
        # 2 = Circle around with/witout Future Position
        # 3 = 8-Navigation
        
        if self.state == 1: # Waypoint capture with Stay at
            Target = WPlist.currWP
            if plot_path:
                line(self.Pos.x, self.Pos.y, Target.x, Target.y)
                ellipse(Target.x, Target.y, 6, 6)
            
            return [Target]
                
        elif self.state == 2: # Circle around with or without Future Position
            Center = WPlist.currWP           
            # For the time being, plotting and other things will be handled 
            # within circleAround function.
            
            return [Center]
            
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
                line(self.Pos.x, self.Pos.y, self.currTarget.x, self.currTarget.y)
                ellipse(Target.x, Target.y, 6, 6)
            
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
