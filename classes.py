import sys
from larpmemory import bandwidth, aura_pointer

class Node:
    pass

class InstructionNode(Node):
    def __init__(self, instruction: str):
        self.instruction = instruction
    def print(self):
        print(self.instruction)
    def run(self, ast: AST):
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
            print(f"input aura at position {aura_pointer}: ", end="", file=sys.stderr, flush=True)
            bandwidth[aura_pointer] = int(input()) % 256
        elif self.instruction == "leak(AURA)":
            print(bandwidth[aura_pointer] % 256 if bandwidth[aura_pointer] <= 127 else bandwidth[aura_pointer] - 256, flush=True)
        elif self.instruction == "leak(BANDWIDTH)":
            print([aura % 256 if aura <= 127 else aura - 256 for aura in bandwidth], flush=True)
        elif self.instruction == "leak(aura)":
            sys.stdout.buffer.write(bytes([bandwidth[aura_pointer]]))
            sys.stdout.buffer.flush()
        elif self.instruction == "aura ++":
            bandwidth[aura_pointer] = (bandwidth[aura_pointer] + 1) % 256
        elif self.instruction == "aura --":
            bandwidth[aura_pointer] = (bandwidth[aura_pointer] - 1) % 256
        elif self.instruction == "aura #":
            bandwidth[aura_pointer] = (bandwidth[aura_pointer] + 2) % 256
    def transpile(self, ast: AST) -> str:
        if self.instruction == "aura ++":
            return "+"
        if self.instruction == "aura --":
            return "-"
        if self.instruction == "aura #":
            return "++"
        if self.instruction == "leak(aura)":
            return "."
        if self.instruction == "touchbase":
            return ","
        if self.instruction == "movetheneedle":
            return "<"
        if self.instruction == "MOVETHENEEDLE":
            return ">"
        if self.instruction == "import opsec from mainframe":
            return ""
        raise SyntaxError(f"Instruction {self.instruction} cannot be transpiled to Brainf***")

class LoopNode(Node):
    def __init__(self):
        self.open = True
        self.body: list[LoopNode | InstructionNode] = []
    def get_deepest_open_loop(self, depth: int) -> tuple[LoopNode, int]:
        visited = []
        for child in self.body:
            if isinstance(child, LoopNode) and child.open:
                visited.append(child.get_deepest_open_loop(depth+1))
        if len(visited):
            return max(visited, key=lambda x: x[1])
        return (self, depth)
    def print(self):
        print(self.body)
        for child in self.body:
            child.print()
    def run(self, ast: AST):
        global aura_pointer
        while bandwidth[aura_pointer] != 0:
            for child in self.body:
                child.run(ast)
    def transpile(self, ast: AST) -> str:
        bf = "["
        for child in self.body:
            if child.transpile(ast) is not None:
                bf += child.transpile(ast)
        bf += "]"
        return bf
    
class ASTNode(Node):
    def __init__(self):
        self.body: list[LoopNode|InstructionNode|FunctionCallNode] = []
    def add_to_deepest_open_loop(self, node):
        self.get_deepest_open_loop()[0].body.append(node)
    def get_deepest_open_loop(self) -> tuple[LoopNode, int]:
        visited = []
        for child in self.body:
            if isinstance(child, LoopNode) and child.open:
                visited.append(child.get_deepest_open_loop(1))
        if len(visited):
            return max(visited, key=lambda x: x[1])
        return (self, 0)
    def print(self):
        for child in self.body:
            child.print()
    def run(self, ast: AST):
        for child in self.body:
            child.run(ast)
    def transpile(self, ast: AST):
        bf = ""
        for child in self.body:
            if child.transpile(ast) is not None:
                bf += child.transpile(ast)
        return bf

class Functions:
    def __init__(self):
        self.open = True
        self.func: FunctionDeclarationNode = None
        self.declarations: dict[str, FunctionDeclarationNode] = {}

class FunctionDeclarationNode(ASTNode):
    def __init__(self):
        super().__init__()
    def run(self, ast: AST):
        super().run(ast)
        print(self.body)

class FunctionCallNode(Node):
    def __init__(self, name):
        self.name = name
    def run(self, ast: AST):
        ast.functions.declarations[self.name].run(ast)
    def transpile(self, ast: AST):
        return ast.functions.declarations[self.name].transpile(ast)

class AST:
    def __init__(self):
        self.functions = Functions()
        self.root = ASTNode()
        self.open = True
    def add_to_deepest_open_loop(self, node: LoopNode|InstructionNode|FunctionCallNode):
        self.root.add_to_deepest_open_loop(node)
    def get_deepest_open_loop(self) -> tuple[LoopNode, int]:
        return self.root.get_deepest_open_loop()
    def print(self):
        self.root.print()
    def run(self):
        self.root.run(self)
    def transpile(self):
        return self.root.transpile(self)
    def add_function_declaration(self, name: str, node: FunctionDeclarationNode):
        self.functions.func = node
        self.functions.declarations[name] = node