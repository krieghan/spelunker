from entity.item import Item

class Pencil(Item):
    
    def __init__(self, 
                 name):
        Item.__init__(self,
                      name,
                      displayAutomatically=True,
                      isGettable=True,
                      displayName='pencil',
                      aliases=['pencil'])
        self.text = ''
    
    def handleDoingWrite(self,
                         writingAgent):
        return True