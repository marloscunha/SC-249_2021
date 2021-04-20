class waypoint():
    def __init__(self):
        
        self.currWP = PVector(0,0)
        self.prevWP = PVector(0,0)
        self.nextWP = PVector(0,0)
        
        # Status = {captured, chasing, skipped}
        self.currWP_status = 'chasing'
        self.prevWP_status = 'chasing'
        self.nextWP_status = 'chasing'
        
        self.captureTol = 2
        
    def generateTarget(self, WPstatus):
        self.prevWP = self.currWP.copy()
        self.prevWP_status = WPstatus
        self.currWP = PVector(constrain(random(1) * width,300,width-300), constrain(random(1)*height,210,height-210))
        self.currWP_status = 'chasing'
        self.nextWP = PVector.add(self.currWP,PVector(200,0,0))
        self.nextWP_status = 'chasing'
            
    def updateTarget(self, distTarget_mag, newTarget=None):
        # 0  : captured
        # -1 : skip
        # >0 : chasing 

        if distTarget_mag >=0: 
            if distTarget_mag <= self.captureTol: #Captured
                self.generateTarget('captured')
                print(str(self.prevWP) + ': ' + self.prevWP_status + ' || ' + str(self.currWP) + ': '+ self.currWP_status)

        elif distTarget_mag == -1: 
            if newTarget != None: #Skipping and following a new WP.   
                self.prevWP, self.prevWP_status = self.currWP.copy(), 'skipped'
                self.currWP, self.currWP_status = newTarget, 'chasing'
                
                self.nextWP, self.nextWP_status = PVector.add(newTarget, PVector(2*100,0,0)), 'chasing'
                
                print(str(self.prevWP) + ': ' + self.prevWP_status + ' || ' + str(self.currWP) + ': '+ self.currWP_status)
            else:
                self.generateTarget('skipped')
