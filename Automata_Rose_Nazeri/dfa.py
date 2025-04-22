from collections import deque


class DFA:
    def __init__(self):
        self.states = set()
        self.transitions = {}
        self.start = ""
        self.final_states = set()
        self.alphabet = set()

    def __str__(self):
        s = "# States\n"
        s += " ".join(map(str, self.states))
        s += "\n# Alphabet\n"
        s += " ".join(map(str, self.alphabet))
        s += "\n# Start State\n"
        s += self.start
        s += "\n# Final States\n"
        s += " ".join(map(str, self.final_states))
        s += "\n# Transitions\n"

        for ((state, symbol), next_state) in self.transitions.items():
            s += f"{state} {symbol} {next_state}\n"

        return s

    def add_transition(self, state, symbol, next_state):
        self.transitions.setdefault((state, symbol), next_state)


def nfa_to_dfa(nfa):
    dfa = DFA()
    dfa.start = "Q0"
    dfa.alphabet = nfa.alphabet
    state_names = {}
    state_num = 1

    queue = deque()
    queue.append(frozenset(nfa.start))
    state_names.setdefault(frozenset(nfa.start), "Q0")
    checked = set()

    while queue:

        states_set = queue.popleft()
        checked.add(states_set)
        transitions = {}

        for s in states_set:
            temp_transitions = nfa.get_state_transitions(s)
            for symbol, next_states in temp_transitions.items():
                transitions.setdefault(symbol, set()).update(next_states)
        for (symbol, next_states) in transitions.items():
            next_states = frozenset(next_states)
            state_names.setdefault(next_states, f"Q{state_num}")
            if state_names.get(next_states) == f"Q{state_num}":
                state_num += 1
            dfa.add_transition(state_names.get(states_set), symbol, state_names.get(next_states))
            if next_states not in checked:
                queue.append(next_states)
            dfa.transitions.setdefault((state_names.get(states_set), symbol), state_names.get(next_states))

    dfa.states.update(state_names.values())

    flag = False
    for state in dfa.states:
        for symbol in dfa.alphabet:
            if (state, symbol) not in dfa.transitions.keys():
                dfa.transitions.setdefault((state, symbol), "N")
                flag = True

    if flag:
        dfa.states.add("N")
        for symbol in dfa.alphabet:
            dfa.add_transition("N", symbol, "N")

    for (dfa_states, name) in state_names.items():
        for acc in nfa.final_states:
            if acc in dfa_states:
                dfa.final_states.add(name)

    return dfa


def complement(dfa):
    dfa_complement = DFA()
    dfa_complement.final_states = dfa.states.copy().difference(dfa.final_states)
    dfa_complement.states = dfa.states.copy()
    dfa_complement.alphabet = dfa.alphabet.copy()
    dfa_complement.states = dfa.states.copy()
    dfa_complement.transitions = dfa.transitions.copy()
    dfa_complement.start = dfa.start
    return dfa_complement


def union(dfa1, dfa2):
    dfa = DFA()
    dfa.alphabet = dfa1.alphabet.copy()
    start_state = (dfa1.start, dfa2.start)
    dfa.start = "Q0"

    states_queue = deque([start_state])
    checked = set()
    state_mapping = {start_state: "Q0"}
    dfa.states.add("Q0")
    
    state_count = 1

    while states_queue:
        (s1, s2) = states_queue.popleft()
        checked.add((s1, s2))
        current_state_name = state_mapping[(s1, s2)]
        for symbol in dfa.alphabet:
            next_s1 = dfa1.transitions.get((s1, symbol))
            next_s2 = dfa2.transitions.get((s2, symbol))
            next_state = (next_s1, next_s2)

            if next_state not in state_mapping and next_state not in checked:
                new_state_name = f"Q{state_count}"
                state_mapping[next_state] = new_state_name
                state_count += 1
                dfa.states.add(new_state_name)
                states_queue.append(next_state)

            dfa.add_transition(current_state_name, symbol, state_mapping[next_state])
        if s1 in dfa1.final_states or s2 in dfa2.final_states:
            dfa.final_states.add(current_state_name)

    return dfa


def intersection(dfa1, dfa2):
    dfa = DFA()
    dfa.alphabet = dfa1.alphabet.copy()
    start_state = (dfa1.start, dfa2.start)
    dfa.start = "Q0"

    states_queue = deque([start_state])
    checked = set()
    state_mapping = {start_state: "Q0"}
    dfa.states.add("Q0")
    
    state_count = 1

    while states_queue:
        (s1, s2) = states_queue.popleft()
        checked.add((s1, s2))
        current_state_name = state_mapping[(s1, s2)]

        for symbol in dfa.alphabet:
            next_s1 = dfa1.transitions.get((s1, symbol))
            next_s2 = dfa2.transitions.get((s2, symbol))
            next_state = (next_s1, next_s2)

            if next_state not in state_mapping and next_state not in checked:
                new_state_name = f"Q{state_count}"
                state_mapping[next_state] = new_state_name
                state_count += 1
                dfa.states.add(new_state_name)
                states_queue.append(next_state)

            dfa.add_transition(current_state_name, symbol, state_mapping[next_state])
        if s1 in dfa1.final_states and s2 in dfa2.final_states:
            dfa.final_states.add(current_state_name)

    return dfa


def specify_operation_on_dfa (operation, dfa_list):
    if operation == "Complement":
        dfa = dfa_list.popleft()
        return complement(dfa)

    elif operation == "Union":
        dfa = dfa_list.popleft()
        while dfa_list:
            dfa = union(dfa, dfa_list.popleft())
        return dfa

    elif operation == "Intersection":
        dfa = dfa_list.popleft()
        while dfa_list:
            dfa = intersection(dfa, dfa_list.popleft())
        return dfa
