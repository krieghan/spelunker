class DenyInput(Exception):
    pass

class CouldNotInterpret(DenyInput):
    pass

class CannotGoThatWay(DenyInput):
    pass

class NotPresent(DenyInput):
    pass

class AmbiguousEntity(DenyInput):
    def __init__(self, matches):
        self.matches = matches
        
    def __str__(self):
        allMatches = [x.name for x in self.matches]
        commaMatchString = ', '.join(allMatches[:-1])
        matchString = 'Did you mean %s or %s' % (commaMatchString, allMatches[-1])
        return matchString

class CannotPerformAction(DenyInput):
    pass

class MissingObject(DenyInput):
    pass

class NotImplemented(DenyInput):
    pass

class AmbiguousStructure(DenyInput):
    pass



class PlayerDeath(Exception):
    pass

#Game loop won't catch:

class ItemNotFound(Exception):
    pass

class NotPermitted(Exception):
    pass