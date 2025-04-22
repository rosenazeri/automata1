class Grammar:
    alphabet = set()
    variables = set()
    start = ""
    rules = {}
    
    def __init__(self, alphabet, variables, start, rules):
        self.alphabet = alphabet
        self.variables = variables
        self.start = start
        self.rules = rules
