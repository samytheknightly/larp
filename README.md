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

The included addition program prompts for two integers. Enter `2` and `3`; the final numeric output will be `5`. Input values and the sum wrap modulo `256`, and output is signed: `127` plus `1` prints `-128`, while `200` plus `100` prints `44`.

To subtract the second input from the first, run:

```bash
python larpi.py subtraction.larp
```

Enter `2` and `3` to print `-1`. Subtraction uses the same wrapping arithmetic and signed output: `-128` minus `1` prints `127`.

To run your own program, save it as a `.larp` file and pass its path to the interpreter:

```bash
python larpi.py your_program.larp
```

## How it works

Larp stores unsigned 8-bit values (`0`–`255`) in a tape called **bandwidth** and prints them as signed two's-complement integers (`-128`–`127`). Each cell holds **aura**, and a pointer selects the current cell.

- The tape starts with one cell containing `0`.
- Moving beyond either end creates a new cell containing `0`.
- Arithmetic and input affect the current cell.
- Arithmetic wraps modulo `256`: incrementing `255` gives `0`, and decrementing `0` gives `255`.
- Integer input is also reduced modulo `256`: `256` becomes `0`, and `-1` becomes `255`.
- `leak` prints stored values `0`–`127` unchanged and subtracts `256` from values `128`–`255`. For example, stored `128` prints `-128`, and stored `255` prints `-1`. Printing does not change the cell.

From the program's output, incrementing `127` wraps to `-128`, and decrementing `-128` wraps to `127`. Decrementing a zero cell prints `-1`.

Every program must begin with `import opsec from mainframe` as its first nonblank line. Put one instruction on each line. Instructions are case-sensitive.

## Instructions

| Instruction | Effect |
| --- | --- |
| `import opsec from mainframe` | Required opening line. |
| `movetheneedle` | Move one cell left. |
| `MOVETHENEEDLE` | Move one cell right. |
| `aura++` | Add `1` to the current cell, wrapping modulo `256`. |
| `aura--` | Subtract `1` from the current cell, wrapping modulo `256`. |
| `aura#` | Add `2` to the current cell, wrapping modulo `256`. |
| `touchbase` | Read an integer into the current cell, reduced modulo `256`. |
| `leak` | Print the current cell as a signed integer from `-128` to `127`. |
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

The loop checks whichever cell the pointer selects at the start of each iteration. If the body moves the pointer, that can change whether the loop continues. Repeatedly decrementing a fixed cell reaches `0` from any nonzero value. Other loop bodies can still run forever; for example, repeatedly adding `2` to an odd value never reaches `0`.

## Included files

| File | Purpose |
| --- | --- |
| `larpi.py` | Tokenizer, syntax tree, and interpreter. |
| `addition.larp` | Adds two input values modulo `256` by moving their values into a third cell. |
| `subtraction.larp` | Subtracts the second input from the first modulo `256`, leaving the result in the first cell. |
| `tree.py` | Standalone tree traversal experiment; not needed to run Larp programs. |

## Current limitations

Larp is experimental. Comments are not supported. Unknown instructions are generally ignored, and malformed loops have limited validation.
