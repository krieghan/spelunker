import sys

from text_adventure.grammar.interpreter import Interpreter
from text_adventure.inventory import displayPlayerInventory
from text_adventure.exception import \
    (CannotGoThatWay,
     DenyInput, 
     NotImplemented,
     PlayerDeath)

from entity.room import Room
from entity.agent import Agent
from entity.item import Item
from spelunker.action import Action
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
                sentence = interpreter.evaluate(actionText)
                action = Action(sentence=sentence,
                                player=self.player)
                succeeded = action.act()
                if not succeeded:
                    raise CouldNotInterpret('I understood "%s", but did not know what to do with it.' % actionText)
            except DenyInput, e:
                print str(e)
                continue
            except PlayerDeath:
                print "You have died"
                sys.exit()
    
    def getEntityNames(self):
        return Agent.getNames() + Room.getNames() + Item.getNames()
            
    
if __name__ == '__main__':
    game = Game()
    game.run()
