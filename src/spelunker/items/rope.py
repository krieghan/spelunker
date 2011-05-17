from entity.item import Item

class Rope(Item):
    
    def __init__(self,
                 name):
        Item.__init__(self,
                      name=name,
                      displayName='rope',
                      description='There is a rope here.  It frays in a few places, but is generally sturdy.',
                      aliases=['rope'],
                      isGettable=True)
    
    def canAttach(self):
        return True