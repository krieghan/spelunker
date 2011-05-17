from inventory import InventoryManager, Inventory
from exception import (CannotPerformAction,
                       ItemNotFound)

class GameEntity(object):
    def __init__(self,
                 name,
                 description=None,
                 shortDescription=None,
                 inventory=None,
                 aliases=None,
                 isGettable=False,
                 exposeInventory=True,
                 displayAutomatically=False,
                 recurseAutomatically=True,
                 displayName=None,
                 attachedTo=None):
        if inventory is None:
            inventory = InventoryManager()
        if aliases is None:
            aliases = []
        if attachedTo is None:
            attachedTo = []
        self.inventory = inventory
        self.name = name
        self.names = [x.lower() for x in aliases] + [name.lower()]
        self.description = description
        self.shortDescription = shortDescription
        self.isGettable = isGettable
        self.hasBeenSeen = False
        self.currentOwner = None
        self.exposeInventory = exposeInventory
        self.displayAutomatically = displayAutomatically
        self.displayName = displayName
        self.recurseAutomatically = recurseAutomatically
        self.attachedTo = attachedTo
        objectivePronoun = self.getObjectivePronoun()
        if objectivePronoun:
            self.names.append(objectivePronoun)
        
    def addEntity(self,
                  entity,
                  whichSlot=None):
        if whichSlot is None:
            whichSlot = self.determineDefaultSlot()
        self.inventory.slots[whichSlot][entity.name] = entity
        entity.currentOwner = self
        
    def removeEntity(self,
                     entity,
                     whichSlot=None):
        if whichSlot is None:
            whichSlot = self.determineWhichSlot(entity) 
        del self.inventory.slots[whichSlot][entity.name]
        entity.currentOwner = None
        
    
    def changeOwner(self,
                    newOwner,
                    fromSlot=None,
                    toSlot=None):
        if self.currentOwner:
            self.currentOwner.removeEntity(
                   self,
                   whichSlot=fromSlot)
        newOwner.addEntity(self,
                           whichSlot=toSlot)
        
    def removeFromOwner(self,
                        fromSlot=None):
        if self.currentOwner:
            self.placeAllItemsInOwner()
            self.currentOwner.removeEntity(
                    self,
                    whichSlot=fromSlot)

    def getDescription(self,
                       isLooking=False):    
        if isLooking:
            description = self.getLongDescription(isLooking=isLooking)
        elif self.hasBeenSeen:
            description = self.getShortDescription(isLooking=isLooking)
        else:
            self.hasBeenSeen = True
            description = self.getLongDescription(isLooking=isLooking)
        return description
    
    def getShortDescription(self,
                            isLooking=False):
        if self.shortDescription:
            return self.shortDescription
        else:
            return ''
    
    def getLongDescription(self,
                           isLooking=False):
        description = self.description or ''
        return description
    
    def getDescriptionOfContents(self,
                                 inventory,
                                 slotKey):
        inventoryDescription = None
        slot = inventory.slots[slotKey]
        preposition = slotKey[0].upper() + slotKey[1:]
        elementsToDisplay = []
        if slot.exposed:
            for entity in slot.values():
                if entity.displayName is not None:
                    elementsToDisplay.append(entity.getDisplayName())
            
        if elementsToDisplay:
            inventoryDescription = ', '.join(elementsToDisplay)
            inventoryDescription = '%s the %s is %s.' % (preposition,
                                                        self.getDisplayName(),
                                                        inventoryDescription)
        return inventoryDescription
    
    def getDisplayName(self):
        return self.displayName
    
    def getPersonalPronoun(self):
        return None
    
    def getObjectivePronoun(self):
        return None
    
    def getName(self):
        return self.displayName
   
    def read(self):
        raise CannotPerformAction('You cannot read the %s.' % self.name)
    
    def determineWhichSlot(self,
                           entity):
        whichSlot = None
        for (slotKey, slot) in self.inventory.slots.items():
            if entity in slot.values():
                whichSlot = slotKey
                break
        if whichSlot is None:
            raise ItemNotFound('%s does not have %s in any slot' %\
                               (self.name,
                                entity.name))
        
        return whichSlot
    
    def determineDefaultSlot(self):
        return self.inventory.slots.keys()[0]
    
    def placeItemInSelf(self,
                        item,
                        whichSlot=None):
        if whichSlot is None:
            whichSlot = self.determineDefaultSlot()
        if whichSlot not in self.inventory.slots.keys():
            raise CannotPerformAction('You cannot place the %s %s the %s' %\
                                      (item.name, 
                                       whichSlot,
                                       self.name))
            
        item.changeOwner(newOwner=self,
                         toSlot=whichSlot)

    def placeAllItemsInOwner(self,
                             whichSlot=None):
        newOwner = self.currentOwner
        if whichSlot is None:
            whichSlot = newOwner.determineDefaultSlot()
        
        for (slotKey, slot) in self.inventory.slots.items():
            for item in slot.values():
                item.changeOwner(newOwner=newOwner,
                                 fromSlot=slotKey,
                                 toSlot=whichSlot)
                    
        
    def verifyCanBeRetrieved(self,
                             retrievingParty=None):
        if self.currentOwner:
            return self.currentOwner.verifyCanBeRetrieved(
                                        retrievingParty=retrievingParty)
        else:
            return True
        
    def handleBeingThrown(self,
                          throwingAgent):
        pass
        
    def handleReceiveThrowAt(self,
                             throwingAgent,
                             itemBeingThrown):
        print 'The %s harmlessly bounces off the %s and lands on the ground' %\
            (itemBeingThrown.displayName,
             self.getDisplayName())
        itemBeingThrown.changeOwner(newOwner=self.currentOwner,
                                    toSlot='inside')
        
    def handleReceiveThrowIn(self,
                             throwingAgent,
                             itemBeingThrown):
        if 'inside' in self.inventory.slots.keys():
            inside = self.inventory.slots['inside']
            itemBeingThrown.changeOwner(newOwner=self,
                                        toSlot='inside')
            print ('Nice shot! %s lands inside %s.' % 
                   (itemBeingThrown.getDisplayNameWithDefiniteArticle(),
                    self.getDisplayNameWithDefiniteArticle()))
        else:
            raise CannotPerformAction('You cannot throw the %s in the %s')
        
    def handleReceivePlacement(self,
                               placingAgent,
                               itemBeingPlaced,
                               whichSlot=None):
        if whichSlot is None:
            whichSlot = self.determineDefaultSlot()
        raise CannotPerformAction('Entity does not support placement')
       
    def handleEat(self):
        raise CannotPerformAction('You cannot eat the %s' % self.getDisplayName())
    
    def handleDestroy(self,
                      destroyingAgent=None,
                      itemToUse=None):
        raise CannotPerformAction('You cannot destroy %s' % self.getDisplayNameWithDefiniteArticle())
    
    def handleDoingCut(self,
                       cuttingAgent):
        raise CannotPerformAction('The %s is not sharp enough to cut anything.' % self.getDisplayName())
    
    def handleReceivingCut(self,
                           cuttingAgent,
                           itemBeingUsed):
        raise CannotPerformAction('You cannot cut the %s' % self.getDisplayName())
    
    def getDisplayNameWithDefiniteArticle(self):
        return 'the %s' % self.getDisplayName()
    
    def getDisplayNameWithIndefiniteArticle(self):
        name = self.getDisplayName()
        if name[0] in ['a', 'e', 'i', 'o', 'u']:
            article = 'an'
        else:
            article = 'a'
        return '%s %s' % (article, name)
    
    def getDisplayNamePlural(self):
        name = self.getDisplayName()
        return '%s%s' % (name, 's')
    
    def getPersonalPronoun(self):
        return 'it'
        
    def handleTalk(self,
                   talkingAgent,
                   subjectOfConversation=None):
        raise CannotPerformAction('Talking to %s would be like talking to a brick wall' % self.getDisplayNameWithDefiniteArticle())
    
    def handleAsk(self,
                  askingAgent,
                  subjectOfConversation=None):
        raise CannotPerformAction("There's no reason to believe that %s would know anything about %s" %\
                                  (self.getDisplayNameWithDefiniteArticle(),
                                   subjectOfConversation))
    
    def handleDoingWrite(self,
                         writingAgent=None):
        raise CannotPerformAction("You can't write with %s" % self.getDisplayNameWithDefiniteArticle())
    
    def handleReceivingWriting(self,
                    writingAgent,
                    itemToWriteWith):
        raise CannotPerformAction("%s doesn't have a good enough writing surface" % self.getDisplayNameWithDefiniteArticle())
    
    def handlePositioning(self,
                          positioningAgent,
                          whereToPosition):
        raise CannotPerformAction("You can't go %s %s" % (whereToPosition,
                                                          self.getDisplayNameWithDefiniteArticle()))
    
    def handleSwim(self,
                   swimmingAgent):
        raise CannotPerformAction("You cannot swim in %s" % self.getDisplayNameWithDefiniteArticle())

    def handleReceiveKiss(self,
                          kissingAgent):
        print 'You kiss %s.  Congratulations, your lips now taste like %s' %\
            (self.getDisplayNameWithDefiniteArticle(),
             self.getDisplayName())
    
    def handleListening(self,
                        listeningAgent):
        print 'You spend a few moments listening to %s, but determine that it is mute' %\
            (self.getDisplayNameWithDefiniteArticle())
            
    def handleTasting(self,
                      tastingAgent):
        print 'It tastes alot like %s' % self.getDisplayNameWithIndefiniteArticle()
    
    def handleSmelling(self,
                       smellingAgent):
        print "You sniff at %s a bit, but it isn't giving off much of an odor." %\
            self.getDisplayNameWithDefiniteArticle()
            
    def handleFeeling(self,
                      feelingAgent):
        print 'You run your fingers over %s, but conclude that it feels an awful lot like %s' %\
                (self.getDisplayNameWithDefiniteArticle(),
                 self.getDisplayNameWithIndefiniteArticle())
                
    def handleReceiveHug(self,
                         huggingAgent):
        print ("I like to hug %s too, but they don't hug back." %
               (self.getDisplayNamePlural()))
    
    def getListOfAttachedEntities(self):
        return ' and '.join([x.getDisplayNameWithDefiniteArticle() 
                             for x in self.attachedTo]) 
            
    
    def handleDoingAttach(self,
                          entityToAttach,
                          entityToAttachTo=None):
        if entityToAttachTo is not None:
            entitiesToAttach = [entityToAttach,
                                entityToAttachTo]
        else:
            entitiesToAttach = [entityToAttach]

        if self.canAttach():
            if len(self.attachedTo) + len(entitiesToAttach) > 2:
                raise CannotPerformAction(
                          '%s is already attached to %s'
                          % (self.getDisplayNameWithDefiniteArticle(),
                             self.getListOfAttachedEntities()))
            else:
                for entity in entitiesToAttach:
                    entity.handleBeingAttached(entityToAttachWith=self)
                    self.attachedTo.append(entity)
                    print ('You attach %s to %s'
                           % (self.getDisplayNameWithDefiniteArticle(),
                              entity.getDisplayNameWithDefiniteArticle()))
        else:
            if entityToAttachTo is not None:
                raise CannotPerformAction('You cannot attach %s to %s with %s'
                                          % (entityToAttach.getDisplayNameWithDefiniteArticle(),
                                             entityToAttachTo.getDisplayNameWithDefiniteArticle(),
                                             self.getDisplayNameWithDefiniteArticle()))
            else:
                raise CannotPerformAction('You cannot attach %s to %s'
                                          % (entityToAttach.getDisplayNameWithDefiniteArticle(),
                                             self.getDisplayNameWithDefiniteArticle()))
        
    def handleBeingAttached(self,
                            entityToAttachWith):
        if len(self.attachedTo) > 0:
            attachedTo = self.attachedTo[0]
            raise CannotPerformAction('%s is already attached to %s'
                                      % (self.getDisplayNameWithDefiniteArticle(),
                                         attachedTo.getDisplayNameWithDefiniteArticle()))
        self.attachedTo.append(entityToAttachWith)
    
    def handleTear(self,
                   tearingAgent):
        raise CannotPerformAction('%s has a tough texture.  %s cannot be torn.' %
                                  (self.getDisplayNameWithDefiniteArticle(),
                                   self.getPersonalPronoun()))
    
    def handleStrike(self,
                     strikingAgent,
                     entityToStrikeWith=None):
        if entityToStrikeWith is None:
            print ('You strike %s with your bare hands.  You succeed in hurting your hands.' %
                   self.getDisplayNameWithDefiniteArticle())
        else:
            print ('You strike %s with %s' % 
                   (self.getDisplayNameWithDefiniteArticle(),
                    entityToStrikeWith.getDisplayNameWithDefiniteArticle()))
            
    def handleOpen(self,
                   openingAgent):
        raise CannotPerformAction('You see no obvious way to open %s'
                                  % self.getDisplayNameWithDefiniteArticle())
        
    def handleClose(self,
                    closingAgent):
        raise CannotPerformAction('%s cannot be opened, and thus it cannot be closed.'
                                  % self.getDisplayNameWithDefiniteArticle())
            
    def handleTravelTo(self,
                       travelingAgent):
        raise CannotPerformAction('You cannot travel to %s' % 
                                  (self.getDisplayNameWithDefiniteArticle()))
            
    def handleDoingLock(self,
                        lockingAgent):
        raise CannotPerformAction('%s cannot lock anything' % 
                                  self.getDisplayNameWithDefiniteArticle())
    
    def handleReceivingLock(self,
                            lockingAgent,
                            entityToLockWith):
        raise CannotPerformAction('%s cannot be locked' %
                                  self.getDisplayNameWithDefiniteArticle())
    
    def handleDoingUnlock(self,
                          unlockingAgent):
        raise CannotPerformAction('%s cannot unlock anything' %
                                  self.getDisplayNameWithDefiniteArticle())
    
    def handleReceivingUnlock(self,
                              unlockingAgent,
                              entityToUnlockWith):
        raise CannotPerformAction('%s cannot be unlocked' %
                                  self.getDisplayNameWithDefiniteArticle())
        
    def handleDoingBlock(self,
                         blockingAgent):
        raise CannotPerformAction('%s cannot be used for blocking.' %
                                  self.getDisplayNameWithDefiniteArticle())
        
    def handleReceivingBlock(self,
                             blockingAgent,
                             entityToBlockWith=None):
        if entityToBlockWith is None:
            raise CannotPerformAction(
                      "It doesn't really make much sense to " 
                      "block %s with your body" %
                      self.getDisplayNameWithDefiniteArticle())
        raise CannotPerformAction(
                      '%s is not sufficient to block %s' %
                      (entityToBlockWith.getDisplayNameWithDefiniteArticle(),
                      self.getDisplayNameWithDefiniteArticle()))
        
    def handleReceivingUnblock(self,
                               blockingAgent):
        raise CannotPerformAction('%s is not blocked' %
                                  self.getDisplayNameWithDefiniteArticle())
    
    def handleReceivingDip(self,
                           dippingAgent,
                           entityToDip):
        raise CannotPerformAction('You cannot dip anything into %s' % 
                                  self.getDisplayNameWithIndefiniteArticle())
        
    def handleReceiveGive(self,
                          givingAgent,
                          entityToGive):
        raise CannotPerformAction('%s has no need for such earthly possessions.' % 
                                  self.getDisplayNameWithDefiniteArticle())
    
    def handleReceiveSearch(self,
                            searchingAgent,
                            entityToSearchWith=None):
        print 'You studiously search %s' % self.getDisplayNameWithDefiniteArticle()
        self.handleReceiveLook(lookingAgent=searchingAgent,
                               relation='in')
    
    def handleReceiveLook(self,
                          lookingAgent,
                          relation='at'):
        print self.getDescription(isLooking=True)
        
    def handleReceiveClimb(self,
                           climbingAgent):
        raise CannotPerformAction("Why?  Because it's there?")
    
    def canAttach(self):
        return False
    
    def speak(self,
              speech):
        print '%s: %s' % (self.getDisplayName(),
                          speech)
        