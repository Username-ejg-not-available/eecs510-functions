from Graph import DirGraph
from Graph import Graph
from Util import bSort

class Automata:
    def __init__(self,ststate,delta,finalstates):
        self.startState = ststate
        self.deltaT = delta
        self.finStates = finalstates
        self.showSteps = False
        self.sigma = []
        for n in range(len(self.deltaT[0])):
           self.sigma.append(str(n))

    #sets alphabet to new alphabet, must be same length as original
    #delta, deltaHat, and acceptedWord must be used with new alphabet
    def setSigma(self,newSigma):
        if len(self.sigma) != len(newSigma):
           return
        self.sigma = newSigma

class DFA(Automata):
    def __init__(self, ststate, transitionF, finalstates):
        super().__init__(ststate,transitionF,finalstates)

    #returns next state from ststate when given a certain letter
    #has stroke if letter is not in alphabet
    def delta(self, letter, ststate = -1):
        if (ststate == -1):
            ststate = self.startState
        for x in range(len(self.sigma)):
            if self.sigma[x] == letter:
                letter = x
                break
        else:
            print("Error: provided letter is not in the alphabet")
            return -1
        next = self.deltaT[ststate][letter]
        if self.showSteps:
            print("q%s -> q%s" % (ststate, next))
        return next

    #calls delta() for every letter in the word
    #goes from self.startState to wherever the word leads it
    def deltaHat(self, word):
        curr = self.startState
        for c in word:
            if curr == -1:
                return curr
            curr = self.delta(c,curr)
        return curr

    #checks if the word makes deltaHat end at a final state
    def acceptedWord(self, word):
        return self.deltaHat(word) in self.finStates

    #converts to directed graph, loses input values
    def convertToDirGraph(self):
        gr = DirGraph(len(self.deltaT))
        for q in range(len(self.deltaT)):
            for l in range(len(self.deltaT[q])):
                gr.add([q, self.deltaT[q][l]])
        return gr

    #converts to directed graph, loses input values
    def convertToGraph(self):
        gr = Graph(len(self.deltaT))
        for q in range(len(self.deltaT)):
            for l in range(len(self.deltaT[q])):
                gr.add([q, self.deltaT[q][l]])
        return gr

class NFA(Automata):
    def __init__(self, ststate, transFunc, finStates):
        super().__init__(ststate,transFunc,finStates)

    #returns next state, even if it's a list of states or None
    def DELTA(self,letter,ststate = -1):
        if ststate == -1:
            ststate = self.startState
        for x in range(len(self.sigma)):
            if self.sigma[x] == letter:
                letter = x
                break
        else:
            print("Error: provided letter is not in the alphabet")
            return -1
        return self.deltaT[ststate][letter]

    #follows all possible paths and returns a list of all the endstates
    def DELTAHat(self, word, currstate = -1, endstates = []):
        if currstate == -1:
            currstate = self.startState
        if word == "":
            if currstate not in endstates:
                endstates.append(currstate)
            return
        nextState = self.DELTA(word[0],currstate)
        if nextState == None:
            return
        if isinstance(nextState, list):
            for x in nextState:
                self.DELTAHat(word[1:], x)
        else:
            self.DELTAHat(word[1:], nextState)
        return endstates

    #checks if there is a final state in the deltahat endstates
    def acceptedWord(self,word):
        for x in self.DELTAHat(word):
            if x in self.finalStates:
                return True
        return False

    #uses subset construction to convert nfa to a dfa that accepts the same words
    def toDFA(self):
        Q = statePermutations(len(self.deltaT), "", [])
        ststate = self.startState
        finalStates = []
        newDelta = [[] for column in range(len(Q))]
        for x in range(len(newDelta)):
            for y in self.sigma:
                if (type(Q[x]) is list):
                    temp = []
                    for z in range(len(Q[x])):
                        temp2 = self.DELTA(y,int(Q[x][z]))
                        if type(temp2) is int:
                            temp.append(temp2)
                        elif type(temp2) is list:
                            for a in temp2:
                                temp.append(a)
                    if len(temp) == 1:
                        newDelta[x].append(temp[0])
                    else:
                        newDelta[x].append(temp)
                else:
                    if self.DELTA(y,Q[x]) == None:
                        newDelta[x].append([])
                    else:
                        newDelta[x].append(self.DELTA(y,Q[x]))

        #removing dud states
        newQ = removeExtraState(Q,newDelta,ststate)
        newDelta2 = []
        for x in range(len(Q)):
            if Q[x] in newQ:
                newDelta2.append(newDelta[x])
        Q = newQ
        #making finalstates
        for x in range(len(Q)):
            if type(Q[x]) is int:
                if x in self.finStates:
                    finalStates.append(x)
            else:
                for y in Q[x]:
                    if y in self.finStates:
                        finalStates.append(x)
                        break

        #transliterating delta
        for x in range(len(Q)):
            for y in range(len(newDelta2)):
                for z in range(len(newDelta2[y])):
                    if newDelta2[y][z] == Q[x]:
                        newDelta2[y][z] = x

        dfa = DFA(ststate, newDelta2, finalStates)
        dfa.setSigma(self.sigma)
        return dfa
            
        

#type: ('u' = union, 'i' = intersection, 'c' = complement)
#if using complement function, only include the dfa1 parameter
#returns a DFA object that is the correct product of the inputs
def productDFA(type, dfa1, dfa2 = DFA(0,[[]],[])):
    if (dfa2.deltaT != [[]] and type == 'c'):
        return False
    if (dfa1.sigma != dfa2.sigma and type != 'c'):
        return False
    if (type == 'c'):
        result = DFA(dfa1.startState, dfa1.deltaT, dfa1.finalStates)
        result.setSigma(dfa1.sigma)
        newFStates = []
        for x in range(len(result.deltaT)):
            if x not in result.finalStates:
                newFStates.append(x)
        result.finalStates = newFStates
        return result
    Q = []
    for x in range(len(dfa1.deltaT)):
        for y in range(len(dfa2.deltaT)):
            Q.append([x,y])
    delta = [[] for column in range(len(Q))]
    for q in range(len(Q)):
        for letter in dfa1.sigma:
            newLoc = [dfa1.delta(letter, Q[q][0]), dfa2.delta(letter, Q[q][1])]
            for qnum in range(len(Q)):
                if newLoc == Q[qnum]:
                    delta[q].append(qnum)
                    break
    ststate = [dfa1.startState, dfa2.startState]
    for q in range(len(Q)):
        if ststate == Q[q]:
            ststate = q
            break
    result = DFA(ststate,delta,[])
    result.setSigma(dfa1.sigma)
    if (type == 'u'):
        for q in range(len(Q)):
            if Q[q][0] in dfa1.finalStates or Q[q][1] in dfa2.finalStates:
                result.finalStates.append(q)
    else:
        for q in range(len(Q)):
            if Q[q][0] in dfa1.finalStates and Q[q][1] in dfa2.finalStates:
                result.finalStates.append(q)
    return result

def statePermutations(length, out = "", perms = []):
    if type(length) is int:
        temp = ""
        for x in range(length):
            temp += str(x)
        length = temp
    if length == "":
        return
    for x in range(len(length)):
        out += length[x]
        temp = [int(char) for char in out]
        if bSort(temp, len(temp)) not in perms:
            if len(temp) == 1:
                perms.append(temp[0])
            else:
                perms.append(temp)
        out = out[:len(out) - 1]
    for x in range(len(length)):
        out += length[x]
        statePermutations(length[:x] + length[x+1:], out, perms)
        out = out[:len(out) - 1]
    return perms

def removeExtraState(Q,delta,currstate,visited = []):
    if currstate not in visited:
        visited.append(currstate)
    csIndex = 0
    for x in range(len(delta[0])):
        for y in range(len(Q)):
            if currstate == Q[y]:
                csIndex = y
                break
        if delta[csIndex][x] not in visited:
            removeExtraState(Q,delta,delta[csIndex][x], visited)
    return visited
