from entity.human import Human
from text_adventure.inventory import InventoryManager

class Player(Human):
    def __init__(self,
                 name,
                 displayAutomatically=False):
        inventory = InventoryManager(on=False,
                                     under=False,
                                     inside=True)
        Human.__init__(self,
                       name=name,
                       displayAutomatically=displayAutomatically,
                       inventory=inventory,
                       recurseAutomatically=False,
                       displayName='handsome looking gentleman')
