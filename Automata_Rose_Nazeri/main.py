from parser import parse
from nfa import grammar_to_nfa
from dfa import nfa_to_dfa, specify_operation_on_dfa
from collections import deque

grammars = []
nfa_list = []
dfa_list = []
operation = ""

file = open("input.txt", 'r')
(grammars, operation) = parse(file)
file.close()

for grammar in grammars:
    nfa_list.append(grammar_to_nfa(grammar))

for nfa in nfa_list:
    dfa_list.append(nfa_to_dfa(nfa))

dfa_list = deque(dfa_list)

final_dfa = specify_operation_on_dfa(operation, dfa_list)

file = open("output_file.txt", "w")
file.write(str(final_dfa))
file.close()
