from entity.item import Item

class Key(Item):
    def handleDoingUnlock(self,
                       unlockingAgent):
        return True
    
    def handleDoingLock(self,
                     lockingAgent):
        return True