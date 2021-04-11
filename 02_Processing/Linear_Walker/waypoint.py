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
                
    
