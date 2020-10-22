from Graph import DirGraph
from Graph import Graph
from Util import bSort
from copy import deepcopy

class Automata:
	#ststate is startState index, delta is transition matrix, finalStates are a list of final states
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
		#convert the letter from the alphabet into an index for deltaT
		for x in range(len(self.sigma)):
			if self.sigma[x] == letter:
				letter = x
				break
		else:
			#have stroke if letter isnt in alphabet
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

	#converts to directed graph, loses input values, not useful but what the heck
	def convertToDirGraph(self):
		gr = DirGraph(len(self.deltaT))
		for q in range(len(self.deltaT)):
			for l in range(len(self.deltaT[q])):
				gr.add([q, self.deltaT[q][l]])
		return gr

	#converts to directed graph, loses input values, not useful
	def convertToGraph(self):
		gr = Graph(len(self.deltaT))
		for q in range(len(self.deltaT)):
			for l in range(len(self.deltaT[q])):
				gr.add([q, self.deltaT[q][l]])
		return gr
	
	#converts to NFA object, even though it doesn't actually add any nondeterminism
	def toNFA(self):
		nfa = NFA(self.startState,self.deltaT,self.finStates)
		nfa.setSigma(self.sigma)
		return nfa

class NFA(Automata):
	def __init__(self, ststate, transFunc, finStates):
		super().__init__(ststate,transFunc,finStates)
		self.sigma[len(self.sigma) - 1] = "\n"

	#returns next state, even if it's a list of states or None
	def DELTA(self,letter,ststate = -1):
		if ststate == -1:
			ststate = self.startState
		#convert letter into index
		for x in range(len(self.sigma)):
			if self.sigma[x] == letter:
				letter = x
				break
		else:
			#die if letter not in alphabet
			print("Error: provided letter is not in the alphabet")
			return -1
		next = self.deltaT[ststate][letter]
		return next

	#follows all possible paths and returns a list of all the endstates
	def DELTAHat(self, word, currstate = -1, endstates = []):
		if currstate == -1:
			currstate = self.startState

		#check epsilon transitions
		eps = self.deltaT[currstate][len(self.sigma) - 1]
		if type(eps) is int:
			self.DELTAHat(word, eps)
		elif type(eps) is list:
			for x in eps:
				self.DELTAHat(word, x)

		#reached end of word, attempt to add state to our list
		if word == "":
			if currstate not in endstates:
				endstates.append(currstate)
			return endstates
		nextState = self.DELTA(word[0],currstate)
		#None means that this branch is invalid, can't follow it for entirety of the word
		if nextState == None:
			return endstates
		if type(nextState) is list:
			for x in nextState:
				self.DELTAHat(word[1:], x)
		else:
			self.DELTAHat(word[1:], nextState)
		return endstates

	#checks if there is a final state in the deltahat endstates
	def acceptedWord(self,word):
		for x in self.DELTAHat(word):
			if x in self.finStates:
				return True
		return False

	#gets epsilon closure for a state
	def epsClosure(self,state,endstates=None):
		if endstates == None:
			endstates = []
		if state not in endstates:
			endstates.append(state)
		next = self.deltaT[state][len(self.sigma) - 1]
		if type(next) is int:
			self.epsClosure(next,endstates)
		elif type(next) is list:
			for x in next:
				self.epsClosure(x,endstates)
		return endstates

	def toDFA(self):
		newQ = []
		newDelta = []
		newF = []

		#generates delta matrix and list of states for other calculations
		[newQ,newDelta] = self._toDFAHelp(self.startState)

		#add st to newF if intersection of st and self.finstates is not empty
		for st in range(len(newQ)):
			for fst in self.finStates:
				if fst in newQ[st]:
					newF.append(st)

		#transliterates newDelta to not be butt ugly
		for st in range(len(newQ)):
			for dst in range(len(newDelta)):
				for dst2 in range(len(newDelta[dst])):
					if newDelta[dst][dst2] == newQ[st]:
						newDelta[dst][dst2] = st
		
		dfa = DFA(0,newDelta,newF)
		dfa.setSigma(self.sigma[:len(self.sigma) - 1])
		return dfa

	def _toDFAHelp(self,state,Q=None,D=None):
		if Q == None and D == None:
			Q = []
			D = []
		stateIndex = len(Q)
		#attempt to add new state to statelist, or gtfo if it already there
		if type(state) is int:
			ep = self.epsClosure(state)
			if ep not in Q:
				Q.append(bSort(ep, len(ep)))
			else:
				return [Q,D]
		elif type(state) is list:
			if state not in Q:
				Q.append(bSort(state, len(state)))
			else:
				return [Q,D]

		D.append([])

		#for every letter (except epsilon), use fancy schmancy epsclosure to find transition,
		#then add it in the proper spot in D
		for letter in range(len(self.sigma) - 1):
			D[stateIndex].append([])
			for tempstate in Q[stateIndex]:
				tempEps = self.epsClosure(tempstate)
				for st in tempEps:
					de = self.DELTA(self.sigma[letter],st)
					if type(de) is int and de not in D[stateIndex][letter]:
						D[stateIndex][letter].append(de)
					elif type(de) is list:
						for x in de:
							if x not in D[stateIndex][letter]:
								D[stateIndex][letter].append(x)
			bSort(D[stateIndex][letter], len(D[stateIndex][letter]))
			#attempt to recurse to add possible new states
			if D[stateIndex][letter] not in Q:
				[Q,D] = self._toDFAHelp(D[stateIndex][letter], Q, D)
		return [Q,D]
		

		

		


#type: ('u' = union, 'i' = intersection, 'c' = complement)
#if using complement function, only include the dfa1 parameter
#returns a DFA object that is the correct product of the inputs or false if inputs are bad
def productDFA(type, dfa1, dfa2 = DFA(0,[[]],[])):
	#check for incompatible inputs
	if (dfa2.deltaT != [[]] and type == 'c'):
		return False
	if (dfa1.sigma != dfa2.sigma and type != 'c'):
		return False
	#in complement, everything stays the same except finStates are inverted
	if (type == 'c'):
		result = DFA(dfa1.startState, dfa1.deltaT, dfa1.finStates)
		result.setSigma(dfa1.sigma)
		newFStates = []
		for x in range(len(result.deltaT)):
			if x not in result.finStates:
				newFStates.append(x)
		if dfa1.showSteps:
			print("Just reversed final states lmao")
		result.finStates = newFStates
		return result
	#create list of states
	Q = []
	if dfa.showSteps or dfa2.showSteps:
		print("Create list of states:")
	for x in range(len(dfa1.deltaT)):
		for y in range(len(dfa2.deltaT)):
			if dfa1.showSteps or dfa2.showSteps:
				print([x,y])
			Q.append([x,y])
	tablestr = ""
	for letter in dfa1.sigma:
		tablestr += "          " + letter
	if dfa1.showSteps or dfa2.showSteps:
		print("\nDetermine transitions for new dfa by checking the transitions of individual dfas with their current state and letter:\nQ" + tablestr)
	delta = [[] for column in range(len(Q))]
	for q in range(len(Q)):
		astr = str(Q[q])
		for letter in dfa1.sigma:
			newLoc = [dfa1.delta(letter, Q[q][0]), dfa2.delta(letter, Q[q][1])]
			for qnum in range(len(Q)):
				if newLoc == Q[qnum]:
					astr += "     " + str(newLoc)
					delta[q].append(qnum)
					break
		if dfa1.showSteps or dfa2.showSteps:
			print(astr)
	
	ststate = [dfa1.startState, dfa2.startState]
	if dfa1.showSteps or dfa2.showSteps:
		print("\nNew Start State = [dfa1 start state, dfa2 start state]:")
		print(ststate + "\n")
		
	for q in range(len(Q)):
		if ststate == Q[q]:
			ststate = q
			break
	result = DFA(ststate,delta,[])
	result.setSigma(dfa1.sigma)
	
	if (type == 'u'):
		if dfa1.showSteps or dfa2.showSteps:
			print("Final States are those states that are in dfa1s OR dfa2s final states\n")
		for q in range(len(Q)):
			if Q[q][0] in dfa1.finStates or Q[q][1] in dfa2.finStates:
				result.finStates.append(q)
	else:
		if dfa1.showSteps or dfa2.showSteps:
			print("Final States are those states that are in dfa1s AND dfa2s final states\n")
		for q in range(len(Q)):
			if Q[q][0] in dfa1.finStates and Q[q][1] in dfa2.finStates:
				result.finStates.append(q)
	return result

def concatNFA(nfa1,nfa2):
	delta = deepcopy(nfa1.deltaT).append(deepcopy(nfa2.deltaT))
	stst = nfa.startState
	finst = nfa2.finStates
	
	if type(delta[len(nfa.deltaT) - 1][len(nfa1.sigma) - 1]) is None:
		delta[len(nfa1.deltaT) - 1][len(nfa1.sigma) - 1] = nfa2.startState
	elif type(delta[len(nfa.deltaT) - 1][len(nfa1.sigma) - 1]) is int:
		delta[len(nfa1.deltaT) - 1][len(nfa1.sigma) - 1] = [delta[len(nfa1.deltaT) - 1][len(nfa1.sigma) - 1], nfa1.startState]
	else:
		delta[len(nfa1.deltaT) - 1][len(nfa1.sigma) - 1].append(nfa2.startState)

	newnfa = NFA(stst,delta,finst)
	newnfa.setSigma(nfa1.sigma)
	return newnfa

#helper function for NFA.toDFA(), creates the subsets for construction
def statePermutations(length, out = "", perms = [], exit = 0):
	#this exists so I could pass in the number of states and it would create a string to make permutations with
	if type(length) is int:
		exit = pow(2, length)
		temp = ""
		for x in range(length):
			temp += str(x)
		length = temp
	#no more permutations to make in this recursion
	if length == "":
		return
	#creates permutations with current 'out' as a base string, only adds new combinations to perms
	for x in range(len(length)):
		out += length[x]
		temp = [int(char) for char in out]
		if bSort(temp, len(temp)) not in perms:
			perms.append(temp)
		out = out[:len(out) - 1]
		if len(perms) == exit:
			return perms
	#creates new base string and attempts more permutations
	for x in range(len(length)):
		out += length[x]
		statePermutations(length[:x] + length[x+1:], out, perms,exit)
		out = out[:len(out) - 1]
	return perms

#helper function for NFA.toDFA(), determines which states are actually used
def findVisitedStates(Q,delta,currstate,visited = []):
	#we're here, we're visiting, add this place to visited
	if currstate not in visited:
		if type(currstate) is int:
			visited.append([currstate])
		else:
			visited.append(currstate)
	#goes through possible paths from this state, adds them to visited if they're not already there
	#eventually won't be able to add any new destinations, which is how this function actually stops
	csIndex = 0
	for y in range(len(Q)):
		if currstate == Q[y] or [currstate] == Q[y]:
			csIndex = y
			break
	for x in range(len(delta[0])):
		if delta[csIndex][x] not in visited:
			findVisitedStates(Q,delta,delta[csIndex][x], visited)
	return visited

#if nfa accepts w, this returns nfa that accepts w^R
def revNFA(nfa):
	finalState = [nfa.startState]
	delta = [[[] for column in range(len(nfa.sigma))] for column in range(len(nfa.deltaT))]
	for x in range(len(nfa.deltaT)):
		for y in range(len(nfa.sigma)):
			state = nfa.deltaT[x][y]
			if type(state) is int:
				delta[state][y].append(x)
			elif type(state) is list:
				for z in state:
					delta[z][y].append(x)
	for x in range(len(nfa.deltaT)):
		for y in range(len(nfa.sigma)):
			if delta[x][y] == []:
				delta[x][y] = None
			elif len(delta[x][y]) == 1:
				delta[x][y] = delta[x][y][0]
	delta.append([None for column in range(len(nfa.sigma))])
	startState = len(delta) - 1
	if len(nfa.finStates) == 1:
		delta[startState][len(nfa.sigma) - 1] = nfa.finStates[0]
	else:
		delta[startState][len(nfa.sigma) - 1] = nfa.finStates
	nfa2 = NFA(startState, delta, finalState)
	nfa2.setSigma(nfa.sigma)
	return nfa2

def regex(dfa):
	#in order by state number, then loops, outgoing,incoming, then [letter, state] for the latter 2
	#ex: connTable[0] = [ [ 'a' ], [ 'b', 2 ], ['a', 2] ]
	connTable = [["",[],[]] for x in range(len(dfa.deltaT))]
	for x in range(len(dfa.deltaT)):
		for y in range(len(dfa.sigma)):
			if dfa.deltaT[x][y] == x:
				if len(connTable[x][0]):
					connTable[x][0] += " + " + dfa.sigma[y]
				else:
					connTable[x][0] = dfa.sigma[y]
			else:
				connTable[x][1].append([dfa.sigma[y],dfa.deltaT[x][y]]) #add state to outgoing
				connTable[dfa.deltaT[x][y]][2].append([dfa.sigma[y],x]) #add x to incoming of delta[x][y]
	stateCount = len(connTable)
	for x in range(len(connTable)):
		if x not in dfa.finStates and x != dfa.startState:
			elimState(connTable, x)
			if dfa.showSteps:
				print("Removing state " + str(x) + ":\n[Loop, [connections leaving the state], [connections coming in]]\n")
				for y in connTable:
					if y != ["",[],[]]:
						print(y)
				print("")
			stateCount -= 1
	for x in range(len(connTable)):
		if x == dfa.startState and stateCount > 1:
			elimState(connTable, x, dfa.startState not in dfa.finStates)
			if dfa.showSteps:
				print("Removing state " + str(x) + ":\n[Loop, [connections leaving the state], [connections coming in]]\n")
				for y in connTable:
					if y != ["",[],[]]:
						print(y)
				print("")
	for x in connTable:
		if x != ["",[],[]]:
			if dfa.startState in dfa.finStates:
				return "(" + x[0] + ")*"
			else:
				return x[0]

def elimState(connTable, state, changeStartState=False):
	#adds paths between adj states if there is a path to be made
	for incom in connTable[state][2]:
		for outgo in connTable[state][1]:
			if incom[1] == outgo[1]:
				continue
			word = ""
			for z in connTable[incom[1]][1]:
				if z[1] == outgo[1]:
					word += z[0] + " + "
					connTable[incom[1]][1].remove(z)
					connTable[outgo[1]][2].remove([z[0], incom[1]])
					break

			word += incom[0]
			if len(connTable[state][0]):
				if len(connTable[state][0]) > 1 or '+' in connTable[state][0]:
					word += "(" + connTable[state][0] + ")*"
				else:
					word += connTable[state][0] + "*"
			word += outgo[0]
			#add new connection
			connTable[incom[1]][1].append([word,outgo[1]])
			connTable[outgo[1]][2].append([word,incom[1]])

	#adds loops to adjacent states if there is a 2 way connection
	for outgoingState in connTable[state][1]:  
		word = ""
		if not changeStartState:
			#current loop on adjacent + (incoming letter * loop on removed * outgoing letter)
			if len(connTable[outgoingState[1]][0]):
				word += connTable[outgoingState[1]][0] + " + "
			incomingState = []
			for x in connTable[state][2]:
				if x[1] == outgoingState[1]:
					incomingState = x
					break
			word += incomingState[0]
			if len(connTable[state][0]):
				if len(connTable[state][0]) > 1 or '+' in connTable[state][0][0]:
					word += "(" + connTable[state][0] + ")*"
				else:
					word += connTable[state][0] + "*"
			word += outgoingState[0]
		else:
			#loop on remove Node * transition to adj node
			lastState = connTable[state][1][0][1]
			loop1 = ""
			loop2 = ""
			if len(connTable[state][0]):
				if len(connTable[state][0]) > 1 or '+' in connTable[state][0][0]:
					loop1 = "(" + connTable[state][0] + ")*"
				else:
					loop1 = connTable[state][0] + "*"
			word += loop1 + connTable[state][1][0][0]
			if len(connTable[lastState][0]):
				if len(connTable[lastState][0]) > 1 or '+' in connTable[lastState][0][0]:
					loop2 = "(" + connTable[lastState][0] + ")*"
				else:
					loop2 = connTable[lastState][0] + "*"
			if len(connTable[lastState][1]):
				word += loop2 + "(" + connTable[lastState][1][0][0] + loop1 + connTable[state][1][0][0] + loop2 + ")*"
			else:
				word += loop2

		connTable[outgoingState[1]][0] = word

	for x in range(len(connTable)):
		connTable[x][1] = list(filter(lambda y: y[1] != state,connTable[x][1]))
		connTable[x][2] = list(filter(lambda y: y[1] != state,connTable[x][2]))

	connTable[state] = ["",[],[]]
