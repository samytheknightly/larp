# LARP

A Brainf***-style language with corporate jargon and slang.

## Run

Requires Python 3.14+.

```sh
python larpi.py scripts/addition.larp
```

More examples are in [scripts/](scripts/).

## Basics

- Start every program with `import opsec from mainframe`.
- Declare functions anywhere after the opening import, including after calls to them.
- Write one instruction per line. Instructions are case-sensitive; indentation is optional.
- The tape starts with one zero-valued cell and the pointer at cell 0. Moving right grows the tape; moving left stops at cell 0.
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
| `leak(aura)` | Write the current cell as one raw byte. | `.` |
| `leak(AURA)` | Print the current signed integer, with a newline. | Interpreter only |
| `leak(BANDWIDTH)` | Print a list of signed integers, with a newline. | Interpreter only |
| `circleback:` | Loop while the current cell is nonzero. | `[` |
| `endcircleback` | End the loop. | `]` |
| `takeitoffline` | Exit. | Interpreter only |

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

## Functions

Declare a function with `synergy name:`, close it with `endsynergy`, and call it using `name()` on its own line. Declarations can appear before or after calls:

```text
import opsec from mainframe

synergy increment:
    aura++
endsynergy

boost()
boost()
leak(AURA)

synergy boost:
    aura#
    increment()
endsynergy
```

Each call runs the function body once, then continues after the call. Functions share the program's tape and pointer, so their changes remain after a call. Use the tape to pass data. Function bodies can contain loops and calls to other functions.

The example leaves `6` in the current cell and prints it.

Function declarations are collected before execution and do not run until called. The main program's executable instructions run in source order.

The interpreter supports recursive calls. Use a tape-based stopping condition, such as a `circleback:` loop whose current cell reaches zero, to end the recursion. Each recursive call shares the same tape and pointer.

## Export to Brainf***

```sh
python transpiler.py path/to/program.larp
```

Parses the program and writes a `.bf` file beside the source, overwriting an existing file.

Loops export as bracketed bodies, and function calls expand inline, including loops within those functions. Use instructions with a Brainf*** mapping in the main program and called functions when exporting.

For export, use non-recursive function call chains so each call expands into a finite sequence of Brainf*** instructions.

`leak(aura)` maps to Brainf***'s `.` for raw-byte output.

To display `é` in a UTF-8 terminal when running LARP, use `leak(aura)` to output the byte values `195` then `169`.
