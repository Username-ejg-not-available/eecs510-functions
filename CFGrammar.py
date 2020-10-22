

class CFG:
    def __init__(self,N,sig,P,S):
        self.nonterminal = N
        self.terminal = sig
        self.productions = P
        self.start = S

    def accepted(self,word,curr=None):
        if curr == None:
            curr = self.start

        for letter in range(len(curr)):
            if curr[letter] in self.nonterminal:
                break
            elif letter > len(word) - 1:
                return False
            elif word[letter] != curr[letter]:
                return False
        else:
            return word == curr

        found = False
        for letter in curr:
            if letter in self.nonterminal and not found:
                for sub in self.produce(letter):
                    found = self.accepted(word,curr.replace(letter, sub, 1))
                    if found:
                        break
        return found

    def produce(self,nonterm):
        return self.productions[self._symbol_to_index(nonterm)]

    def _symbol_to_index(self,symbol):
        for s in range(len(self.nonterminal)):
            if self.nonterminal[s] == symbol:
                return s
        for s in range(len(self.terminal)):
            if self.terminal[s] == symbol:
                return s
        print("Symbol not in grammar 4head")