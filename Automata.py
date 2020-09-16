from Graph import DirGraph
from Graph import Graph
from Util import bSort

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
	def epsClosure(self,state,endstates=[]):
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
		useSubset = True
		for x in self.deltaT:
			if x[len(self.sigma) - 1] != None:
				useSubset = False
				break
		if useSubset:
			info = self.subsetConstruction()
		else:
			info = self.epsilonConstruction()

		#determining final states
		finalStates = []
		for x in range(len(info[0])):
			if type(info[0][x]) is int:
				if x in self.finStates:
					finalStates.append(x)
			else:
				for y in info[0][x]:
					if y in self.finStates:
						finalStates.append(x)
						break

		#transliterating delta
		for x in range(len(info[0])):
			for y in range(len(info[1])):
				for z in range(len(info[1][y])):
					if info[1][y][z] == info[0][x]:
						info[1][y][z] = x

		dfa = DFA(info[2],info[1],finalStates)
		dfa.setSigma(self.sigma[:len(self.sigma) - 1])
		return dfa

	#uses subset construction to convert nfa to a dfa that accepts the same words
	#showSteps might actually work for this, it'll just be long
	def subsetConstruction(self):
		#get subset list
		Q = statePermutations(len(self.deltaT), "", [])
		if self.showSteps:
			print("State Permutations:")
			for x in Q:
				print(x)
			print("")
		ststate = self.startState
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
		if self.showSteps:
			print("Transistion Function without Eliminated States:")
			for x in range(len(newDelta2)):
				spaces = "              "
				if type(newQ[x]) is not int:
					for y in range(len(str(newQ[x])) - 1):
						spaces = spaces[1:]
				print(str(newQ[x]) + spaces + str(newDelta2[x]))
			print("")
		return [newQ,newDelta2,ststate]

	def epsilonConstruction(self, currstate = -1, Q = [], delta = []):
		if currstate == -1:
			currstate = self.epsClosure(self.startState)
		if currstate not in Q:
			Q.append(currstate)
			delta.append([])
		else:
			return

		#determine index of currstate in Q
		currIndex = 0
		for x in range(len(Q)):
			if Q[x] == currstate:
				currIndex = x
				break

		for x in range(len(self.sigma) - 1):
			nextState = []
			for y in range(len(currstate)):
				next = self.DELTA(self.sigma[x],currstate[y])
				if type(next) is int:
					if next not in nextState:
						nextState.append(next)
				elif type(next) is list:
					for z in next:
						if z not in nextState:
							nextState.append(z)
			delta[currIndex].append(nextState)
			if self.showSteps:
				print("Mapped: q%s -> q%s for input \"%s\"" % (currstate,nextState,self.sigma[x]))
			self.epsilonConstruction(nextState,Q,delta)
		return [Q,delta,0]

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
