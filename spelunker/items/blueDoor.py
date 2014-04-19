from entity.item import Item
from text_adventure.exception import CannotPerformAction

from spelunker.items.door import RoomDoor

class BlueDoor(RoomDoor):
    

    def handleReceivingLock(self,
                   lockingAgent,
                   entityToLockWith=None):
        if self.door.locked:
            raise CannotPerformAction('%s is already locked.' %
                                      self.getDisplayNameWithDefiniteArticle())
        if self.door.open:
            raise CannotPerformAction('%s is open.  It cannot be locked at this time.' %
                                      self.getDisplayNameWithDefiniteArticle())
        if entityToLockWith == Item.getItem('Blue Key'):
            self.door.locked = True
            print 'You lock the door.'
        elif entityToLockWith is not None:
            raise CannotPerformAction('You cannot lock %s with %s' %
                                      self.getDisplayNameWithDefiniteArticle(),
                                      entityToLockWith.getDisplayNameWithDefiniteArticle())
        else:
            raise CannotPerformAction(
                        'You cannot lock %s with your bare hands' %
                        self.getDisplayNameWithDefiniteArticle())
            
    def handleReceivingUnlock(self,
                     unlockingAgent,
                     entityToUnlockWith=None):
        if not self.door.locked:
            raise CannotPerformAction('%s is already unlocked.' %
                                      self.getDisplayNameWithDefiniteArticle())
        if entityToUnlockWith == Item.getItem('Blue Key'):
            self.door.locked = False
            print 'You unlock the door.'
        elif entityToUnlockWith is not None:
            raise CannotPerformAction('You cannot unlock %s with %s' %
                                      self.getDisplayNameWithDefiniteArticle(),
                                      entityToUnlockWith.getDisplayNameWithDefiniteArticle())
        else:
            raise CannotPerformAction(
                        'You cannot unlock %s with your bare hands' %
                        self.getDisplayNameWithDefiniteArticle())
