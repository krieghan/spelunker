import sys

from text_adventure import (
        inventory,
        sentence)
from text_adventure.exception import \
        (CouldNotInterpret,
         CannotPerformAction,
         NotImplemented)

class Action(object):
    def __init__(self, sentence, player):
        self.sentence = sentence
        self.player = player

    def isTravelling(self):
        if self.sentence.verb in ('walk', 'run', 'go'):
            return True
        if (self.sentence.verb is None and
            self.sentence.object in ('north', 'south', 'east',
                                     'west', 'up', 'down')):
            return True

    def isLooking(self):
        return self.sentence.verb in ('look', 'examine')

    def isGetting(self):
        return self.sentence.verb == 'get'

    def isDropping(self):
        return self.sentence.verb == 'drop'

    def isCheckingInventory(self):
        if (self.sentence.verb in ('look', 'examine') and
            self.sentence.object == 'inventory'):
            return True

    def isPlacing(self):
        return self.sentence.verb == 'put'

    def isThrowing(self):
        return self.sentence.verb == 'throw'

    def isPositioningSelf(self):
        return False

    def isReplacing(self):
        return False

    def isGiving(self):
        return False

    def isReading(self):
        return False

    def isEating(self):
        return False

    def isDestroying(self):
        return False

    def isCutting(self):
        return False

    def isTalking(self):
        return False

    def isAsking(self):
        return False

    def isWriting(self):
        return False

    def isSwimming(self):
        return False

    def isKissing(self):
        return False

    def isListening(self):
        return False

    def isTasting(self):
        return False

    def isSmelling(self):
        return False

    def isFeeling(self):
        return False

    def isHugging(self):
        return False

    def isAttaching(self):
        return False

    def isUnattaching(self):
        return False

    def isTearing(self):
        return False

    def isStriking(self):
        return False

    def isOpening(self):
        return self.sentence.verb == 'open'

    def matchObjects(self, object_names):
        return {k: self.player.currentOwner.match(
                            entityName=v,
                            player=self.player)
                for (k, v) in object_names.items() if v is not None}

    def act(self):
        currentOwner = self.player.currentOwner
        sentenceObjectNames = self.sentence.getObjects()
        sentenceObjects = self.matchObjects(sentenceObjectNames)

        if isinstance(self.sentence, sentence.Command):
            if self.sentence.isCheckingInventory():
                inventory.displayPlayerInventory(self.player.inventory)
                return True
            if self.sentence.isQuitting():
                sys.exit(0)
                return True
            if self.sentence.isSaving():
                raise NotImplemented('Saving is not implemented')
            if self.sentence.isRestoring():
                raise NotImplemented('Restoring is not implemented')
        else:
            if self.isTravelling():
                if self.sentence.object is None:
                    raise CouldNotInterpret('Where do you want to go?')
                placeToTravel =\
                    self.player.currentOwner.getRoomInDirection(
                            self.sentence.object)
                if placeToTravel is None:
                    raise CannotPerformAction('You cannot go that way')
                self.player.travel(placeToTravel=placeToTravel)
                return True
            if self.isLooking():
                self.player.look(sentenceObjectNames, sentenceObjects)
                return True
            if self.isCheckingInventory():
                inventory.displayPlayerInventory(self.player.inventory)
                return True
            if self.isGetting():
                self.player.get(sentenceObjectNames, sentenceObjects)
                return True
        
        return currentOwner.actOnAction(action=self,
                                        player=self.player)
