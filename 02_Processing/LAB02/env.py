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
        
