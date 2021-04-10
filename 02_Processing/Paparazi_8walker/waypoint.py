class waypoint():
    def __init__(self, wSize, hSize):
        self.posNow = PVector(0,0)
        self.posToGo = PVector(wSize/2, hSize/2)
        
    def updateWP(self, sim_time):
        self.posNow = PVector.mult(self.posNow, 1 - sim_time)
        self.posNow = self.posNow.add(PVector.mult(self.posToGo,sim_time))
