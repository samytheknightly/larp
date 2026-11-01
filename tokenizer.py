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