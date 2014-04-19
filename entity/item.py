from entity.gameEntity import GameEntity
from text_adventure.exception import CannotPerformAction

class Item(GameEntity):
    registry = dict()
    
    def __init__(self,
                 name,
                 displayName=None,
                 description=None,
                 shortDescription=None,
                 inventory=None,
                 aliases=None,
                 isGettable=False,
                 displayAutomatically=True):
        GameEntity.__init__(self,
                            name=name,
                            description=description,
                            shortDescription=shortDescription,
                            inventory=inventory,
                            aliases=aliases,
                            isGettable=isGettable,
                            displayAutomatically=displayAutomatically)
        self.__class__.registry[name] = self
        self.displayName = displayName
        if displayName is not None:
            self.names.append(displayName.lower())
        
    @classmethod
    def getItem(cls,
                key):
        return cls.registry.get(key)
    
    @classmethod
    def getKeys(cls):
        return cls.registry.keys()
    
    @classmethod
    def getNames(cls):
        names = []
        for (key, element) in cls.registry.items():
            names.extend(element.names)
        return names

    

    def getDescription(self,
                       isLooking=False):
        description = GameEntity.getDescription(self,
                                                isLooking=isLooking)
        for slotKey in self.inventory.slots.keys():
            inventoryDescription = self.getDescriptionOfContents(
                                          inventory=self.inventory,
                                          slotKey=slotKey)
            if inventoryDescription is not None:
                description = '%s\n%s' % (description,
                                          inventoryDescription)
        if self.attachedTo:
            description = '%s  Attached to %s is %s' %\
                                    (description,
                                     self.getDisplayNameWithDefiniteArticle(),
                                     self.getListOfAttachedEntities())
            
        return description

    def getShortDescription(self,
                            isLooking=False):   
        if self.shortDescription is not None:
            return self.shortDescription
        elif self.displayName is not None:
            return 'There is a %s here' % self.getDisplayName()
        else:
            return None
        
    def handleReceivePlacement(self,
                               placingAgent,
                               itemBeingPlaced,
                               whichSlot=None):
        if whichSlot is None:
            whichSlot = self.determineDefaultSlot()
        slot = self.inventory.slots.get(whichSlot)
        if slot is not None and slot.exposed:
            self.placeItemInSelf(itemBeingPlaced,
                                 whichSlot=whichSlot)
        else:
            raise CannotPerformAction('Entity does not support placement in that slot')
    
    def throw(self,
              entityToThrowAt):
        print 'The %s sails through the air toward its target.' % self.displayName
        entityToThrowAt.itemThrown(self)
    
