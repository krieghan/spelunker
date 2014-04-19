from entity.item import Item
from text_adventure.stateMachine.state import State
from text_adventure.stateMachine.stateMachine import StateMachine
from text_adventure.exception import CannotPerformAction
from text_adventure.inventory import InventoryManager

class Tree(Item):
    def __init__(self,
                 name,
                 description='',
                 inventory=None):
        if inventory is None:
            inventory = InventoryManager(on=False,
                                         inside=True,
                                         under=False)
            inventory.slots['inside'].exposed = False
        Item.__init__(self,
                      name=name,
                      description=description,
                      inventory=inventory,
                      displayName='tree',
                      displayAutomatically=True)
        
        self.stateMachine = StateMachine(owner=self,
                                         startingState=acornStillInTree)
        
    def handlePositioning(self,
                          positioningAgent,
                          whereToPosition):
        if whereToPosition == 'on':
            Item.handlePositioning(self,
                                   positioningAgent,
                                   whereToPosition)
        else:
            self.stateMachine.currentState.handleGoingUnder(
                    owner=self,
                    positioningAgent=positioningAgent)

        
class AcornStillInTree(State):
    def handleGoingUnder(self,
                         owner,
                         positioningAgent):
        acorn = owner.inventory.slots['inside']['Acorn']
        acorn.changeOwner(newOwner=positioningAgent,
                          fromSlot='inside',
                          toSlot='inside')
        owner.stateMachine.changeState(acornHasFallen)
        
        print 'You walk under the tree.  An acorn falls out of the tree and hits you on the head.  You pocket it.'
        
        
class AcornHasFallen(State):
    def handleGoingUnder(self,
                         owner,
                         positioningAgent):
        print 'You cover your head, expecting another acorn attack.  Fortunately, the tree seems to be short on supply.'

acornStillInTree = AcornStillInTree()
acornHasFallen = AcornHasFallen()

