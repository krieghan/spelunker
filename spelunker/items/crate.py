from entity.item import Item

class Crate(Item):
    
    def __init__(self,
                 name,
                 description=''):
        Item.__init__(self,
                      name=name,
                      displayName='crate',
                      description=description)
    
    def handleDoingBlock(self,
                         blockingAgent):
        return True