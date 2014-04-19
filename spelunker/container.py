from entity.agent import Agent
from entity.item import Item
from entity.room import Room

def fillContainers():
    wall = Item.getItem('Wall')
    pathToTown = Item.getItem('Path To Town')
    
    player = Agent.getAgent('Player')
    player.addEntity(Item.getItem('Note from Unknown Party'))
    
    table = Item.getItem('Table')
    sunlightRoom = Room.getRoom('Sunlight Room')
    sunlightRoom.addEntity(Item.getItem('Note from Adventurer'))
    sunlightRoom.addEntity(table)
    sunlightRoom.addEntity(wall)
    table.addEntity(Item.getItem('Apple'))
    table.addEntity(Item.getItem('Paper'))
    table.addEntity(Item.getItem('Pencil'))
    
    sack = Item.getItem('Canvas Sack')
    entrance = Room.getRoom('Entrance')
    entrance.addEntity(pathToTown)
    entrance.addEntity(wall)
    entrance.addEntity(sack)
    sack.addEntity(Item.getItem('Dagger'))
    
    pathToTownLocation = Room.getRoom('North Of Town')
    pathToTownLocation.addEntity(Item.getItem('Rock'))
    pathToTownLocation.addEntity(pathToTown)
    
    townGate = Room.getRoom('Town Gate')
    townGate.addEntity(Item.getItem('Rope'))
    
    wolfDen = Room.getRoom('Wolf Den')
    wolfDen.addEntity(Agent.getAgent('Wolf'))
    wolfDen.addEntity(Item.getItem('Blue Key'))
    
    townPlaza = Room.getRoom('Town Plaza')
    townPlaza.addEntity(Agent.getAgent('Dark Henry'))    
    
    pond = Room.getRoom('Pond')
    tree = Item.getItem('Tree')
    pond.addEntity(tree)
    tree.addEntity(Item.getItem('Acorn'))
    pond.addEntity(Item.getItem('Pond'))
    
    darkRoom = Room.getRoom('Dark Room')
    darkRoom.addEntity(Item.getItem('Crate'))