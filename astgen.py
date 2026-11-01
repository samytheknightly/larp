from classes import AST, LoopNode, InstructionNode, FunctionDeclarationNode, FunctionCallNode

def generate_ast(tokenized_clean_lines: list[list[str]]):
    ast = AST()
    for i in range(len(tokenized_clean_lines)):
        tokens = tokenized_clean_lines[i]
        instruction = InstructionNode(" ".join(tokens))
        loop = LoopNode()

        if i == 0 and " ".join(tokens) != "import opsec from mainframe":
            raise SyntaxError("bro got no opsec")
        elif tokens[0] == "deepdive:":
            ast.functions.open = True
        elif tokens[0] == "enddeepdive":
            ast.functions.open = False
        elif ast.functions.open:
            if tokens[0] == "synergy" and ast.functions.func is None:
                ast.add_function_declaration(tokens[1][:-1], FunctionDeclarationNode())
            elif tokens[0] == "endsynergy":
                ast.functions.func = None
            elif ast.functions.func is not None:
                if tokens[0] == "circleback:":
                    ast.functions.func.add_to_deepest_open_loop(loop)
                elif tokens[0] == "endcircleback":
                    ast.functions.func.get_deepest_open_loop()[0].open = False
                elif tokens[0].endswith("()"):
                    ast.functions.func.add_to_deepest_open_loop(FunctionCallNode(tokens[0][:-2]))
                else:
                    ast.functions.func.add_to_deepest_open_loop(instruction)
        elif tokens[0].endswith("()"):
            ast.add_to_deepest_open_loop(FunctionCallNode(tokens[0][:-2]))
        elif tokens[0] == "circleback:":
            ast.add_to_deepest_open_loop(loop)
        elif tokens[0] == "endcircleback":
            ast.get_deepest_open_loop()[0].open = False
        else:
            ast.add_to_deepest_open_loop(instruction)
    return ast