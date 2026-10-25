# Larp

An esoteric programming language like Brainf**k where you move the needle, build aura, and circle back until the work is done. The interpreter is written in Python and uses only the standard library.

```text
import opsec from mainframe

aura#
aura++
leak
takeitoffline
```

This program prints `3`.

## Quick start

Install **Python 3.10 or newer**, then run the interpreter from this directory:

```bash
python larpi.py addition.larp
```

On Windows, you can also use `py` instead of `python`. No packages need to be installed.

The included addition program prompts for two integers. Enter nonnegative values, such as `2` and `3`; the final numeric output will be `5`.

To run your own program, save it as a `.larp` file and pass its path to the interpreter:

```bash
python larpi.py your_program.larp
```

## How it works

Larp stores integers in a tape called **bandwidth**. Each cell holds **aura**, and a pointer selects the current cell.

- The tape starts with one cell containing `0`.
- Moving beyond either end creates a new cell containing `0`.
- Arithmetic and input affect the current cell.
- Values can be negative; they do not wrap around.

Every program must begin with `import opsec from mainframe` as its first nonblank line. Put one instruction on each line. Instructions are case-sensitive.

## Instructions

| Instruction | Effect |
| --- | --- |
| `import opsec from mainframe` | Required opening line. |
| `movetheneedle` | Move one cell left. |
| `MOVETHENEEDLE` | Move one cell right. |
| `aura++` | Add `1` to the current cell. |
| `aura--` | Subtract `1` from the current cell. |
| `aura#` | Add `2` to the current cell. |
| `touchbase` | Read an integer into the current cell. |
| `leak` | Print the current cell's value. |
| `circleback:` | Start a loop that runs while the current cell is nonzero. |
| `endcircleback` | End the innermost open loop. |
| `takeitoffline` | Exit the program immediately. |

Write instructions exactly as shown above.

## Loops

Close every `circleback:` with `endcircleback`. Loops can be nested; indentation is for readability and does not define the loop body.

This countdown prints `3`, `2`, then `1`, each on its own line:

```text
import opsec from mainframe

aura#
aura++
circleback:
    leak
    aura--
endcircleback
```

The loop checks whichever cell the pointer selects at the start of each iteration. If the body moves the pointer, that can change whether the loop continues. A negative value is also nonzero, so repeatedly decrementing it will not end a loop.

## Included files

| File | Purpose |
| --- | --- |
| `larpi.py` | Tokenizer, syntax tree, and interpreter. |
| `addition.larp` | Adds two nonnegative integers by moving their values into a third cell. |
| `tree.py` | Standalone tree traversal experiment; not needed to run Larp programs. |

## Current limitations

Larp is experimental. Comments are not supported. Unknown instructions are generally ignored, and malformed loops have limited validation.
