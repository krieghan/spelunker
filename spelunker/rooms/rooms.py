from entity.room import Room
from spelunker.rooms.wolfDen import WolfDen

def createRooms():
    entrance = Room(name='Entrance',
                    description='You are at the entrance of a cave.  There are paths down, to the south and to the east.',
                    down='Sunlight Room',
                    south='North Of Town',
                    east='Wolf Den')
    sunlightRoom = Room(name='Sunlight Room',
                        description='You enter a room of the cave.  Sunlight pours in from the entrance.  From here, you can go up to the cave entrance.',
                        up='Entrance',
                        south='Dark Room')
    pathToTown = Room(name='North Of Town',
                      description='You are walking along the path from the town to the cave.  There is a path that runs from the north to the south',
                      north='Entrance',
                      south='Town Gate',
                      west='Pond')
    wolfDen = WolfDen(name='Wolf Den',
                      description='You come to a corner of the woods unlike any other.  The bones of small creatures litter the forest floor.  From here, you can go back west to the cave entrance.',
                      west='Entrance')
    townGate = Room(name='Town Gate',
                    description='You are standing at the gate to town, which lies to the south.  The path to the cave runs to the north of where you are now.',
                    north='North Of Town',
                    south='Town Plaza')
    townPlaza = Room(name='Town Plaza',
                     description='Town is smaller than it might appear from the outside.  A few assorted buildings run along the street.  To the north is the town gate.',
                     north='Town Gate')
    pond = Room(name='Pond',
                description='You come to a tranquil pond in the forest.',
                east='North Of Town')
    inPond = Room(name='In the Pond',
                  description='You are under the surface of the pond.',
                  up='Pond')
    darkRoom = Room(name='Dark Room',
                    description='It is pitch black in here.',
                    north='Sunlight Room')