'''
This class shall handle with creation of Waypoints that will be followed by the walker. 

Still have to include:
- Linear walker with constant speed


Deveria mandar uma lista e nao assim...

'''

class waypoint():
    def __init__(self, wSize, hSize):
        
        self.currWP = PVector(0,0)
        self.prevWP = PVector(0,0)
        self.nextWP = PVector(0,0)
        
        # Status = {captured, chasing, skipped}
        self.currWP_status = 'chasing'
        self.prevWP_status = 'chasing'
        self.nextWP_status = 'chasing'
        
        self.captureTol = 2
        
        self.WPtype = 1 
        
        self.radius = 1

        self.window_wSize = wSize
        self.window_hSize = hSize
        
    def generateTarget(self, WPstatus):
        # Gerar automaticamente os WPs (next, current e ja trocar automaticamente)    
        if self.WPtype == 1: # Generates a new random target.
            self.prevWP = self.currWP.copy()
            self.prevWP_status = WPstatus
            self.currWP = PVector(random(1) * self.window_wSize, random(1) * self.window_hSize)
            self.currWP_status = 'chasing'
            self.nextWP = PVector.add(self.currWP,PVector(200,0,0))
            self.nextWP_status = 'chasing'
        
        elif self.WPtype == 2: # Generates an Eight-Navigation-Scheme
            print('aqui')
            
    def setWPtype(self, WPtypeID):
        self.WPtype = WPtypeID
        print('Waypoint Type: ' + str(self.WPtype))
           
    def updateTarget(self, distTarget_mag, newTarget=None):
        # 0  : captured
        # -1 : skip
        # >0 : chasing 

        if distTarget_mag >=0: 
            if distTarget_mag <= self.captureTol: #Captured
                self.generateTarget('captured')
                print(str(self.prevWP) + ': ' + self.prevWP_status + ' || ' + str(self.currWP) + ': '+ self.currWP_status)

        elif distTarget_mag == -1 and newTarget != None: #Skipping and following a new WP.            
            
            self.prevWP, self.prevWP_status = self.currWP.copy(), 'skipped'
            self.currWP, self.currWP_status = newTarget, 'chasing'
            
            self.nextWP, self.nextWP_status = PVector.add(newTarget, PVector(2*100,0,0)), 'chasing'
            
            print(str(self.prevWP) + ': ' + self.prevWP_status + ' || ' + str(self.currWP) + ': '+ self.currWP_status)
            print(self.nextWP)
                
