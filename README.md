# LARP

LARP is a small, Brainf***-style programming language with corporate-jargon instructions. Its Python interpreter, `larpi.py`, runs `.larp` programs and can also export their core instructions to Brainf***.

## Requirements

- Python 3.10 or newer.
- No third-party Python packages are required.

## Run a program

From the project directory:

```sh
python larpi.py scripts/addition.larp
```

Enter `2` and `3` at the two input prompts. The program prints `5`. If your system uses `python3` for Python 3, substitute it for `python` in these commands.

To run another program, pass its path as the first argument:

```sh
python larpi.py path/to/program.larp
```

## Language basics

Each program starts with this required header on its first nonblank line:

```text
import opsec from mainframe
```

Write one instruction per line. Instructions are case-sensitive; in particular, `movetheneedle` and `MOVETHENEEDLE` move in opposite directions. Blank lines and indentation are allowed. Both `aura++` and `aura ++` work, as do `aura--` and `aura --`.

### Memory

- **Bandwidth** is the memory tape. It starts with one cell containing zero.
- The **aura pointer** starts at cell 0 and selects the current cell.
- Moving right beyond the allocated tape adds a new zero-valued cell. Moving left at cell 0 leaves the pointer there.
- Cells store values from 0 through 255. Arithmetic and numeric input wrap modulo 256.
- Output displays signed values from -128 through 127: for example, a stored value of 255 prints as `-1`.

### Instructions

| Instruction | Effect | Brainf*** export |
| --- | --- | --- |
| `import opsec from mainframe` | Required program header; no runtime effect. | Omitted |
| `MOVETHENEEDLE` | Move the pointer one cell right. | `>` |
| `movetheneedle` | Move the pointer one cell left, stopping at cell 0. | `<` |
| `aura++` | Increment the current cell by 1. | `+` |
| `aura--` | Decrement the current cell by 1. | `-` |
| `aura #` | Increment the current cell by 2. | `++` |
| `touchbase` | Read an integer into the current cell. | `,` |
| `leak(aura)` | Print the current cell as a signed integer. | `.` |
| `leak(bandwidth)` | Print all allocated cells as a list of signed integers. | Omitted |
| `circleback:` | Start a loop that runs while the current cell is nonzero. | `[` |
| `endcircleback` | End a loop. | `]` |
| `takeitoffline` | Exit the interpreter immediately. | Omitted |

Loops can be nested. The loop condition uses whichever cell the pointer selects when the condition is checked, so moving the pointer inside a loop can change which cell controls it.

### Example

Save this as `countdown.larp`:

```text
import opsec from mainframe

aura #
aura++
circleback:
    leak(aura)
    aura--
endcircleback
```

Run it with `python larpi.py countdown.larp`. It prints:

```text
3
2
1
```

## Export to Brainf***

Add `--bf` after the program path:

```sh
python larpi.py scripts/addition.larp --bf
```

The interpreter **runs the LARP program first**, including any input prompts, and then writes `scripts/addition.bf`. The output file is placed beside the source with its extension replaced by `.bf`; an existing file at that path is overwritten.

The export maps instructions according to the table above. LARP reads and prints integers, while typical Brainf*** interpreters use character input and output, so exported programs can behave differently for I/O. Tape boundaries also depend on the Brainf*** interpreter. `leak(bandwidth)` and `takeitoffline` have no exported equivalent. If execution reaches `takeitoffline`, it exits before the `.bf` file is written; a program that never finishes likewise never writes the export.

## Included programs

The [scripts](scripts/) directory contains arithmetic, copying, and pointer-movement examples:

| Files | Purpose |
| --- | --- |
| `addition.larp`, `subtraction.larp`, `multiplication.larp` | Arithmetic examples using numeric input. |
| `divisionwithoutremainder.larp` | Division example intended for division without a remainder. |
| `copy.larp` | Copy a value to the next cell while restoring the source. |
| `copytosecondnextcell.larp`, `copytothirdnextcell.larp`, `copytofourthnextcell.larp` | Copy values to cells farther along the tape. |
| `jumpby.larp`, `jumpleftby.larp` | Move the pointer using a value supplied as input. |

Arithmetic uses the same wrapping cell values as every other program. Inspect the scripts for their input order and tape usage.

## Project layout

- [larpi.py](larpi.py): tokenizer, syntax-tree construction, interpreter, and Brainf*** export.
- [scripts/](scripts/): example LARP programs.

## Current limitations

The parser performs limited validation. Unknown instruction lines are silently ignored, and malformed loops are not reliably diagnosed. The examples use standalone `//` lines as annotations, but there is no dedicated comment parser; avoid inline comments on instructions. `#` is part of the increment-by-two instruction, not a comment marker.

`touchbase` expects an integer; invalid input raises a Python exception. Script imports are not implemented: the required header is a syntax marker, not a module import.
