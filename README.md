# Larp Language

```text
import opsec from mainframe // MANDATORY! no opsec, no program
```

```text
bandwidth = 5 // 5 cells of storage (aura)
```

### Movement

```text
move the needle // move 1 aura to the left

MOVE THE NEEDLE // MOVE 1 AURA TO THE RIGHT
```

### Aura Operations

```text
aura-- // aura++

aura++ // aura--

aura# // aura += 2
```

### Input

```text
touch base // aura = input()
```

### Loops

```text
circle back: // check if aura is positive and loops

    aura--
```

### Output

```text
leak aura // print(aura)

leak bandwidth // print(bandwidth)
```

### Exit

```text
take it offline // exit()
```
