from entity.item import Item

class Paper(Item):
    
    def __init__(self, 
                 name):
        Item.__init__(self,
                      name,
                      displayAutomatically=True,
                      isGettable=True,
                      displayName='paper',
                      aliases=['paper'])
        self.text = ''
    
    def handleReceivingWriting(self,
                               writingAgent,
                               itemToWriteWith):
        print 'You write on %s with the %s' % (self.getDisplayNameWithDefiniteArticle(),
                                               itemToWriteWith.getDisplayNameWithDefiniteArticle())
        self.text = 'I am now writing on this piece of paper'
        
    def getLongDescription(self,
                           isLooking=False):
        if self.text:
            return 'You see a piece of paper.  On it is written "%s"' % self.text
        else:
            return 'You see a piece of paper.  It is blank' 