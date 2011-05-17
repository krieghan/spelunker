class StateMachine(object):
    
    def __init__(self, 
                 owner,
                 startingState):
        self.startingState = startingState
        self.currentState = startingState
        self.owner = owner
        
    def changeState(self,
                    newState):
        self.currentState.exit(owner=self.owner)
        self.currentState = newState
        self.currentState.enter(owner=self.owner)