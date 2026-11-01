import sys
from astgen import generate_ast
from tokenizer import tokenized

sys.stdout.reconfigure(encoding='utf-8')

with open(sys.argv[1], "r") as larp_file:
    lines = larp_file.readlines()
    tokenized_clean_lines = [tokens for line in lines if len(tokens := tokenized(line.replace("\n", "")))]
    ast = generate_ast(tokenized_clean_lines)

    if __name__ == "__main__":
        ast.run()