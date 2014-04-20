import sys

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

    def isLookingAtRoom(self):
        if (self.sentence.verb in ('look', 'examine') and
            (self.sentence.object in ('room',) or 
             self.sentence.object is None)):
            return True

    def isCheckingInventory(self):
        if (self.sentence.command == 'inventory' or
            self.sentence.verb in ('look', 'examine') and
            self.sentence.object == 'inventory'):
            return True

    def isQuitting(self):
        if self.sentence.command in ('quit', 'exit'):
            return True

    def isSaving(self):
        if self.sentence.command == 'save':
            return True

    def isRestoring(self):
        if self.sentence.command in ('restore', 'load'):
            return True

    def act(self):
        currentOwner = self.player.currentOwner
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
        if self.isLookingAtRoom():
            print currentOwner.getDescription(isLooking=True)
            return True
        if self.isCheckingInventory():
            displayPlayerInventory(self.player.inventory)
            return True
        if self.isQuitting():
            sys.exit(0)
            return True
        if self.isSaving():
            raise NotImplemented('Saving is not implemented')
        if self.isRestoring():
            raise NotImplemented('Restoring is not implemented')
        
        return currentOwner.actOnAction(action=self,
                                        player=self.player)
