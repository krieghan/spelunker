import sys

from entity.room import Room
from entity.agent import Agent
from entity.item import Item
from exception import \
    (CouldNotInterpret, 
     CannotGoThatWay,
     CannotPerformAction, 
     DenyInput, 
     NotImplemented,
     PlayerDeath)
from grammar.interpreter import Interpreter
from spelunker.items.items import createItems
from spelunker.agents.agents import createAgents
from spelunker.rooms.rooms import createRooms
from spelunker.container import fillContainers
from spelunker.dictionary import dictionary, thesaurus
from inventory import displayPlayerInventory
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
        multiWordTokens = self.getMultiWordTokens()
        interpreter = Interpreter(dictionary=dictionary,
                                  thesaurus=thesaurus,
                                  multiWordTokens=multiWordTokens)
        
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
    
    
    def getMultiWordTokens(self):
        multiWordTokens = []
        for (key, listOfTokens) in dictionary.items():
            for token in listOfTokens:
                if ' ' in token:
                    multiWordTokens.append(token)
    
        for synonymSet in thesaurus:
            for token in synonymSet:
                if ' ' in token:
                    multiWordTokens.append(token)
                    
        for key in self.getEntityNames():
            if ' ' in key:
                multiWordTokens.append(key)
        
        return multiWordTokens
    
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