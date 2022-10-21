// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(LOOP)
@16384
D=A
@position
M=D
@8192
D=A
@AllWords
M=D
@KBD
D=M
@WHITE
D;JEQ
@BLACK
D;JMP

(WHITE)
@0
D=A
@filler
M=D
@ChangeScr
D;JMP

(BLACK)
@0
D=A-1
@filler
M=D
@ChangeScr
D;JMP

(ChangeScr)
@AllWords
D=M
@LOOP
D;JLE

@filler
D=M
@position
A=M
M=D

@position
M=M+1
@AllWords
M=M-1
@ChangeScr
D;JMP
