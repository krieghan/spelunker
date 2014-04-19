from entity.item import Item

class Prop(Item):
    def __init__(self,
                 name,
                 displayName=None,
                 description=None,
                 shortDescription=None,
                 inventory=None,
                 aliases=None,
                 isGettable=False,
                 displayAutomatically=False):
        Item.__init__(self,
                      name=name,
                      displayName=displayName,
                      description=description,
                      shortDescription=shortDescription,
                      inventory=inventory,
                      aliases=aliases,
                      isGettable=isGettable,
                      displayAutomatically=displayAutomatically)