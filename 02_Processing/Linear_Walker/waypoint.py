'''
This class shall handle with creation of Waypoints that will be followed by the walker. 

Still have to include:
- Linear walker with constant speed
- Mouse-click waypoint follower.

'''

class waypoint():
    def __init__(self, wSize, hSize):
        
        self.currWP = PVector(0,0)
        
        self.maxSpd = 6
        self.maxForce = 0.1
        
        self.window_wSize = wSize
        self.window_hSize = hSize
        
    def generateTarget(self):
        self.currWP = PVector(random(1) * self.window_wSize, random(1) * self.window_hSize)
        
    def generateCommands(self, walkerPos, walkerSpd, walkerAcc):
        deltaPath = PVector.sub(self.currWP, walkerPos)        
        if deltaPath.mag() == 0:
            self.generateTarget()
            print("Captured")
        
        desSpd = deltaPath.copy().limit(self.maxSpd) # Desired Speed
        
        steering = PVector.sub(desSpd,walkerSpd).limit(self.maxForce)
        #randomNoise = PVector.random2D().mult(0.14)
        randomNoise = PVector(0,0)
        
        outAcc = PVector.add(PVector.add(walkerAcc, steering), randomNoise)
        outSpd = PVector.add(walkerSpd, outAcc).limit(self.maxSpd)
        outPos = PVector.add(walkerPos, outSpd)
        
        return outAcc, outSpd, outPos
