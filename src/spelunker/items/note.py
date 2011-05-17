from entity.item import Item

class Note(Item):
    def __init__(self,
                 name,
                 displayName=None,
                 description=None,
                 shortDescription=None,
                 inventory=None,
                 aliases=None,
                 isGettable=True,
                 text=None,
                 displayAutomatically=True):
        Item.__init__(self,
                      name=name,
                      displayName=displayName,
                      description=description,
                      shortDescription=shortDescription,
                      inventory=inventory,
                      aliases=aliases,
                      isGettable=isGettable,
                      displayAutomatically=displayAutomatically)
        self.text = text
        
    def read(self):
        if self.text is None:
            Item.read(self)
        else:
            self.speak(self.text)
            
    def handleDestroy(self):
        self.removeFromOwner()
        
    def handleReceivingCut(self,
                           cuttingAgent,
                           itemBeingUsed):
        self.removeFromOwner()
        
    def handleTear(self,
                   tearingAgent):
        self.removeFromOwner()