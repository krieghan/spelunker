from entity.agent import Agent

class Human(Agent):
    
    
    def handleFeeling(self,
                      feelingAgent):
        print '%s shrinks away from your touch.'
        self.speak("Don't touch me!")