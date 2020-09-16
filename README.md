# eecs510-functions
Don't want to do the calculations? Boy do I have news for you.

## Table of Sadness
* [Automata](#Automata)
* [Combinations and Permutations](#CandP)

## Automata
* [Automata Variables](#AutomataVariables)  
* [DFA Creation](#CreateDFA)  
* [DFA functions](#FunctionsDFA)  
* [NFA Creation](#CreateNFA)  
* [NFA functions](#FunctionsNFA)  

### AutomataVariables
* `deltaT`  
This is the delta function you put in. Print this after NFA.toDFA() or the productDFA function to see the new transition function  
* `finStates`  
List of states that words will be accepted from
* `startState`  
It's the start state
* `showSteps`  
boolean value. If set to True, certain functions from NFA and DFA will print what they are doing in case you need to show work or something
* `sigma`  
List of the alphabet used by the automaton.

### CreateDFA
To create an DFA:
* Create a transition function:  
`delta = [[0,1],  
          [1,0]]`  
The rows are the states, the columns are the inputs. There is no limit to how many of each.  
* Call DFA constructor  
Parameters are (Start state, delta, list of final states [as they are indexed in delta)])  
`dfa = DFA(0,delta,[1])`  
This DFA determines if there is an even number of 1s  

### FunctionsDFA
There are various functions you can use with a DFA:
* setSigma(list)  
Imagine the problem gives you sigma = {a,b}. What person wants to have to use their brain to transform that to {0,1} to use with the function?  
`dfa.setSigma(["a","b"])`  
As long as sigma is the same length as it was, you can change it to anything.  
Using letters in the other functions that are not in sigma will cause other functions to give errors.
* delta(letter, current state [optional parameter, defaults to start state])  
Just put the next letter (as a string), and the state you are starting in (as a number, as indexed in delta)  
Compatible with `showSteps`, will print the transistions (by proxy, deltaHat and acceptedWord are also compatible)  
`dfa.delta("a",0)`  
* deltaHat(word)  
Starting from the start state, calls delta() a whole bunch until it reaches the end of the word. Returns the last state it's in  
`dfa.deltaHat("aaabababababbababababbababababababba")`
* acceptedWord(word)  
Returns if the input is in the list of final states  
`dfa.acceptedWord("ababbabababa")`  
* productDFA(type, DFAObject1, DFAObject2)  
This function returns the complement of a DFA, or the union or intersection of 2 DFAs.  
If doing complement, leave 3rd parameter blank  
`productDFA('c', dfa)`  
To do union ('u') or intersection ('i'), use appropriate type character and 2 dfa objects  
`productDFA('u',dfa1,dfa2)`
* toNFA()  
Creates an NFA object with the same parameters. Kinda dumb since it's basically identical.  

### CreateNFA
To create an NFA:
* Create transition function:  
Unlike DFAs, NFAs can have multiple or even no transitions for a specific state letter combo.  
To show no transitions, write `None`  
To show multiple, write them as a list  
IMPORTANT: NFAs support epsilon-transisions, which means epsilon must be included as the last column in delta whether you are using it or not.
This example is problem 1 from HW2 for my class  
`delta = [ [[0,1], 0, None], [2, None, None], [3, None, None], [None, None, None] ]`    
* Call NFA constructor  
The parameters are the same as DFAs. There is currently no support for multiple start states or epsilon-transitions as we haven't done them yet  
`nfa = NFA(0,delta,[3])`  

### FunctionsNFA
Various NFA functions:
* setSigma(list)  
Same as DFA, except to accomadate for the fact that epsilon is technically in sigma, you must also include "\n", which represents epsilon.
`nfa.setSigma(["a","b", "\n"])`  
* DELTA(letter, current state [optional parameter, defaults to start state])  
Same as dfa, returns list if there are multiple transistions, None if there are none  
`nfa.DELTA("a",0)`  
* DELTAHat(word)
Returns list of possible end states for the given word  
`nfa.DELTAHat("aababababaab")`
* acceptedWord(word)
Returns if any of the end states given by DELTAHat are final states  
`nfa.acceptedWord("ababababbaba")`  
* toDFA()  
Creates a DFA that does the same thing as the NFA using subset construction.  
Compatible with `showSteps`, and printing out the variables of the resulting object is recommended  
`dfa = nfa.toDFA()`  

## CandP
Not useful for class rn so not writing this yet
