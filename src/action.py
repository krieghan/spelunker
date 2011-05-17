class Action(object):
    def __init__(self,
                 verb,
                 object=None,
                 preposition=None,
                 indirectObject=None,
                 indirectObjectPhrase=None):
        if indirectObjectPhrase is None:
            indirectObjectPhrase = dict()
        self.verb = verb
        self.object = object
        self.preposition = preposition
        self.indirectObject = indirectObject
        self.indirectObjectPhrase = indirectObjectPhrase
    
    def verbOnly(self):
        if (self.verb is not None and 
            self.preposition is None and 
            self.object is None and 
            self.indirectObject is None):
            return True
        else:
            return False
    
    def isTravelling(self):
        if (self.verb == 'go' and
            (self.preposition is None or
             self.preposition == 'to')):
            return True
        else:
            return False
        
    def isLookingAtRoom(self):
        if (self.verb == 'look' and 
            (self.verbOnly() or
             (self.preposition == 'at' and
              self.indirectObject == 'room') or
             self.preposition == 'around')):
            return True
        else:
            return False
        
    def isLookingAtEntity(self):
        if (self.verb == 'look' and 
            (self.object is not None or self.indirectObject is not None)):
            return True
        else:
            return False
        
    def isReading(self):
        if self.verb == 'read':
            return True
        else:
            return False
        
    def isGetting(self):
        if ((self.verb == 'get') or
            (self.verb == 'pick' and self.preposition == 'up')):
            return True
        else:
            return False
        
    def isDropping(self):
        if (self.verb == 'drop' and 
            (self.indirectObject is None or
             self.indirectObject == 'ground')):
            return True
        else:
            return False
        
    def isPlacing(self):
        if ((self.verb == 'drop' or
             self.verb == 'put') and
            self.indirectObject is not None):
            return True
        else:
            return False
    
    def isThrowing(self):
        if self.verb == 'throw':
            return True
        else:
            return False
    
    def isThrowingAt(self):
        if ((self.verb == 'throw') and
            (self.preposition == 'at')):
            return True
        else:
            return False
        
    def isThrowingIn(self):
        if ((self.verb == 'throw') and
            (self.preposition == 'in')):
            return True
        else:
            return False
        
        
    def isCheckingInventory(self):
        if ((self.object == 'inventory' or 
             self.indirectObject == 'inventory') and
            (self.verb == 'look' or
             self.verb is None)):
            return True
        else:
            return False
            
        
    def isQuitting(self):
        if self.verb == 'quit':
            return True
        else:
            return False
        
    def isSaving(self):
        if self.verb == 'save':
            return True
        else:
            return False
        
    def isRestoring(self):
        if self.verb == 'restore':
            return True
        else:
            return False
        
    def isEating(self):
        if self.verb == 'eat':
            return True
        else:
            return False
        
    def isDestroying(self):
        if self.verb == 'destroy':
            return True
        else:
            return False
        
    def isCutting(self):
        if self.verb == 'cut':
            return True
        else:
            return False
        
    def isTalking(self):
        if self.verb == 'talk':
            return True
        else:
            return False
        
    def isAsking(self):
        if self.verb == 'ask':
            return True
        else:
            return False
        
    def isWriting(self):
        if self.verb == 'write':
            return True
        else:
            return False
        
    def isPositioningSelf(self):
        if ((self.verb == 'get' or
             self.verb == 'go' or
             self.verb == 'climb') and
            (self.preposition == 'under' or
             self.preposition == 'on')):
            return True
        else:
            return False
        
    def isSwimming(self):
        if self.verb == 'swim':
            return True
        else:
            return False
        
    def isKissing(self):
        if self.verb == 'kiss':
            return True
        else:
            return False
        
    def isListening(self):
        if self.verb == 'listen':
            return True
        else:
            return False
        
    def isTasting(self):
        if self.verb == 'taste':
            return True
        else:
            return False
        
    def isSmelling(self):
        if self.verb == 'smell':
            return True
        else:
            return False
        
    def isFeeling(self):
        if self.verb == 'feel':
            return True
        else:
            return False
        
    def isHugging(self):
        if self.verb == 'hug':
            return True
        else:
            return False
        
    def isAttaching(self):
        if self.verb == 'attach':
            return True
        else:
            return False
        
    def isUnattaching(self):
        if self.verb == 'unattach':
            return True
        else:
            return False
        
    def isReplacing(self):
        if self.verb == 'replace':
            return True
        else:
            return False
        
    def isTearing(self):
        if self.verb == 'tear':
            return True
        else:
            return False
        
    def isStriking(self):
        if self.verb == 'strike':
            return True
        else:
            return False
        
    def isOpening(self):
        if self.verb == 'open':
            return True
        else:
            return False
        
    def isClosing(self):
        if self.verb == 'close':
            return True
        else:
            return False
        
    def isLocking(self):
        if self.verb == 'lock':
            return True
        else:
            return False
        
    def isUnlocking(self):
        if self.verb == 'unlock':
            return True
        else:
            return False
        
    def isBlocking(self):
        if self.verb == 'block':
            return True
        else:
            return False
        
    def isUnblocking(self):
        if self.verb == 'unblock':
            return True
        else:
            return False
        
    def isDipping(self):
        if self.verb == 'dip':
            return True
        else:
            return False
        
    def isGiving(self):
        if self.verb == 'give':
            return True
        else:
            return False
        
    def isSearching(self):
        if self.verb == 'search':
            return True
        else:
            return False
        
    def isClimbing(self):
        if self.verb == 'climb':
            return True
        else:
            return False