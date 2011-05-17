from entity.item import Item
from entity.room import Room

class Pond(Item):
    def __init__(self,
                 name,
                 description=''):
        Item.__init__(self,
                      name=name,
                      description=description,
                      displayName='pond',
                      aliases=['pond',
                               'lake',
                               'water'],
                      displayAutomatically=True)
        
    def handleReceiveThrowIn(self,
                             throwingAgent,
                             itemBeingThrown):
        self.handleReceiveThrow(throwingAgent,
                                itemBeingThrown)
        
    def handleReceiveThrownAt(self,
                              throwingAgent,
                              itemBeingThrown):
        self.handleReceiveThrow(throwingAgent,
                                itemBeingThrown)
        
    def handleReceiveThrow(self,
                           throwingAgent,
                           itemBeingThrown):
        inPondRoom = Room.getRoom('In the Pond')
        itemBeingThrown.changeOwner(inPondRoom)
        print 'The %s hits the surface of the pond and disappears underneath the surface.' %\
            itemBeingThrown.getDisplayNameWithDefiniteArticle()
            
    def handleSwim(self,
                   swimmingAgent):
        inPondRoom = Room.getRoom('In the Pond')
        swimmingAgent.changeOwner(inPondRoom)
        print inPondRoom.getDescription()
        
    def handleReceivingDip(self,
                           dippingAgent,
                           entityToDip):
        print ('You dip %s into %s.  You are rewarded with a wet %s' %
               (entityToDip.getDisplayNameWithDefiniteArticle(),
                self.getDisplayNameWithDefiniteArticle(),
                entityToDip.getDisplayName()))
