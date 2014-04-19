from entity.item import Item
from entity.room import Room
from entity.obstruction import Obstruction
from text_adventure.exception import CannotPerformAction

class Door(object):
    def __init__(self,
                 room1,
                 room2,
                 room1Description,
                 room2Description,
                 room1DoorClass=None,
                 room2DoorClass=None,
                 room1DisplayName='door',
                 room2DisplayName='door',
                 locked=False,
                 open=False,
                 blockedBy=None):
        if room1DoorClass is None:
            room1DoorClass = RoomDoor
        if room2DoorClass is None:
            room2DoorClass = RoomDoor
        name = 'Door between %s and %s' % (room1,
                                           room2)
        doorInRoom1 = room1DoorClass(
                               door=self,
                               thisRoom=room1,
                               otherRoom=room2,
                               name='%s in %s' % (name,
                                                  room1),
                               description=room1Description,
                               displayName=room1DisplayName)
        doorInRoom2 = room2DoorClass(
                               door=self,
                               thisRoom=room1,
                               otherRoom=room2,
                               name='%s in %s' % (name,
                                                  room2),
                               description=room2Description,
                               displayName=room2DisplayName)
        Room.getRoom(room1).addEntity(doorInRoom1)
        Room.getRoom(room2).addEntity(doorInRoom2)
        self.open = open
        self.locked = locked
        self.blockedBy = blockedBy
        if not open:
            Room.addObstruction(fromRoom=room1,
                                toRoom=room2,
                                obstruction=closedDoorObstruction)
            Room.addObstruction(fromRoom=room2,
                                toRoom=room1,
                                obstruction=closedDoorObstruction)

class RoomDoor(Item):
    def __init__(self,
                 door,
                 thisRoom,
                 otherRoom,
                 name,
                 aliases=None,
                 description='',
                 displayName='door'):
        if aliases is None:
            aliases = ['door']
        Item.__init__(self,
                      name=name,
                      aliases=aliases,
                      description=description,
                      displayName=displayName)
        self.door = door
        self.thisRoom = thisRoom
        self.otherRoom = otherRoom
        
    def handleOpen(self,
                   openingAgent):
        if self.door.open == True:
            raise CannotPerformAction('%s is already open' %
                                      self.getDisplayNameWithDefiniteArticle())
        elif self.door.locked:
            raise CannotPerformAction('%s is locked.  It cannot be opened at this time.' %
                                      self.getDisplayNameWithDefiniteArticle())
        elif self.door.blockedBy:
            raise CannotPerformAction('%s is blocked by %s.  It cannot be opened at this time.' %
                                      (self.getDisplayNameWithDefiniteArticle(),
                                       self.door.blockedBy.getDisplayNameWithDefiniteArticle()))
        else:
            self.door.open = True
            Room.removeObstruction(fromRoom=self.thisRoom,
                                   toRoom=self.otherRoom)
            Room.removeObstruction(fromRoom=self.otherRoom,
                                   toRoom=self.thisRoom)
            print ('You open %s' %
                   self.getDisplayNameWithDefiniteArticle())
            
    def handleClose(self,
                    closingAgent):
        if self.door.open == False:
            raise CannotPerformAction('%s is already closed' %
                                      self.getDisplayNameWithDefiniteArticle())
        else:
            self.door.open = False
            Room.addObstruction(fromRoom=self.thisRoom,
                                toRoom=self.otherRoom,
                                obstruction=closedDoorObstruction)
            Room.addObstruction(fromRoom=self.otherRoom,
                                toRoom=self.thisRoom,
                                obstruction=closedDoorObstruction)
            print ('You close %s' %
                   self.getDisplayNameWithDefiniteArticle())
                
    def handleReceivingLock(self,
                            lockingAgent,
                            entityToLockWith):
        raise CannotPerformAction("This door doesn't lock")
    
    def handleReceivingUnlock(self,
                              unlockingAgent,
                              entityToUnlockWith):
        raise CannotPerformAction("This door doesn't unlock")
    
    def handleReceivingBlock(self,
                             blockingAgent,
                             entityToBlockWith=None):
        if self.door.blockedBy:
            raise CannotPerformAction('%s is already blocked by %s' %
                                      (self.getDisplayNameWithDefiniteArticle(),
                                       self.door.blockedBy.getDisplayNameWithDefiniteArticle()))
        if self.door.open:
            raise CannotPerformAction('This door is already open.  It makes no sense to block it with anything.')
        if entityToBlockWith == Item.getItem('Crate'):
            self.door.blockedBy = entityToBlockWith
            print ('You block %s with %s' %
                   (self.getDisplayNameWithDefiniteArticle(),
                   entityToBlockWith.getDisplayNameWithDefiniteArticle()))
        else:
            Item.handleReceivingBlock(self,
                                      blockingAgent=blockingAgent,
                                      entityToBlockWith=entityToBlockWith)
            
    def handleReceivingUnblock(self,
                               unblockingAgent):
        if self.door.blockedBy is None:
            raise CannotPerformAction("You can't very well unblock something that isn't blocked in the first place.")
        self.door.blockedBy = None
        print ('You unblock %s' %
               self.getDisplayNameWithDefiniteArticle())
        
closedDoorObstruction = Obstruction(description='You have to open the door first.')
