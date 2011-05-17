from entity.item import Item

class Food(Item):
    def handleEat(self):
        self.removeFromOwner()