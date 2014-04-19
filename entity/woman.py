from entity.human import Human

class Woman(Human):
    def getPersonalPronoun(self):
        return 'she'
    
    def handleReceiveSearch(self,
                            searchingAgent,
                            entityToSearchWith=None):
        self.speak('Keep your hands off, mister.')
