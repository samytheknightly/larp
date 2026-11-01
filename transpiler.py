from classes import AST
from pathlib import Path
import sys

def transpile(ast: AST):
    bf = ast.transpile()
    my_file = Path(sys.argv[1]).with_suffix(".bf")
    my_file.write_text(bf)