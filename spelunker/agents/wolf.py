from entity.animal import Animal
from entity.item import Item
from text_adventure.exception import PlayerDeath, CannotPerformAction
from text_adventure.stateMachine.state import State
from text_adventure.stateMachine.stateMachine import StateMachine

class Wolf(Animal):
    
    def __init__(self,
                 name):
        Animal.__init__(self,
                       name=name)
        self.stateMachine = StateMachine(owner=self,
                                         startingState=wolfAliveState)
    
    def handleReceiveThrowAt(self,
                           throwingAgent,
                           itemBeingThrown):
        return self.stateMachine.currentState.handleReceiveThrowAt(
                                        throwingAgent=throwingAgent,
                                        itemBeingThrown=itemBeingThrown,
                                        receivingEntity=self)
        
    def handleDestroy(self,
                      destroyingAgent,
                      itemToUse):
        return self.handleStrike(strikingAgent=destroyingAgent,
                                 entityToStrikeWith=itemToUse)
        
    def handleStrike(self,
                     strikingAgent,
                     entityToStrikeWith):
        return self.stateMachine.currentState.handleStrike(
                                                strikingAgent=strikingAgent,
                                                entityToStrikeWith=entityToStrikeWith)
        
    def getLongDescription(self,
                           isLooking=False):
        return self.stateMachine.currentState.getLongDescription(self)
        
    def getDisplayName(self):
        return self.stateMachine.currentState.getDisplayName(self)

    def handleReceiveHug(self,
                         huggingAgent):
        return self.stateMachine.currentState.handleReceiveHug(
                                               huggingAgent=huggingAgent)
        
    def handleReceiveSearch(self,
                            searchingAgent,
                            entityToSearchWith=None):
        return self.stateMachine.currentState.handleReceiveSearch(
                                    searchingAgent=searchingAgent,
                                    entityToSearchWith=entityToSearchWith,
                                    entityToSearch=self)
        
class WolfAliveState(State):
    def handleReceiveThrowAt(self,
                           throwingAgent,
                           itemBeingThrown,
                           receivingEntity):
        if itemBeingThrown == Item.getItem('Dagger'):
            print ('The dagger pierces the wolf in the throat.  It lets out '
                   'a blood-chilling whine and collapses on the ground.')
            itemBeingThrown.changeOwner(newOwner=receivingEntity,
                                   toSlot='inside')
            receivingEntity.inventory.slots['inside'].exposed = True
            receivingEntity.stateMachine.changeState(wolfDeadState)
            receivingEntity.names.append('body')
            
        else:
            print ('The %s hits the wolf squarely in the jaw.  The wolf lunges at you, '
                  'tearing out your throat as you go down.' %\
                    itemBeingThrown.getDisplayName())
            raise PlayerDeath()
        
    def getLongDescription(self,
                           owner):
        return 'There is a wolf here.  It growls menacingly at your approach.'
    
    def getDisplayName(self,
                       owner):
        return 'wolf'
    
    def verifyCanBeRetrieved(self,
                             player=None):
        raise CannotPerformAction('The wolf snarls at you menacingly.  You do not want to provoke him.')
       
        
    def handleStrike(self,
                     strikingAgent,
                     entityToStrikeWith):
        if entityToStrikeWith is None:
            raise CannotPerformAction("Yeah.  You really stand a change at destroying the wolf with your bare hands.  That's it")
        if entityToStrikeWith.getName() in ['dagger']:
            raise CannotPerformAction('You grip the dagger in preparation of hand-to-hand combat with the wolf.  It snarls menacingly and readies itself to spring.  You pocket the dagger quickly.')
    
    
    
    def handleReceiveHug(self,
                         huggingAgent):
        print ("I like hugging aggressive, rabid wolves too.  Except that I don't.  "
               "And whenever I've tried to hug them, they've always attacked me visciously "
               "and torn my throat out.  Like this one is doing to you...")
        raise PlayerDeath()
    
    def handleReceiveSearch(self,
                            searchingAgent,
                            entityToSearchWith,
                            entityToSearch):
        raise CannotPerformAction('The wolf is not going to let you search it.')
    
class WolfDeadState(State):
    def handleReceiveThrow(self,
                           throwingAgent,
                           itemBeingThrown,
                           receivingEntity):
        Animal.handleReceiveThrowAt(receivingEntity,
                                    itemBeingThrown=itemBeingThrown)


    def getLongDescription(self,
                           owner):
        return ('There is a dead wolf here.  The still body contrasts '
                'sharply with the aggressiveness the wolf had in life.  ')
        
    def getDisplayName(self,
                       owner):
        return 'dead wolf'
    
    def verifyCanBeRetrieved(self,
                             player=None):
        return True
    
    def handleStrike(self,
                     strikingAgent,
                     entityToStrikeWith):
        raise CannotPerformAction('The wolf is already dead.  You see no reason to mutilate the corpse.')

    def handleReceiveHug(self,
                         huggingAgent):
        print "So you go in for that whole necro thing?  Ick."
        
    def handleReceiveSearch(self,
                            searchingAgent,
                            entityToSearchWith,
                            entityToSearch):
        descriptionOfContents =\
            entityToSearch.getDescriptionOfContents(
                                inventory=entityToSearch.inventory,
                                slotKey='inside')
        if descriptionOfContents:
            print descriptionOfContents
        else:
            print 'You find nothing'
            return
        for item in entityToSearch.inventory.slots['inside'].values():
            item.changeOwner(searchingAgent)
            print 'You get %s' % item.getDisplayNameWithDefiniteArticle()
        
        

wolfAliveState = WolfAliveState()
wolfDeadState = WolfDeadState()
