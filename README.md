import opsec from mainframe  // MANDATORY! no opsec, no program

bandwidth = 5  // 5 cells of storage (aura)

# Movement
move the needle  // move 1 aura to the left
MOVE THE NEEDLE  // MOVE 1 AURA TO THE RIGHT

# Aura Operations
aura--  // aura++
aura++  // aura--
aura#   // aura += 2

# Input
touch base  // aura = input()

# Loops
circle back:  // check if aura is positive and loops
    aura--

# Output
leak aura       // print(aura)
leak bandwidth  // print(bandwidth)

# Exit
take it offline  // exit()