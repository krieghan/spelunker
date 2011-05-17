from entity.gameEntity import GameEntity
from exception import (NotPresent, 
                       AmbiguousEntity, 
                       MissingObject,
                       CannotPerformAction)
from inventory import InventoryManager

class Room(GameEntity):
    
    registry = dict()
    obstructions = dict()
    
    def __init__(self,
                 name,
                 description,
                 inventory=None,
                 up=None,
                 down=None,
                 north=None,
                 south=None,
                 east=None,
                 west=None,
                 displayAutomatically=False):
        if inventory is None:
            inventory = InventoryManager(inside=True,
                                         on=False,
                                         under=False)
        self.name = name
        self.__class__.registry[name] = self
        self.description = description
        self.directions = dict()
        self.directions['up'] = up
        self.directions['down'] = down
        self.directions['north'] = north
        self.directions['south'] = south
        self.directions['east'] = east
        self.directions['west'] = west
        GameEntity.__init__(self,
                            name=name,
                            description=description,
                            inventory=inventory,
                            displayAutomatically=displayAutomatically)
    
    @classmethod
    def getRoom(cls, key):
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

    @classmethod
    def addObstruction(cls,
                       fromRoom,
                       toRoom,
                       obstruction):
        cls.obstructions['%s->%s' % (fromRoom, toRoom)] = obstruction
        
    @classmethod
    def removeObstruction(cls,
                          fromRoom,
                          toRoom):
        del cls.obstructions['%s->%s' % (fromRoom, toRoom)]
    
    @classmethod
    def getObstruction(cls,
                       fromRoom,
                       toRoom):
        return cls.obstructions.get('%s->%s' % (fromRoom, toRoom))
    
    def getDescription(self,
                       isLooking=False):
        description = GameEntity.getDescription(self,
                                                isLooking=isLooking)
        for slot in self.inventory.slots.values():
            for entity in slot.values():
                if not entity.displayAutomatically:
                    continue
                entityDescription = entity.getDescription(isLooking=isLooking)
                if entityDescription is not None:
                    if description:
                        description = '%s\n%s' % (description,
                                                  entityDescription)
                    else:
                        description = entityDescription
        return description
    
    def getLongDescription(self,
                           isLooking=False):
        return '%s\n%s' % (self.getShortDescription(isLooking=isLooking),
                           self.description)
    
    def getShortDescription(self,
                            isLooking=False):
        return self.name
    
    def getRoomInDirection(self, direction):
        roomName = self.directions[direction]
        if roomName is None:
            return None
        
        return self.__class__.getRoom(self.directions[direction])
    
    def match(self, 
              entityName,
              player,
              default='default'):
        matches = []
        matches.extend(player.inventory.match(entityName))
        matches.extend(self.inventory.match(entityName))
        if len(matches) == 0:
            if default != 'default':
                return default
            else:
                raise NotPresent('There is no %s here' % entityName)
        if len(matches) > 1:
            raise AmbiguousEntity(matches)
        if len(matches) == 1:
            match = matches[0]
            return match
        
    def matchToPlayerInventory(
                         self,
                         entityName,
                         player,
                         default='default'):
        matches = []
        matches.extend(player.inventory.match(entityName))
        if len(matches) == 0:
            if default != 'default':
                return default
            else:
                raise NotPresent('You do not have the %s' % 
                                 entityName)
        if len(matches) > 1:
            raise AmbiguousEntity(matches)
        if len(matches) == 1:
            match = matches[0]
            return match
        
    def matchToRoom(self,
                    entityName,
                    default='default'):
        matches = []
        matches.extend(self.inventory.match(entityName))
        if len(matches) == 0:
            if default != 'default':
                return default
            else:
                raise NotPresent('There is no %s here' % entityName)
        if len(matches) > 1:
            raise AmbiguousEntity(matches)
        if len(matches) == 1:
            match = matches[0]
        return match
            
    def actOnAction(self, 
                    action,
                    player):
        verb = action.verb
        if action.isGetting():
            entityName = action.object
            indirectObjectName = action.indirectObject
            if indirectObjectName is None:
                indirectObject = None
                containingInventory = self.inventory
                notPresentException = NotPresent('There is no %s here' % entityName)
            else:
                indirectObject = self.matchToRoom(entityName=indirectObjectName,
                                                  default=None)
                containingInventory = indirectObject.inventory
                notPresentException =\
                    NotPresent('%s has no %s' % 
                               (indirectObject.getDisplayNameWithDefiniteArticle(),
                                entityName))
            if entityName is None:
                raise MissingObject('What do you want to get?')
            matches = []
            matches.extend(containingInventory.match(entityName))
            if len(matches) == 1:
                match = matches[0]
                player.get(entityToGet=match)
                return True
            elif len(matches) == 0:
                matches.extend(player.inventory.match(entityName))
                if len(matches) == 1:
                    match = matches[0]
                    raise CannotPerformAction('You already have the %s' % match.name)
            if len(matches) > 1:
                raise AmbiguousEntity(matches)
            
            raise notPresentException
        if action.isDropping():
            entityName = action.object
            if entityName is None:
                raise MissingObject('What do you want to drop?')
            matches = []
            matches.extend(player.inventory.match(entityName))
            if len(matches) == 1:
                match = matches[0]
                player.drop(match)
                return True
            elif len(matches) == 0:
                matches.extend(self.inventory.match(entityName))
                if len(matches) == 1:
                    match = matches[0]
                    raise CannotPerformAction("You don't have the %s" % match.name)
            if len(matches) > 1:
                raise AmbiguousEntity(matches)
        if action.isPlacing():
            nameOfObjectToPlace = action.object
            containerName = action.indirectObject
            if nameOfObjectToPlace is None:
                raise MissingObject('What do you want to place?')
            if containerName is None:
                raise MissingObject('What do you want to place the %s on?' % nameOfObjectToPlace)
            objectToPlace = self.matchToPlayerInventory(
                                       nameOfObjectToPlace,
                                       player)
            container = self.match(containerName,
                                   player)
            try:
                whichSlot = InventoryManager.getSlotKey(
                                   key=action.preposition)
                player.place(objectToPlace,
                            container,
                            whichSlot=whichSlot)
            except CannotPerformAction:
                raise CannotPerformAction('You cannot place the %s %s the %s' % (nameOfObjectToPlace,
                                                                                 action.preposition,
                                                                                 containerName))
            print 'You place the %s %s the %s' % (nameOfObjectToPlace,
                                                  action.preposition,
                                                  container.getDisplayName())
            return True
        if action.isThrowing():
            nameOfDirectObject = action.object
            nameOfIndirectObject = action.indirectObject
            if nameOfDirectObject is None:
                raise MissingObject('What do you want to throw?')
            if nameOfIndirectObject is None:
                raise MissingObject('What do you want to throw the %s at?' % nameOfIndirectObject)
            
            try:
                directObject = self.matchToPlayerInventory(nameOfDirectObject,
                                                           player)
            except NotPresent:
                raise NotPresent('You cannot throw what you do not have')
            indirectObject = self.matchToRoom(nameOfIndirectObject)
            
            player.throw(directObject,
                         indirectObject,
                         where=action.preposition)

            return True
        
        if action.isPositioningSelf():
            nameOfDirectObject = action.object
            directObject = self.matchToRoom(entityName=nameOfDirectObject)
            player.position(entityWithWhichToPosition=directObject,
                            whereToPosition=action.preposition)
            return True
        
        if action.isReplacing():
            nameOfDirectObject = action.object
            nameOfIndirectObject = action.indirectObject
            if nameOfDirectObject is None:
                raise MissingObject('What do you want to replace?')
            directObject = self.matchToRoom(entityName=nameOfDirectObject)
            if nameOfIndirectObject is None:
                raise MissingObject('What do you want to replace %s with?'
                                    % (directObject.getDisplayNameWithDefiniteArticle()))
            indirectObject = self.matchToPlayerInventory(entityName=nameOfIndirectObject,
                                                         player=player)
        
            player.replace(entityToReplace=directObject,
                          entityToReplaceWith=indirectObject)
            return True
        
        if action.isGiving():
            nameOfDirectObject = action.object
            nameOfIndirectObject = action.indirectObject
            if nameOfDirectObject is None:
                raise MissingObject('What do you want to give?')
            if nameOfIndirectObject is None:
                raise MissingObject('To whom do you wish to give the %s?')
            directObject = self.matchToPlayerInventory(entityName=nameOfDirectObject,
                                                       player=player)
            indirectObject = self.matchToRoom(entityName=nameOfIndirectObject)
            player.give(entityToGive=directObject,
                        entityToGiveTo=indirectObject)
            return True
        
        nameOfDirectObject = action.object
        nameOfIndirectObject = action.indirectObject
        
        if nameOfDirectObject is None:
            raise MissingObject('What do you want to %s' % verb)
        directObject = self.match(nameOfDirectObject,
                                  player)
        
        if action.isLookingAtEntity():
            player.lookAt(entityToLookAt=directObject)
            return True
        if action.isReading():
            directObject.read()
            return True
        if action.isEating():
            player.eat(directObject)
            return True
        if action.isDestroying():
            indirectObject = None
            if action.preposition == 'with':
                indirectObject = self.match(entityName=nameOfIndirectObject,
                                            player=player,
                                            default=None)
            player.destroy(entityToDestroy=directObject,
                           itemToUse=indirectObject)
            return True
        if action.isCutting():
            if nameOfIndirectObject is None:
                raise MissingObject('With what do you want to cut the %s?' % directObject.getDisplayName())
            indirectObject = self.matchToPlayerInventory(nameOfIndirectObject,
                                                         player)
            player.cut(directObject,
                       indirectObject)
            return True
        if action.isTalking():
            player.talk(entityToTalkTo=directObject,
                        subjectOfConversation=nameOfIndirectObject)
            return True
        if action.isAsking():
            if nameOfIndirectObject is None:
                raise MissingObject('What do you want to ask %s about?' % (directObject.getDisplayNameWithDefiniteArticle()))
            player.ask(entityToAsk=directObject,
                       subjectOfConversation=nameOfIndirectObject)
            return True
        if action.isWriting():
            if nameOfIndirectObject is None:
                raise MissingObject('What do you want to write with?')
            indirectObject = self.matchToPlayerInventory(nameOfIndirectObject,
                                                         player)
            player.write(entityToWriteOn=directObject,
                         itemToWriteWith=indirectObject)
            return True
        if action.isSwimming():
            player.swim(entityToSwimIn=directObject)
            return True
        if action.isKissing():
            player.kiss(entityToKiss=directObject)
            return True
        if action.isListening():
            player.listen(entityToListenTo=directObject)
            return True
        if action.isTasting():
            player.taste(entityToTaste=directObject)
            return True
        if action.isSmelling():
            player.smell(entityToSmell=directObject)
            return True
        if action.isFeeling():
            player.feel(entityToFeel=directObject)
            return True
        if action.isHugging():
            player.hug(entityToHug=directObject)
            return True
        if action.isAttaching():
            if nameOfIndirectObject is None:
                raise MissingObject('What do you want to attach %s to?' %
                                    directObject.getDisplayNameWithDefiniteArticle())
            entityToAttachTo = self.match(nameOfIndirectObject,
                                          player=player)
            nameOfEntityToAttachWith = action.indirectObjectPhrase.get('with')
            if nameOfEntityToAttachWith is None:
                entityToAttachWith = None
            else:
                entityToAttachWith =\
                    self.match(entityName=nameOfEntityToAttachWith,
                               player=player)
            player.attach(entityToAttach=directObject,
                          entityToAttachTo=entityToAttachTo,
                          entityToAttachWith=entityToAttachWith)
            return True
        if action.isUnattaching():
            if nameOfIndirectObject is not None:
                pass
            else:
                entityToUnattach
        
        if action.isTearing():
            player.tear(entityToTear=directObject)
            return True
        if action.isStriking():
            if nameOfIndirectObject is None:
                indirectObject = None
            else:
                indirectObject = self.matchToPlayerInventory(
                                            entityName=nameOfIndirectObject,
                                            player=player)
            player.strike(entityToStrike=directObject,
                          entityToStrikeWith=indirectObject)
            return True
        if action.isOpening():
            player.open(entityToOpen=directObject)
            return True
        if action.isClosing():
            player.close(entityToClose=directObject)
            return True
        if action.isLocking():
            if nameOfIndirectObject is None:
                indirectObject = None
            else:
                indirectObject = self.match(entityName=nameOfIndirectObject,
                                            player=player)
            player.lock(entityToLock=directObject,
                        entityToLockWith=indirectObject)
            return True
        if action.isUnlocking():
            if nameOfIndirectObject is None:
                indirectObject = None
            else:
                indirectObject = self.match(entityName=nameOfIndirectObject,
                                            player=player)
            player.unlock(entityToUnlock=directObject,
                          entityToUnlockWith=indirectObject)
            return True
        if action.isBlocking():
            if nameOfIndirectObject is None:
                indirectObject = None
            else:
                indirectObject = self.match(entityName=nameOfIndirectObject,
                                            player=player)
            player.block(entityToBlock=directObject,
                         entityToBlockWith=indirectObject)
            return True
        if action.isUnblocking():
            player.unblock(entityToUnblock=directObject)
            return True
        if action.isSearching():
            if nameOfIndirectObject is None:
                indirectObject = None
            else:
                indirectObject = self.matchToPlayerInventory(
                                            entityName=nameOfIndirectObject,
                                            player=player)
            player.search(entityToSearch=directObject,
                          entityToSearchWith=indirectObject)
            return True
        if action.isClimbing():
            player.climb(entityToClimb=directObject)
            
        
        
        #Direct object expected to be in player inventory
        
        directObject = self.matchToPlayerInventory(entityName=nameOfDirectObject,
                                                   player=player)
        
        if action.isDipping():
            if nameOfIndirectObject is None:
                raise MissingObject('Into what do you want to dip %s?'
                                    % entity.getDisplayNameWithDefiniteArticle())
            indirectObject = self.match(entityName=nameOfIndirectObject,
                                        player=player)
            player.dip(entityToDip=directObject,
                       entityToDipIn=indirectObject)
            return True
        
        
        return False
    
    def handleTravelTo(self,
                       travellingAgent):
        obstruction = Room.getObstruction(fromRoom=travellingAgent.currentOwner.name,
                                          toRoom=self.name)
        if obstruction is not None:
            raise CannotPerformAction(obstruction.description)
        
        travellingAgent.changeOwner(self)
        currentOwner = travellingAgent.currentOwner
        print currentOwner.getDescription()