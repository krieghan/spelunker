from entity.item import Item
from entity.man import Man
from text_adventure.stateMachine.stateMachine import StateMachine
from text_adventure.stateMachine.state import State


class DarkHenry(Man):
    
    def __init__(self,
                 name='Dark Henry'):
        description = 'Henry is an emaciated figure dressed in assorted black and grey rags.  He skulks about the town plaza.'
        
        Man.__init__(self,
                       name=name,
                       displayName='Henry',
                       description=description,
                       aliases=['Henry',
                                'Dark Henry',
                                'Man'])
        self.stateMachine = StateMachine(owner=self,
                                         startingState=darkHenryStartingState)
        
    def getDisplayNameWithDefiniteArticle(self):
        return self.getDisplayName()
    
    def getDisplayNameWithIndefiniteArticle(self):
        return self.getDisplayName()
    
    def handleTalk(self,
                   talkingAgent,
                   subjectOfConversation):
        if subjectOfConversation is None:
            self.speak('Why are you bothering me?')
            return True
        if subjectOfConversation == 'blue note':
            self.speak("And you say you have no idea how you got it?  That's just downright creepy.")
            return True
        if subjectOfConversation == 'tattered note':
            self.speak("That's Alec's handwriting.  Guess he didn't make it.")
            return True
        if subjectOfConversation == 'alec':
            self.speak('He was an idiot to go looking for the sceptre.  But no one should die like that - all alone and cold in the dark.')
            return True
        if subjectOfConversation == 'dark henry':
            self.speak("I'm raggedy and I smell bad.  Do you think I care?")
            return True
        if subjectOfConversation == 'cave':
            self.speak('Yeah, that place is dangerous.  I know someone who went there a few months ago to look for the blue sceptre.  He never returned.')
            return True
        self.speak("Yeah, yeah, very interesting.  Look, can we hurry this up?")
        return False
    
    def handleAsk(self,
                  askingAgent,
                  subjectOfConversation):
        if subjectOfConversation == 'alec':
            self.speak("An even-tempered guy.  But, well, I guess it was about a year ago, he started going on about this blue sceptre.  No idea what the thing is, but two months ago he went off to that cave to go looking for it.  Haven't seen him since.")
            return True
        
        self.speak("I'm not at all interested in that.")
        return False
    
    def handleReceiveKiss(self,
                          kissingAgent):
        self.speak("What the hell are you doing, man?  I don't go in for that sort of thing!")
    
    def handleFeeling(self,
                      feelingAgent):
        self.speak("Dude, don't touch me.  I have this thing about strange people touching me.")
        
    def handleReceiveGive(self,
                            givingAgent,
                            entityToGive):
        if entityToGive == Item.getItem('Note from Adventurer'):
            self.speak("So I guess Alec didn't make it.  It's a shame.  I'll give the note to Stephanie next time I see her.")
            entityToGive.changeOwner(self)
        else:
            self.speak("What do I look like?  An old canvas sack?  I'm not here to hold onto all that random shit you're picking up, dude.")
    
class DarkHenryStartingState(State):
    pass

darkHenryStartingState = DarkHenryStartingState()
