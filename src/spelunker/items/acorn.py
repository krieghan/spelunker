from entity.item import Item

class Acorn(Item):
    def __init__(self,
                 name,
                 description=''):
        Item.__init__(self,
                      name=name,
                      description=description,
                      displayName='acorn',
                      displayAutomatically=True,
                      isGettable=True)
        
