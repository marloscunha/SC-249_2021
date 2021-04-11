class env():
    def __init__(self):
        self.windVec = PVector(0,0)
    
    def wind(self, flag_wind):
        if flag_wind == 1:
            self.windVec.set(-10,10)
        elif flag_wind == -1:
            self.windVec.set(-2,2)
    
    def generateForces(self):
        windForce = self.windVec
        return windForce
            
    def updateEnv(self, WP, walker, flag_wind=0):
        global pi
        
        self.wind(flag_wind)
        windForce = self.generateForces()
        #print(windForce, flag_wind)
        
        # Inner forces and commands:
            
        WP_outAcc, WP_outSpd, WP_outPos, distTarget_mag = walker.generateCommands(WP.currWP)
        
        WP.updateTarget(distTarget_mag)
        
        # Outer forces and commands:
        outAcc, outSpd, outPos = WP_outAcc, WP_outSpd, WP_outPos+windForce
        
        # Overall effect:
        outAcc = WP_outAcc 
        outSpd = WP_outSpd 
        outPos = WP_outPos + windForce
            
        walker.updatePose(outAcc, outSpd, outPos)
        
