# eecs510-functions
Don't want to do the calculations? Boy do I have news for you.

## How to Use:  
Open python interpreter in same directory.  
import the correct document/functions.  
(eg `from Automata import *`)  
Get free answers.  

## Table of Sadness
* [Automata](#Automata)
* [Combinations and Permutations](#CandP)
* [CFGrammar](#CFG)
* [Turing](#Turing)

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
* concatNFA(nfa1,nfa2)  
Creates an NFA that accepts the concatenation of the 2 inputs. Not tested with DFAs but should theoretically work  
`concatNFA(dfa1,dfa2)`  
* regex(dfa)
Creates a regex line for the DFA. Often cancerous. Cannot promise it works but I think it does  
`regex(dfa)`

### CreateNFA
To create an NFA:
* Create transition function:  
Unlike DFAs, NFAs can have multiple or even no transitions for a specific state letter combo.  
To show no transitions, write `None`  
To show multiple, write them as a list  
IMPORTANT: NFAs support epsilon-transitions, which means epsilon must be included as the last column in delta whether you are using it or not.
This example is problem 1 from HW2 for my class  
`delta = [ [[0,1], 0, None], [2, None, None], [3, None, None], [None, None, None] ]`    
* Call NFA constructor  
The parameters are the same as DFAs.    
`nfa = NFA(0,delta,[3])`  

### FunctionsNFA
Various NFA functions:
* setSigma(list)  
Same as DFA, except to accommodate for the fact that epsilon is technically in sigma, you must also include "\n", which represents epsilon.  
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
`dfa = nfa.toDFA()`  
* revNFA(nfa)  
Creates an NFA that accepts words from nfa in reverse  
`nfa2 = revNFA(nfa)`  
* concatNFA(nfa1,nfa2)  
Same as DFA. Do not know if it works with 1 DFA and 1 NFA or 2 DFAs. Will work for 2 NFAs I think  
`concatNFA(nfa1,nfa2)`

## CFG  
* [CFG Creation](#CreateCFG)  
* [CFG functions](#FunctionsCFG)  

### CreateCFG  
To create CFG:  
* Create productions:  
Too lazy to parse the normal notation for productions, so instead I used the mystical power of 2d arrays  
Each row index corresponds to the nonterminal at the same index  
`P = [["aAb", "aBb"], ["","aa"]]`  
* Call constructor with other parameters  
`cfg = CFG(["A","B"],["a","b"],P,"A")`  

### FunctionsCFG  
* accepted(word)  
returns whether a word is accepted by the grammar  
NOTE: This function currently cannot handle productions with any form of left-recursion  
`cfg.accepted("ababbababababababbabbabbbabbababababababbababbababbababbabbabbabbababbaababa")`
* produce(letter)  
Takes a nonterminal and returns the list of its productions  

## Turing  
* [Machine Creation](#CreateTuring)  
* [Functions](#FunctionsTuring)  

### CreateTuring  
Let's just say that transition functions for Turing machines are like essays, so I wrote an example at the bottom of Turing.py, so that it wouldn't take up too much space here.  

### FunctionsTuring
* read(letter, state)  
It's exactly like delta from DFAs or NFAs, but it returns a 3tuple in the format (nextstate,letter,dir)  
The way I wrote this function allows for shorthands for accept/reject transitions, as seen in the example  
`tur.read('0',2)`  
* accept(word)  
Put in a word, it'll show you step by step the computation and whether that word is part of the set  
`tur.accept("10010")`  

## CandP
Not useful for class rn so not writing this yet
