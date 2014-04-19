from entity.human import Human

class Man(Human):
    def getPersonalPronoun(self):
        return 'he'
    
    def getObjectivePronoun(self):
        return 'him'
    
    def handleReceiveSearch(self,
                            searchingAgent,
                            entityToSearchWith=None):
        self.speak('Are you looking for a fight?')