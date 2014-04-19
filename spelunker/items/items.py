from entity.item import Item
from entity.prop import Prop

from spelunker.items.note import Note
from spelunker.items.table import Table
from spelunker.items.bag import Bag
from spelunker.items.dagger import Dagger
from spelunker.items.rock import Rock
from spelunker.items.food import Food
from spelunker.items.paper import Paper
from spelunker.items.pencil import Pencil
from spelunker.items.acorn import Acorn
from spelunker.items.tree import Tree
from spelunker.items.pond import Pond
from spelunker.items.rope import Rope
from spelunker.items.door import Door
from spelunker.items.blueDoor import BlueDoor
from spelunker.items.key import Key
from spelunker.items.crate import Crate

def createItems():
    Note(name='Note from Unknown Party',
         description='A note from an unknown party.',
         aliases=['note'],
         text='I am watching you.',
         displayName='blue note')
    Note(name='Note from Adventurer',
         description='A tattered note, found near the entrance of the cave.',
         aliases=['note'],
         displayName='tattered note',
         text='I could not find the blue sceptre')
    Prop(name='Wall',
         description='The walls of the cave widely vary in shades of grey.',
         aliases=['walls',
                  'cave'],
         displayName='wall')
    Prop(name='Path To Town',
         description='The path to town is paved with many generations of dirt and gravel.  The gravel at the edge of the path blends into the tall grass and wilderness.',
         aliases=['road',
                  'path'],
         displayName='path to town')
    Rock(name='Rock',
         description='There is a small white stone here.  It is round with one particularly sharp edge',
         aliases=['rock',
                  'stone'],
         displayName='rock',
         isGettable=True,
         displayAutomatically=True)
    Table(name='Table',
          description='There is a simple wooden table here.  It has four round legs.',
          aliases=['table'],
          displayName='table')
    Bag(name='Canvas Sack',
        description='There is a canvas sack on the floor.',
        aliases=['sack',
                 'bag'],
        displayName='canvas sack')
    Dagger(name='Dagger',
         description='There is a short dagger here.',
         aliases=['dagger',
                  'knife'],
         displayName='dagger',
         isGettable=True)
    Key(name='Blue Key',
         description='There is a blue key here.',
         aliases=['key',
                  'blue key'],
         displayName='blue key',
         displayAutomatically=True,
         isGettable=True)
    Food(name='Apple',
         description='There is an apple here.  It has an irregular spherical shape and a dull red in color.',
         displayName='apple',
         displayAutomatically=True,
         isGettable=True)
    Paper(name='Paper')
    Pencil(name='Pencil')
    Tree(name='Tree',
         description='There is a tree at the side of the pond.  It provides shade to the surface of the pond.  You see something hanging in the tree, but cannot quite tell what it is at this angle.')
    Acorn(name='Acorn',
          description='There is an acorn here.  It has a rough dark-brown hood and a smooth light-brown surface.')
    Pond(name='Pond',
         description='Ripples emanate from the center of the pond, where fish occasionally arc out and back into the water.')
    Rope(name='Rope')
    Door(
         room1='Sunlight Room',
         room2='Dark Room',
         room1DoorClass=BlueDoor,
         room2DoorClass=BlueDoor,
         room1Description='There is a door to the south.  It is made of creaky old wood.',
         room2Description='There is a door to the north.  It is made of creaky old wood.',
         locked=True)
    Crate(name='Crate',
          description='There is a medium sized wooden crate here.')