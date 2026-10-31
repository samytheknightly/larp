# LARP

A Brainf***-style language with corporate jargon and slang.

## Run

Requires Python 3.10+.

```sh
python larpi.py scripts/addition.larp
```

More examples are in [scripts/](scripts/).

## Basics

- Start every program with `import opsec from mainframe`.
- Write one instruction per line. Instructions are case-sensitive; indentation is optional.
- The tape starts with one zero-valued cell and the pointer at cell 0. Moving right grows the tape; moving left at cell 0 does nothing.
- Cell values and integer input wrap modulo 256. Numeric output is signed (−128 to 127).
- Uppercase leaks print signed integers. `leak(aura)` writes raw bytes directly.

## Instructions

| Instruction | Effect | Brainf*** export |
| --- | --- | --- |
| `MOVETHENEEDLE` | Move right. | `>` |
| `movetheneedle` | Move left. | `<` |
| `aura++` | Add 1. | `+` |
| `aura--` | Subtract 1. | `-` |
| `aura#` | Add 2. | `++` |
| `touchbase` | Read an integer. | `,` |
| `leak(aura)` | Write the current cell as one raw byte, without a newline. | `.` |
| `leak(AURA)` | Print the current signed integer, with a newline. | Unsupported |
| `leak(BANDWIDTH)` | Print a list of signed integers, with a newline. | Unsupported |
| `circleback:` | Loop while the current cell is nonzero. | `[` |
| `endcircleback` | End the loop. | `]` |
| `takeitoffline` | Exit. | Unsupported |

Loops support nesting. Write arithmetic instructions without spaces.

## Example

Prints 3, 2, and 1 on separate lines:

```text
import opsec from mainframe

aura#
aura++
circleback:
    leak(AURA)
    aura--
endcircleback
```

## Export to Brainf***

```sh
python larpi.py path/to/program.larp --bf
```

Runs the program, then writes a `.bf` file beside the source, overwriting an existing file. Instructions marked **Unsupported** are rejected during transpilation.

`leak(aura)` maps to Brainf***'s `.` for raw-byte output.

To display `é` in a UTF-8 terminal when running LARP, use `leak(aura)` to output the byte values `195` then `169`.
