from entity.item import Item
from inventory import InventoryManager
class Table(Item):
    def __init__(self,
                 name,
                 displayName=None,
                 description=None,
                 shortDescription=None,
                 inventory=None,
                 aliases=None,
                 isGettable=False,
                 displayAutomatically=True):
        if inventory is None:
            inventory = InventoryManager(on=True,
                                         inside=False,
                                         under=True)
        Item.__init__(self,
                      name=name,
                      displayName=displayName,
                      description=description,
                      shortDescription=shortDescription,
                      inventory=inventory,
                      aliases=aliases,
                      isGettable=isGettable,
                      displayAutomatically=displayAutomatically)
        
        