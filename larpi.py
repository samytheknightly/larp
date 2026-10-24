import sys

bandwidth = []
aura_pointer = 0 # 0-indexed
in_loop = False
loop_content = []

def tokenized(line: str):
    buffer = ""
    tokens = []
    for i in range(len(line)):
        char = line[i]
        if char == " " and buffer != "":
            tokens.append(buffer)
            buffer = ""
        elif char != "\n":
            buffer += char
        if i == len(line) - 1 and buffer != "":
            tokens.append(buffer)
    return tokens

def execute(tokens: str, first_line = False, last_line = False):
    global bandwidth
    global aura_pointer
    global in_loop
    global loop_content

    if first_line and tokens != ["import", "opsec", "from", "mainframe"]:
        raise Exception("no opsec == not tuff")
    
    if in_loop:
        if tokens[:2] == [" "] * 2:
            loop_content.append(tokens[2:])
            return
        elif len(loop_content) == 0:
            in_loop = False
        else:
            while bandwidth[aura_pointer]:
                in_loop = False
                for line in loop_content:
                    execute(line)
            in_loop = False
            loop_content = []
    
    if last_line:
            if tokens == ["take", "it", "offline"]:
                sys.exit()
            else:
                raise Exception("no take it offline == negative aura")
            
    if tokens[:2] == ["bandwidth", "="]:
        bandwidth = [0] * int(tokens[2])
    elif tokens == ["move", "the", "needle"]:
        aura_pointer -= 1
        if aura_pointer < 0:
            raise Exception("negative aura pointer - lock in")
    elif tokens == ["MOVE", "THE", "NEEDLE"]:
        aura_pointer += 1
        if aura_pointer == len(bandwidth):
            raise Exception("aura pointer out of bounds - lock in")
    elif tokens == ["aura--"]:
        bandwidth[aura_pointer] -= 1
    elif tokens == ["aura++"]:
        bandwidth[aura_pointer] += 1
    elif tokens == ["aura#"]:
        bandwidth[aura_pointer] += 2
    elif tokens == ["circle", "back:"]:
        if in_loop:
            raise Exception("nested loops are NOT sigma")
        in_loop = True
    elif tokens == ["touch", "base"]:
        bandwidth[aura_pointer] = int(input(f"Aura in cell {aura_pointer} (0-indexed): "))
    elif tokens == ["leak", "aura"]:
        print(bandwidth[aura_pointer])
    elif tokens == ["leak", "bandwidth"]:
        print(bandwidth)
    
with open(sys.argv[1], "r") as larp_file:
    lines = larp_file.readlines()
    clean_lines = []
    for i in range(len(lines)):
        line = lines[i]
        tokens = tokenized(line)
        if len(tokens):
            clean_lines.append(tokens)

    for i in range(len(clean_lines)):
        line = clean_lines[i]
        execute(line, i==0, i==len(clean_lines)-1)