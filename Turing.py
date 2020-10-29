'''
| = left end marker
/ = blank
'''

class Turing:
    def __init__(self,gam,d,start):
        self.gamma = gam
        if '|' not in self.gamma:
            self.gamma.append('|')
        if '/' not in self.gamma:
            self.gamma.append('/')
        self.transFunc = d
        self.startState = start

    def read(self,letter,state):
        if letter not in self.gamma:
            return None
        if state == len(self.transFunc) or state == len(self.transFunc) + 1:
            return (state, letter, 'R')
        next = self.transFunc[state][self._symbol_to_index(letter)]
        #allows ref and acc aliases in transFunc
        if next == "rej":
            return (len(self.transFunc)+1,letter,'R')
        elif next == "acc":
            return (len(self.transFunc),letter,'R')
        else:
            return next

    def accept(self,word):
        if word == "" or word[0] != '|':
            word = '|' + word
        if word[len(word) - 1] != '/':
            word += '/'
        currPos = 1
        currState = self.startState
        while currState != len(self.transFunc) and currState != len(self.transFunc) + 1:
            self.printState(word,currPos,currState)
            next = self.read(word[currPos],currState)
            temp = list(word)
            temp[currPos] = next[1]
            word = ''.join(temp)
            currState = next[0]
            if next[2] == 'L':
                currPos -= 1
            else:
                currPos += 1
        self.printState(word,currPos,currState)
        return currState == len(self.transFunc)

    def _symbol_to_index(self,symbol):
        for s in range(len(self.gamma)):
            if self.gamma[s] == symbol:
                return s
        print("symbol not in alphabet dumbass")

    def printState(self,word,currPos,currState):
        print(word + " : " + str(currState))
        space = ""
        for x in range(currPos):
            space += " "
        print(space + "^\n")

'''
EX: accepts words of form w = x#x where x is in {0,1}*

d = [[(1,'x','R'), (2,'x','R'), (7,'#','R'), "rej",       (0,'|','R'), "ref"],
     [(1,'0','R'), (1,'1','R'), (3,'#','R'), "rej",       "rej",       "rej"],
     [(2,'0','R'), (2,'1','R'), (4,'#','R'), "rej",       "rej",       "rej"],
     [(5,'x','L'), "rej",       "rej",       (3,'x','R'), "rej",       "rej"],
     ["rej",       (5,'x','L'), "rej",       (4,'x','R'), "rej",       "rej"],
     [(5,'0','L'), (5,'1','L'), (6,'#','L'), (5,'x','L'), "rej",       "rej"],
     [(6,'0','L'), (6,'1','L'), "rej",       (0,'x','R'), "rej",       "rej"],
     ["rej",       "rej",       "rej",       (7,'x','R'), "rej",       "acc"],]
tur = Turing(['0','1','#','x'],d,0)
tur.accept("1000#1000") #True
'''