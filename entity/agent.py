from entity.room import Room
from entity.gameEntity import GameEntity
from text_adventure.exception import CannotPerformAction
from text_adventure.inventory import InventoryManager


class Agent(GameEntity):
    registry = dict()
    
    def __init__(self,
                 name,
                 description=None,
                 inventory=None,
                 aliases=None,
                 exposeInventory=False,
                 displayAutomatically=True,
                 shortDescription=None,
                 displayName=None,
                 recurseAutomatically=True):
        if inventory is None:
            inventory = InventoryManager(on=False,
                                         under=False,
                                         inside=True)
            inventory.slots['inside'].exposed = False
            
        GameEntity.__init__(self,
                            name=name,
                            description=description,
                            inventory=inventory,
                            aliases=aliases,
                            exposeInventory=exposeInventory,
                            displayAutomatically=displayAutomatically,
                            shortDescription=shortDescription,
                            displayName=displayName,
                            recurseAutomatically=recurseAutomatically)
        self.__class__.registry[name] = self
    
    @classmethod
    def getAgent(cls,
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
    
    def get(self,
            entityNames,
            entities):
        entityName = entityNames['main']
        entityToGet = entities['main']
        if self.inventory.match(entityName):
            raise CannotPerformAction('You already have the {}'.format(entityName))
        if not entityToGet.isGettable:
            raise CannotPerformAction('You cannot get the %s.' % entityToGet.name)
        else:
            entityToGet.verifyCanBeRetrieved(retrievingParty=self)
            entityToGet.changeOwner(self)
            print 'You get the %s' % entityToGet.name
            
    def drop(self,
             entity):
        slot = self.inventory.slots['inside']
        if entity not in slot.values():
            raise CannotPerformAction("You don't have the %s" % entity.name)
        else:
            print 'You drop the %s' % entity.name
            entity.changeOwner(self.currentOwner)
    
    def getDescriptionOfPossessions(self):
        slot = self.inventory.slots['inside']
        if not slot.exposed:
            return ''
        entities = [x.displayName for x in slot.values()]
        if not entities:
            return ''
        else:
            description = ', '.join(entities)
        description = 'The %s has: %s.' % (self.getDisplayName(), description)
        return description
            
    def getDescription(self,
                       isLooking=False):
        description = self.getLongDescription(isLooking=isLooking)
        description += self.getDescriptionOfPossessions()
        if self.attachedTo:
            description += '  %s is attached to %s' %\
                           (self.getDisplayNameWithDefiniteArticle(),
                            self.getListOfAttachedEntities())
        return description
    
    def eat(self,
            entity):
        entity.handleEat()
        print 'You eat the %s' % entity.getDisplayName()
        
    def destroy(self,
                entityToDestroy,
                itemToUse=None):
        entityToDestroy.handleDestroy(destroyingAgent=self,
                                      itemToUse=itemToUse)
        if itemToUse is not None:
            print 'You destroy the %s with the %s' %\
                (entityToDestroy.getDisplayName(),
                 itemToUse.getDisplayName())
        else:
            print 'You destroy the %s' % entityToDestroy.getDisplayName()
        
    def cut(self,
            entityBeingCut,
            itemBeingUsed):
        itemBeingUsed.handleDoingCut(cuttingAgent=self)
        entityBeingCut.handleReceivingCut(cuttingAgent=self,
                                          itemBeingUsed=itemBeingUsed)
        print 'You cut the %s with the %s' % (entityBeingCut.getDisplayName(),
                                              itemBeingUsed.getDisplayName())

    def throw(self,
              itemBeingThrown,
              receivingEntity,
              where='at'):
        itemBeingThrown.handleBeingThrown(throwingAgent=self)
        if where == 'at':
            receivingEntity.handleReceiveThrowAt(
                             throwingAgent=self,
                             itemBeingThrown=itemBeingThrown)
        elif where == 'in':
            receivingEntity.handleReceiveThrowIn(
                             throwingAgent=self,
                             itemBeingThrown=itemBeingThrown)
        else:
            raise CannotPerformAction('Where do you want to throw %s?' % itemBeingThrown.getDisplayNameWithDefiniteArticle())

    def handleReceiveThrowIn(self,
                             throwingAgent,
                             itemBeingThrown):
        raise CannotPerformAction(
                  'Throwing %s into %s makes no sense'
                  % (itemBeingThrown.getDisplayNameWithDefiniteArticle(),
                     self.getDisplayNameWithDefiniteArticle()))

    def place(self,
              objectToPlace,
              container,
              whichSlot=None):
        container.handleReceivePlacement(placingAgent=self,
                                         itemBeingPlaced=objectToPlace,
                                         whichSlot=whichSlot)
        
    def talk(self,
             entityToTalkTo,
             subjectOfConversation=None):
        entityToTalkTo.handleTalk(talkingAgent=self,
                                  subjectOfConversation=subjectOfConversation)
        
    def ask(self,
            entityToAsk,
            subjectOfConversation=None):
        entityToAsk.handleAsk(askingAgent=self,
                              subjectOfConversation=subjectOfConversation)
        
    def write(self,
              entityToWriteOn,
              itemToWriteWith):
        itemToWriteWith.handleDoingWrite(writingAgent=self)
        entityToWriteOn.handleReceivingWriting(writingAgent=self,
                                    itemToWriteWith=itemToWriteWith)
        
    def position(self,
                 entityWithWhichToPosition,
                 whereToPosition):
        entityWithWhichToPosition.handlePositioning(positioningAgent=self,
                                                    whereToPosition=whereToPosition)
    
    def swim(self,
             entityToSwimIn):
        entityToSwimIn.handleSwim(swimmingAgent=self)
        
    def kiss(self,
             entityToKiss):
        entityToKiss.handleReceiveKiss(kissingAgent=self)
        
    def handleReceiveKiss(self,
                          kissingAgent):
        print 'You kiss %s.  Needless to say, %s is quite surprised.' %\
         (self.getDisplayNameWithDefiniteArticle(),
          self.getDisplayNameWithDefiniteArticle())
    
    def getPossessivePronoun(self):
        return 'his'
         
    def listen(self,
               entityToListenTo):
        entityToListenTo.handleListening(listeningAgent=self)
    
    def handleListening(self,
                        listeningAgent):
        print ("%s breathes steadily.  After a few moments of concentration, " 
               "you can hear the beating of %s heart." % (self.getDisplayNameWithDefiniteArticle(),
                                                         self.getPossessivePronoun()))
        
    def taste(self,
              entityToTaste):
        entityToTaste.handleTasting(tastingAgent=self)
        
    def handleTasting(self,
                      tastingAgent):
        self.speak("You wouldn't like how I taste, really.  Too gamey.")
        
    def smell(self,
              entityToSmell):
        entityToSmell.handleSmelling(smellingAgent=self)
        
    def handleSmelling(self,
                       smellingAgent):
        print 'You sniff %s.  %s looks at you and shies away.' % (self.getDisplayName(),
                                                                  self.getDisplayName())
        
    def feel(self,
             entityToFeel):
        entityToFeel.handleFeeling(feelingAgent=self)
        
    
        
    def hug(self,
            entityToHug):
        entityToHug.handleReceiveHug(huggingAgent=self)
        
    def handleReceiveHug(self,
                         huggingAgent):
        print "I like to hug strangers too, but they just think I'm creepy."
        
    def attach(self,
               entityToAttach,
               entityToAttachTo,
               entityToAttachWith=None):
        
        if entityToAttachWith is None:
            if entityToAttach.canAttach():
                entityToAttachWith = entityToAttach
                entityToAttach = entityToAttachTo
            elif entityToAttachTo.canAttach():
                entityToAttachWith = entityToAttachTo
            else:
                raise CannotPerformAction("Neither %s nor %s are capable of attaching."
                                          % (entityToAttach.getDisplayNameWithDefiniteArticle(),
                                             entityToAttachTo.getDisplayNameWithDefiniteArticle())
                                          )
            entityToAttachTo = None
        
        if not entityToAttachWith.canAttach():
            raise CannotPerformAction('%s is not capable of attaching.'
                                      % entityToAttachWith.getDisplayNameWithDefiniteArticle())
            
        if (entityToAttach == entityToAttachTo or 
            entityToAttach == entityToAttachWith):
            raise CannotPerformAction('You cannot attach %s to itself!' %
                                      entityToAttach.getDisplayNameWithDefiniteArticle())
        entityToAttachWith.handleDoingAttach(entityToAttach=entityToAttach,
                                             entityToAttachTo=entityToAttachTo)
    
    def replace(self,
                entityToReplace,
                entityToReplaceWith):
        if not entityToReplace.isGettable:
            raise CannotPerformAction('You cannot get the %s.' % entityToReplace.name)
        
        entityToReplaceOwner = entityToReplace.currentOwner
        entityToReplaceSlot =\
            entityToReplaceOwner.determineWhichSlot(entityToReplace)
        entityToReplaceWithOwner = entityToReplaceWith.currentOwner
        entityToReplaceWithSlot = entityToReplaceWithOwner.determineWhichSlot(entityToReplaceWith)
        
        entityToReplace.changeOwner(newOwner=entityToReplaceWithOwner,
                                    fromSlot=entityToReplaceSlot,
                                    toSlot=entityToReplaceWithSlot)
        entityToReplaceWith.changeOwner(newOwner=entityToReplaceOwner,
                                        fromSlot=entityToReplaceWithSlot,
                                        toSlot=entityToReplaceSlot)
        
        print ('You replace %s with the %s' %
               (entityToReplace.getDisplayNameWithDefiniteArticle(),
                entityToReplaceWith.getDisplayNameWithDefiniteArticle()))
        
    def tear(self,
             entityToTear):
        entityToTear.handleTear(tearingAgent=self)
        print 'You tear %s' % entityToTear.getDisplayNameWithDefiniteArticle()
        
    def strike(self,
               entityToStrike,
               entityToStrikeWith=None):
        entityToStrike.handleStrike(strikingAgent=self,
                                    entityToStrikeWith=entityToStrikeWith)
        
    def handleStrike(self,
                     strikingAgent,
                     entityToStrikeWith):
        raise CannotPerformAction("You have no reason to strike %s" %
                                  self.getDisplayNameWithDefiniteArticle())
        
    def open(self,
             entityToOpen):
        entityToOpen.handleOpen(openingAgent=self)
        
    def close(self,
              entityToClose):
        entityToClose.handleClose(closingAgent=self)
        
    def travel(self,
               placeToTravel):
        placeToTravel.handleTravelTo(travellingAgent=self)
        
    def lock(self,
             entityToLock,
             entityToLockWith=None):
        if entityToLockWith is not None:
            entityToLockWith.handleDoingLock(lockingAgent=self)
        entityToLock.handleReceivingLock(lockingAgent=self,
                                         entityToLockWith=entityToLockWith)
        
    def unlock(self,
               entityToUnlock,
               entityToUnlockWith=None):
        if entityToUnlockWith is not None:
            entityToUnlockWith.handleDoingUnlock(unlockingAgent=self)
        entityToUnlock.handleReceivingUnlock(unlockingAgent=self,
                                             entityToUnlockWith=entityToUnlockWith)
        
    def block(self,
              entityToBlock,
              entityToBlockWith=None):
        if entityToBlockWith is not None:
            entityToBlockWith.handleDoingBlock(blockingAgent=self)
        entityToBlock.handleReceivingBlock(blockingAgent=self,
                                           entityToBlockWith=entityToBlockWith)
        
    def unblock(self,
                entityToUnblock):
        entityToUnblock.handleReceivingUnblock(unblockingAgent=self)
        
    def dip(self,
            entityToDip,
            entityToDipIn):
        entityToDipIn.handleReceivingDip(dippingAgent=self,
                                         entityToDip=entityToDip)
        
    def give(self,
             entityToGive,
             entityToGiveTo):
        entityToGiveTo.handleReceiveGive(givingAgent=self,
                                         entityToGive=entityToGive)
        
    def handleReceiveGive(self,
                          givingAgent,
                          entityToGive):
        raise CannotPerformAction('%s refuses your kind offer.' % 
                                  self.getDisplayNameWithDefiniteArticle())
        
    def search(self,
               entityToSearch,
               entityToSearchWith=None):
        entityToSearch.handleReceiveSearch(searchingAgent=self,
                                           entityToSearchWith=entityToSearchWith)
        
    def look(self,
             objects):
        entityToLookAt = objects.get('main', objects.get('at'))
        entityToLookAt.handleReceiveLook(lookingAgent=self,
                                         relation='at')
        
    def climb(self,
              entityToClimb):
        entityToClimb.handleReceiveClimb(climbingAgent=self)
