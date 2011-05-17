class InventoryManager(object):
    def __init__(self,
                 on=False,
                 under=False,
                 inside=False):
        self.slots = dict() 
        if on:
            self.slots['on'] = Inventory()
        if under:
            self.slots['under'] = Inventory()
        if inside:
            self.slots['inside'] = Inventory()
        
    def match(self, entityKey):
        matches = []
        for (key, inventory) in self.slots.items():
            if not inventory.exposed:
                continue
            matches.extend(inventory.match(entityKey))
        return matches
    
    @classmethod
    def getSlotKey(cls,
                   key):
        if key in ('on', 'onto'):
            return 'on'
        if key in ('under',):
            return 'under'
        if key in ('inside', 'in', 'into'):
            return 'inside'
        
        return 'on'

class Inventory(dict):
    
    def __init__(self, 
                 exposed=True,
                 **kwargs):
        self.exposed = exposed
        dict.__init__(self,
                      **kwargs)
    
    def match(self, entityKey):
        
        matches = []
        for (key, entity) in self.items():
            if entityKey in entity.names:
                matches.append(entity)
            if not entity.recurseAutomatically:
                continue
            matches.extend(entity.inventory.match(entityKey))
        return matches

def displayPlayerInventory(inventory):
    print "In your inventory, you have:"
    slot = inventory.slots['inside']
    inventoryItems = slot.items()
    if not inventoryItems:
        print "nothing"
    else:
        for item in slot.values():
            print item.name