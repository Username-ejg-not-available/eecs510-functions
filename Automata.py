from Graph import DirGraph
from Graph import Graph
from Util import bSort

"""
Examples:
#DFA
#rows are the different states, columns are the input letters
delta1 = [[0,1],
	  [1,0]]
#accepted words have even number of 1s
dfa1 = DFA(0,delta1,[1])
dfa1.acceptedWord("00101") returns true
dfa1.setSigma(["R","~"])
dfa1.acceptedWord("RRR~RR~~") returns false

#dfaCompl accepts words that have odd number of bs
dfaCompl = productDFA('c',dfa1)

delta2 = [[1,0],
	  [2,0],
	  [3,0],
	  [3,0]]
#accepts words that end with '000'
dfa2 = DFA(0,delta2,[3])
dfa2.setSigma(["R","~"])

#both dfas must have identical alphabet for productDFA
#i can be replaced with u, same delta, different final states
dfaProduct('i',dfa1,dfa2)

#NFA
#Nondeterminate transitions should be done as a list
#lack of transition should be None
#example is HW2 question 1
delta3 = [[ [0,1], 0],
	   [ 2, None ],
	   [ 3, None ]
	   [ 3, None ]]
	   
nfa = NFA(0,delta,[3])
nfa.setSigma(["a","b"])
dfaFromNfa = nfa.toDFA()
"""

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
		#no value specified means start state
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
		#reached end of word, attempt to add state to our list
		if word == "":
			if currstate not in endstates:
				endstates.append(currstate)
			return
		nextState = self.DELTA(word[0],currstate)
		#None means that this branch is invalid, can't follow it for entirety of the word
		if nextState == None:
			return
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

	#uses subset construction to convert nfa to a dfa that accepts the same words
	#showSteps might actually work for this, it'll just be long
	def toDFA(self):
		#get subset list
		Q = statePermutations(len(self.deltaT), "", [])
		if self.showSteps:
			print("State Permutations:")
			for x in Q:
				print(x)
			print("")
		ststate = self.startState
		finalStates = []
		newDelta = [[] for column in range(len(Q))]
		#get delta for all the subsets in Q
		for x in range(len(newDelta)):
			for y in self.sigma:
				temp = []
				for z in range(len(Q[x])):
					#sometimes states point to nondeterminate places, need to add all the options
					temp2 = self.DELTA(y,int(Q[x][z]))
					if type(temp2) is int:
						if temp2 not in temp:
							temp.append(temp2)
					elif type(temp2) is list:
						for a in temp2:
							if a not in temp:
								temp.append(a)
				newDelta[x].append(bSort(temp,len(temp)))

		if self.showSteps:
			print("Transistion Function for Q:\nQ              delta")
			for x in range(len(newDelta)):
				spaces = "              "
				if type(Q[x]) is not int:
					for y in range(len(str(Q[x])) - 1):
						spaces = spaces[1:]
				print(str(Q[x]) + spaces + str(newDelta[x]))
			print("")
		#removing dud states
		#get list of states that can actually be used
		newQ = findVisitedStates(Q,newDelta,ststate)
		if self.showSteps:
			print("Q, after removing states that can't be visited:")
			for x in newQ:
				print(x)
			print("")
		newDelta2 = []
		#get delta corresponding to usable functions
		for x in range(len(Q)):
			if Q[x] in newQ:
				newDelta2.append(newDelta[x])
		Q = newQ
		if self.showSteps:
			print("Transistion Function without Eliminated States:")
			for x in range(len(newDelta2)):
				spaces = "              "
				if type(Q[x]) is not int:
					for y in range(len(str(Q[x])) - 1):
						spaces = spaces[1:]
				print(str(Q[x]) + spaces + str(newDelta2[x]))
			print("")
		#making finalstates (any state that has an nfa's final state in it is a state)
		for x in range(len(Q)):
			if type(Q[x]) is int:
				if x in self.finStates:
					finalStates.append(x)
			else:
				for y in Q[x]:
					if y in self.finStates:
						finalStates.append(x)
						break

		#transliterating delta (changing it to not name its states after subsets but instead after indices)
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
#returns a DFA object that is the correct product of the inputs or false if inputs are bad
def productDFA(type, dfa1, dfa2 = DFA(0,[[]],[])):
	#check for incompatible inputs
	if (dfa2.deltaT != [[]] and type == 'c'):
		return False
	if (dfa1.sigma != dfa2.sigma and type != 'c'):
		return False
	#in complement, everything stays the same except finStates are inverted
	if (type == 'c'):
		result = DFA(dfa1.startState, dfa1.deltaT, dfa1.finalStates)
		result.setSigma(dfa1.sigma)
		newFStates = []
		for x in range(len(result.deltaT)):
			if x not in result.finalStates:
				newFStates.append(x)
		result.finalStates = newFStates
		return result
	#create list of states
	Q = []
	for x in range(len(dfa1.deltaT)):
		for y in range(len(dfa2.deltaT)):
			Q.append([x,y])
	#create transition function
	delta = [[] for column in range(len(Q))]
	for q in range(len(Q)):
		for letter in dfa1.sigma:
			newLoc = [dfa1.delta(letter, Q[q][0]), dfa2.delta(letter, Q[q][1])]
			for qnum in range(len(Q)):
				if newLoc == Q[qnum]:
					delta[q].append(qnum)
					break
	#get start state
	ststate = [dfa1.startState, dfa2.startState]
	for q in range(len(Q)):
		if ststate == Q[q]:
			ststate = q
			break
	result = DFA(ststate,delta,[])
	result.setSigma(dfa1.sigma)
	#obvious differentiation between union and intersection is obvious
	if (type == 'u'):
		for q in range(len(Q)):
			if Q[q][0] in dfa1.finalStates or Q[q][1] in dfa2.finalStates:
				result.finalStates.append(q)
	else:
		for q in range(len(Q)):
			if Q[q][0] in dfa1.finalStates and Q[q][1] in dfa2.finalStates:
				result.finalStates.append(q)
	return result

#helper function for NFA.toDFA(), creates the subsets for construction
def statePermutations(length, out = "", perms = []):
	#this exists so I could pass in the number of states and it would create a string to make permutations with
	if type(length) is int:
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
	#creates new base string and attempts more permutations
	for x in range(len(length)):
		out += length[x]
		statePermutations(length[:x] + length[x+1:], out, perms)
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
	for x in range(len(delta[0])):
		for y in range(len(Q)):
			if currstate == Q[y]:
				csIndex = y
				break
		if delta[csIndex][x] not in visited:
			findVisitedStates(Q,delta,delta[csIndex][x], visited)
	return visited
