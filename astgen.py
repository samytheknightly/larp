from classes import AST, LoopNode, InstructionNode

def generate_ast(tokenized_clean_lines: list[list[str]]):
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
    return ast