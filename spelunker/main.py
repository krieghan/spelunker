import sys

from text_adventure.grammar.interpreter import Interpreter
from text_adventure.inventory import displayPlayerInventory
from text_adventure.exception import \
    (CouldNotInterpret, 
     CannotGoThatWay,
     CannotPerformAction, 
     DenyInput, 
     NotImplemented,
     PlayerDeath)

from entity.room import Room
from entity.agent import Agent
from entity.item import Item
from spelunker.items.items import createItems
from spelunker.agents.agents import createAgents
from spelunker.rooms.rooms import createRooms
from spelunker.container import fillContainers
from spelunker.dictionary import dictionary, thesaurus
from spelunker.agents.player import Player

class Game(object):
    
    def run(self):
        self.player = Player(name='Player')
        
        createRooms()
        createAgents()
        createItems()
        fillContainers()
        entityNouns = [x.lower() for x in self.getEntityNames()]
        dictionary.get('nouns').extend(entityNouns)
        interpreter = Interpreter(dictionary=dictionary,
                                  thesaurus=thesaurus)
        
        self.player.changeOwner(Room.getRoom('Entrance'))
        print self.player.currentOwner.getDescription()
        
        while(True):
            actionText = raw_input('>')
            
            try:
                action = interpreter.evaluate(actionText)
                succeeded = self.actOnAction(action)
                if not succeeded:
                    raise CouldNotInterpret('I understood "%s", but did not know what to do with it.' % actionText)
            except DenyInput, e:
                print e
                continue
            except PlayerDeath:
                print "You have died"
                sys.exit()
    
    def getEntityNames(self):
        return Agent.getNames() + Room.getNames() + Item.getNames()
    
    def actOnAction(self,
                    action):
        currentOwner = self.player.currentOwner
        if action.isTravelling():
            if action.object is None:
                raise CouldNotInterpret('Where do you want to go?')
            placeToTravel = self.player.currentOwner.getRoomInDirection(action.object)
            if placeToTravel is None:
                raise CannotPerformAction('You cannot go that way')
            self.player.travel(placeToTravel=placeToTravel)
            return True
        if action.isLookingAtRoom():
            print currentOwner.getDescription(isLooking=True)
            return True
        if action.isCheckingInventory():
            displayPlayerInventory(self.player.inventory)
            return True
        if action.isQuitting():
            sys.exit(0)
            return True
        if action.isSaving():
            raise NotImplemented('Saving is not implemented')
        if action.isRestoring():
            raise NotImplemented('Restoring is not implemented')
        
        return currentOwner.actOnAction(action=action,
                                        player=self.player)
    
if __name__ == '__main__':
    game = Game()
    game.run()
