from entity.item import Item
from text_adventure.inventory import InventoryManager
class Rock(Item):
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
            inventory = InventoryManager(on=False,
                                         inside=False,
                                         under=False)
        Item.__init__(self,
                      name=name,
                      displayName=displayName,
                      description=description,
                      shortDescription=shortDescription,
                      inventory=inventory,
                      aliases=aliases,
                      isGettable=isGettable,
                      displayAutomatically=displayAutomatically)
        
