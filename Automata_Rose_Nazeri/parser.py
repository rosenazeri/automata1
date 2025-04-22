from grammar import Grammar


def parse(file):

    alphabet = set()
    variables = set()
    start = ""
    rules = {}
    operation = ""

    grammars = []

    while True:
        line = file.readline()

        if line == "": 
            break

        line = line.strip()

        if line == "# Alphabet":
            alphabet.clear()
            variables.clear()
            rules.clear()
            line = file.readline()
            alphabet = line.strip().split()

        elif line == "# Variables":
            line = file.readline()
            variables = line.strip().split()

        elif line == "# Start":
            line = file.readline()
            start = line.strip()
        
        elif line == "# Rules":
            while True:
                line = file.readline()
                if line.strip() == "========":
                    break
                left, right = line.strip().split("->")
                rules.setdefault(left.strip(), []).append(right.strip())
            grammars.append(Grammar(alphabet.copy(), variables.copy(), start, rules.copy()))
        
        elif line == "# Operation":
            operation = file.readline().strip()

    return grammars, operation
