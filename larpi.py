import sys
from collections import deque

bandwidth = deque([0])
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
        elif self.instruction == "movetheneedle":
            if aura_pointer == 0:
                bandwidth.appendleft(0)
            else:
                aura_pointer -= 1
        elif self.instruction == "MOVETHENEEDLE":
            if aura_pointer == len(bandwidth) - 1:
                bandwidth.append(0)
            aura_pointer += 1
        elif self.instruction == "touchbase":
            bandwidth[aura_pointer] = int(input(f"input aura at position {aura_pointer}: ")) % 256
        elif self.instruction == "leak":
            print(bandwidth[aura_pointer] % 256 if bandwidth[aura_pointer] <= 127 else bandwidth[aura_pointer] - 256)
        elif self.instruction == "aura ++":
            bandwidth[aura_pointer] = (bandwidth[aura_pointer] + 1) % 256
        elif self.instruction == "aura --":
            bandwidth[aura_pointer] = (bandwidth[aura_pointer] - 1) % 256
        elif self.instruction == "aura #":
            bandwidth[aura_pointer] = (bandwidth[aura_pointer] + 2) % 256

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

class AST:
    def __init__(self):
        self.body: list[LoopNode | InstructionNode] = []
        self.open = True
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

with open(sys.argv[1], "r") as larp_file:
    lines = larp_file.readlines()
    tokenized_clean_lines = [tokens for line in lines if len(tokens := tokenized(line.replace("\n", "")))]

    ast = AST()
    for i in range(len(tokenized_clean_lines)):
        tokens = tokenized_clean_lines[i]

        if i == 0 and " ".join(tokens) != "import opsec from mainframe":
            raise SyntaxError("bro got no opsec")

        if tokens[0] == "circleback:":
            ast.add_to_deepest_open_loop(LoopNode())
        elif tokens[0] == "endcircleback":
            ast.get_deepest_open_loop()[0].open = False
        else:
            ast.add_to_deepest_open_loop(InstructionNode(" ".join(tokens)))
    # ast.print()
    # print("------------------")
    # print("------------------")
    # print("------------------")
    ast.run()