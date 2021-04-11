'''
This class shall handle with creation of Waypoints that will be followed by the walker. 

Still have to include:
- Linear walker with constant speed
- Mouse-click waypoint follower.

'''

class waypoint():
    def __init__(self, wSize, hSize):
        
        self.currWP = PVector(0,0)
        
        self.window_wSize = wSize
        self.window_hSize = hSize
        
    def generateTarget(self):
        self.currWP = PVector(random(1) * self.window_wSize, random(1) * self.window_hSize)
        
    def generateCommands(self, walkerPos):
        deltaPath = PVector.sub(self.currWP, walkerPos)
        if deltaPath.mag() == 0:
            self.generateTarget()
        
        return deltaPath.limit(6)
