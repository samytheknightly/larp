import sys
from pathlib import Path

bandwidth = [0]
aura_pointer = 0 # 0-indexed

def tokenized(line: str):
    buffer = ""
    tokens = []
    for i in range(len(line)):
        char = line[i]
        if char == " " and buffer != "":
            tokens.append(buffer)
            buffer = ""
        elif char in ["+", "-"]:
            if buffer not in ["+", "-"]:
                tokens.append(buffer)
                buffer = char
            elif char == buffer:
                tokens.append(buffer + char)
                buffer = ""
        elif char == "#":
            tokens.append(buffer)
            buffer = ""
            tokens.append(char)
        elif not char.isspace():
            buffer += char
        if i == len(line) - 1 and buffer != "":
            tokens.append(buffer)

    return tokens

class InstructionNode:
    def __init__(self, instruction: str):
        self.instruction = instruction
    def print(self):
        print(self.instruction)
    def run(self):
        global aura_pointer
        if self.instruction == "takeitoffline":
            sys.exit()
        elif self.instruction == "movetheneedle" and aura_pointer > 0:
            aura_pointer -= 1
        elif self.instruction == "MOVETHENEEDLE":
            if aura_pointer == len(bandwidth) - 1:
                bandwidth.append(0)
            aura_pointer += 1
        elif self.instruction == "touchbase":
            bandwidth[aura_pointer] = int(input(f"input aura at position {aura_pointer}: ")) % 256
        elif self.instruction == "leak(aura)":
            print(bandwidth[aura_pointer] % 256 if bandwidth[aura_pointer] <= 127 else bandwidth[aura_pointer] - 256)
        elif self.instruction == "leak(bandwidth)":
            print([aura % 256 if aura <= 127 else aura - 256 for aura in bandwidth])
        elif self.instruction == "aura ++":
            bandwidth[aura_pointer] = (bandwidth[aura_pointer] + 1) % 256
        elif self.instruction == "aura --":
            bandwidth[aura_pointer] = (bandwidth[aura_pointer] - 1) % 256
        elif self.instruction == "aura #":
            bandwidth[aura_pointer] = (bandwidth[aura_pointer] + 2) % 256
    def convert_to_bf(self):
        bf = ""
        if self.instruction == "movetheneedle":
            bf="<"
        elif self.instruction == "MOVETHENEEDLE":
            bf=">"
        elif self.instruction == "touchbase":
            bf=","
        elif self.instruction == "leak(aura)":
            bf="."
        elif self.instruction == "aura ++":
            bf="+"
        elif self.instruction == "aura --":
            bf="-"
        elif self.instruction == "aura #":
            bf="++"
        return bf

class LoopNode:
    def __init__(self):
        self.open = True
        self.body: list[LoopNode | InstructionNode] = []
    def get_deepest_open_loop(self, depth):
        front = []
        visited = []
        for child in self.body:
            if isinstance(child, LoopNode) and child.open:
                front.append(child)
                visited.append(child.get_deepest_open_loop(depth+1))
        if len(visited):
            return max(visited, key=lambda x: x[1])
        return (self, depth)
    def print(self):
        print(self.body)
        for child in self.body:
            child.print()
    def run(self):
        global aura_pointer
        while bandwidth[aura_pointer] != 0:
            for child in self.body:
                child.run()
    def transpile_to_bf(self, bf):
        if self.open:
            bf+="["
        else:
            bf+="]"
        return bf

class AST:
    def __init__(self):
        self.body: list[LoopNode | InstructionNode] = []
        self.open = True
        self.bf = ""
    def add_to_deepest_open_loop(self, node):
        self.get_deepest_open_loop()[0].body.append(node)
    def get_deepest_open_loop(self):
        front = []
        visited = []
        for child in self.body:
            if isinstance(child, LoopNode) and child.open:
                front.append(child)
                visited.append(child.get_deepest_open_loop(1))
        if len(visited):
            return max(visited, key=lambda x: x[1])
        return (self, 0)
    def print(self):
        for child in self.body:
            child.print()
    def run(self):
        for child in self.body:
            child.run()
    def transpile_to_bf(self):
        for child in self.body:
            self.bf = child.transpile_to_bf(self.bf)
        return self.bf

with open(sys.argv[1], "r") as larp_file:
    lines = larp_file.readlines()
    tokenized_clean_lines = [tokens for line in lines if len(tokens := tokenized(line.replace("\n", "")))]

    bf = ""
    transpile = False
    if "--bf" in sys.argv:
        transpile = True

    ast = AST()
    for i in range(len(tokenized_clean_lines)):
        tokens = tokenized_clean_lines[i]

        if i == 0 and " ".join(tokens) != "import opsec from mainframe":
            raise SyntaxError("bro got no opsec")
        if tokens[0] == "circleback:":
            if transpile:
                bf+="["
            ast.add_to_deepest_open_loop(LoopNode())
        elif tokens[0] == "endcircleback":
            if transpile:
                bf+="]"
            ast.get_deepest_open_loop()[0].open = False
        else:
            instruction = InstructionNode(" ".join(tokens))
            if transpile:
                bf+=instruction.convert_to_bf()
            ast.add_to_deepest_open_loop(instruction)
            
    ast.run()
    if transpile:
        my_file = Path(sys.argv[1]).with_suffix(".bf")
        my_file.write_text(bf)
