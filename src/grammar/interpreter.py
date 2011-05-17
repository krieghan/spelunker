from action import Action
from exception import CouldNotInterpret


class Interpreter(object):
    
    def __init__(self,
                 dictionary,
                 thesaurus,
                 multiWordTokens):
        self.dictionary = dictionary
        self.verbs = dictionary.get('verbs')
        self.nouns = dictionary.get('nouns') + dictionary.get('names')
        self.prepositions = dictionary.get('prepositions')
        self.articles = dictionary.get('articles')
        self.directions = dictionary.get('directions')
        self.thesaurus = thesaurus
        self.multiWordTokens = [x.lower() for x in multiWordTokens]
        
    def evaluate(self, text):
        text = text.lower()
        for token in self.multiWordTokens:
            if token in text:
                tokenWithUnderscores = token.replace(' ', '_')
                text = text.replace(token, tokenWithUnderscores)
        
        words = text.split(' ')
        words = [x.replace('_', ' ') for x in words]
        
        reducedWords = [x for x in words if not self.exclude(x)]
        simplifiedWords = [self.simplify(x) for x in reducedWords]
        structure = self.getStructure(simplifiedWords)
        
        actions = []
        
        if self.determineMatch(['direction'],
                               structure):
            actions.append(Action(verb='go',
                                  object=simplifiedWords[0]))
        if self.determineMatch(['verb', 'direction'],
                               structure):
            actions.append(Action(verb=simplifiedWords[0],
                                  object=simplifiedWords[1]))
        if self.determineMatch(['verb'], structure):
            actions.append(Action(verb=simplifiedWords[0]))
        if self.determineMatch(['verb', 'preposition', 'noun'],
                               structure):
            actions.append(Action(verb=simplifiedWords[0],
                                  preposition=simplifiedWords[1],
                                  object=simplifiedWords[2]))
        if self.determineMatch(['verb', 'noun'],
                               structure):
            actions.append(Action(verb=simplifiedWords[0],
                                  object=simplifiedWords[1]))
        if self.determineMatch(['noun'],
                               structure):
            actions.append(Action(verb=None,
                                  object=simplifiedWords[0]))
        if self.determineMatch(['verb', 'noun', 'preposition'],
                               structure):
            actions.append(Action(verb=simplifiedWords[0],
                                  object=simplifiedWords[1],
                                  preposition=simplifiedWords[2]))
        if self.determineMatch(['verb', 'noun', 'preposition', 'noun'],
                               structure):
            actions.append(Action(verb=simplifiedWords[0],
                                  object=simplifiedWords[1],
                                  preposition=simplifiedWords[2],
                                  indirectObject=simplifiedWords[3]))
        if self.determineMatch(['verb', 'preposition', 'noun', 'preposition', 'noun'],
                               structure):
            actions.append(Action(verb=simplifiedWords[0],
                                  object=simplifiedWords[2],
                                  preposition=simplifiedWords[3],
                                  indirectObject=simplifiedWords[4]))
        if self.determineMatch(['verb', 
                                'noun', 
                                'preposition', 
                                'noun', 
                                'preposition',
                                'noun'],
                               structure):
            actions.append(
               Action(verb=simplifiedWords[0],
                      object=simplifiedWords[1],
                      preposition=simplifiedWords[2],
                      indirectObject=simplifiedWords[3],
                      indirectObjectPhrase=\
                        {simplifiedWords[4] : simplifiedWords[5]})
                      )
        if self.determineMatch(['verb',
                                'noun',
                                'noun'],
                               structure):
            actions.append(Action(verb=simplifiedWords[0],
                                  object=simplifiedWords[2],
                                  indirectObject=simplifiedWords[1]))
            
        if len(actions) > 1:
            raise CouldNotInterpret('I identified more than one way to interpret that command.')
        if len(actions) == 0:
            raise CouldNotInterpret('I do not know what to do with the structure %s' % structure)
        if len(actions) == 1:
            action = actions[0]
        return action
    
    def getPartsOfSpeech(self, word):
        parts = []
        if word in self.verbs:
            parts.append('verb')
        if word in self.nouns:
            parts.append('noun')
        if word in self.directions:
            parts.append('direction')
        if word in self.prepositions:
            parts.append('preposition')
        
        if not parts:
            raise CouldNotInterpret('I did not understand "%s"' % word)
        else:
            return parts
        
    def getStructure(self, words):
        possibilities = [self.getPartsOfSpeech(x) for x in words]
        return possibilities
        
    def determineMatch(self,
                       concreteStructure,
                       possibilities):
        if len(concreteStructure) != len(possibilities):
            return False
        for index in range(len(concreteStructure)):
            partOfSpeech = concreteStructure[index]
            possiblePartsOfSpeech = possibilities[index]
            if partOfSpeech not in possiblePartsOfSpeech:
                return False
        return True
            
        
    def simplify(self, word):
        for synonymSet in self.thesaurus:
            if word in synonymSet:
                return synonymSet[0]
        return word
    
    def exclude(self, word):
        if word in self.articles:
            return True
        
        return False