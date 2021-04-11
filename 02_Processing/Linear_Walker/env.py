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
            
    def updateForces(self, WP, walker, flag_wind=0):
        
        self.wind(flag_wind)
        windForce = self.generateForces()
        #print(windForce, flag_wind)
        
        WP_outAcc, WP_outSpd, WP_outPos = WP.generateCommands(walker.Pos, walker.Spd, walker.Acc)
        outAcc, outSpd, outPos = WP_outAcc, WP_outSpd, WP_outPos+windForce
        walker.updatePose(outAcc, outSpd, outPos)
        
