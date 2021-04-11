'''
This class shall handle with creation of Waypoints that will be followed by the walker. 

Still have to include:
- Linear walker with constant speed

'''

class waypoint():
    def __init__(self, wSize, hSize):
        
        self.currWP = PVector(0,0)
        self.prevWP = PVector(0,0)
        
        # Status = {captured, chasing, skipped}
        self.currWP_status = 'chasing'
        self.prevWP_status = 'chasing'
        
        self.maxSpd = 1
        self.maxForce = 0.1
        
        self.window_wSize = wSize
        self.window_hSize = hSize
        
    def generateTarget(self, WPstatus):
        # Generates a new random target.
        self.prevWP = self.currWP.copy()
        self.prevWP_status = WPstatus
        self.currWP = PVector(random(1) * self.window_wSize, random(1) * self.window_hSize)
        self.currWP_status = 'chasing'
    
    def updateTarget(self, WPstatus, newTarget=None):
        # 0  : captured
        # -1 : skip
        # >0 : chasing 

        if WPstatus == 0: #Captured
            self.generateTarget('captured')
            print(str(self.prevWP) + ': ' + self.prevWP_status + ' || ' + str(self.currWP) + ': '+ self.currWP_status)

        elif WPstatus == -1 and newTarget != None: #Skipping and following a new WP.
            self.prevWP = self.currWP.copy()
            self.prevWP_status = 'skipped'
            self.currWP = newTarget
            self.currWP_status = 'chasing'
            
            print(str(self.prevWP) + ': ' + self.prevWP_status + ' || ' + str(self.currWP) + ': '+ self.currWP_status)
                
    def generateCommands(self, walkerPos, walkerSpd, walkerAcc):
        
        flag_useAcc = 0
        flag_useNoise = 0
        
        deltaPath = PVector.sub(self.currWP, walkerPos)     
        
        self.updateTarget(deltaPath.mag())
        
        desSpd = deltaPath.copy().limit(self.maxSpd) # Desired Speed
        
        steering = PVector.sub(desSpd,walkerSpd).limit(self.maxForce)
        
        if flag_useNoise == 0:
            randomNoise = PVector(0,0)
        else:
            randomNoise = PVector.random2D().mult(0.14) 
        
        outAcc = PVector.add(PVector.add(walkerAcc, steering), randomNoise)
        outSpd = PVector.add(walkerSpd, outAcc).limit(self.maxSpd)
        if flag_useAcc == 0:
            outPos = PVector.add(walkerPos, desSpd)
        else:
            outPos = PVector.add(walkerPos, outSpd)
        
        return outAcc, outSpd, outPos
