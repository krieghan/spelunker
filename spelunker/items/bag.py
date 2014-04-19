from entity.item import Item
from text_adventure.inventory import InventoryManager
from text_adventure.exception import CannotPerformAction
class Bag(Item):
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
                                         inside=True,
                                         under=False)
            inventory.slots['inside'].exposed = False
        Item.__init__(self,
                      name=name,
                      displayName=displayName,
                      description=description,
                      shortDescription=shortDescription,
                      inventory=inventory,
                      aliases=aliases,
                      isGettable=isGettable,
                      displayAutomatically=displayAutomatically)
        
        self.open = False
        
    def handleDestroy(self,
                      destroyingAgent=None,
                      itemToUse=None):
        if itemToUse.getName() in ['dagger']:
            self.removeFromOwner()
            return True
        else:
            raise CannotPerformAction('You cannot destroy %s with %s' %\
                                      (self.getDisplayNameWithDefiniteArticle(),
                                       itemToUse.getDisplayNameWithDefiniteArticle()))
            
    def handleOpen(self,
                   openingAgent):
        if self.open == True:
            raise CannotPerformAction('%s is already open' % 
                                      self.getDisplayNameWithDefiniteArticle())
        self.open = True
        self.inventory.slots['inside'].exposed = True
        print ('You open %s' % self.getDisplayNameWithDefiniteArticle())
        descriptionOfContents = self.getDescriptionOfContents(
                                            inventory=self.inventory,
                                            slotKey='inside')
        if descriptionOfContents is not None:
            print descriptionOfContents
            
    def handleClose(self,
                    closingAgent):
        if self.open == False:
            raise CannotPerformAction('%s is already closed' %
                                      self.getDisplayNameWithDefiniteArticle())
        self.open = False
        self.inventory.slots['inside'].exposed = False
        print ('You close %s' % self.getDisplayNameWithDefiniteArticle())
