from pathlib import Path
import sys
from larpi import ast

def transpile():
    bf = ast.transpile()
    my_file = Path(sys.argv[1]).with_suffix(".bf")
    my_file.write_text(bf)