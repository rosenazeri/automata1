class NFA:
    def __init__(self):
        self.states = set()
        self.transitions = {}
        self.start = ""
        self.final_states = set()
        self.alphabet = set()

    def add_transition(self, state, symbol, next_state):
        self.transitions.setdefault((state, symbol), []).append(next_state)

    def get_state_transitions(self, state):
        ans = {}
        for (s, symbol) in self.transitions.keys():
            if s == state:
                ans.setdefault(symbol, self.transitions.get((s, symbol)))
        return ans

epsilon = "Îµ"

def grammar_to_nfa(grammar):
    nfa = NFA()
    nfa.start = grammar.start
    nfa.states = grammar.variables.copy()
    nfa.alphabet = grammar.alphabet.copy()
    for left, right in grammar.rules.items(): 
        
        for r in right:

            if r == epsilon:
                nfa.final_states.add(left)
            elif r[-1] in grammar.alphabet:  
                new_state = "F"
                nfa.states.add(new_state)
                nfa.add_transition(left, r, new_state)
                nfa.final_states.add(new_state)

            else:
                nfa.add_transition(left, r[0], r[1])
    
    return nfa

