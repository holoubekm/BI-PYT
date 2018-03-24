# BI-PYT Course
## Programování v Pythonu 3
### CTU / ČVUT FIT

### Semestral work
#### Brainfuck, braincopter and brainloller interpreter
This semestral work was a rather complex one. We had to implement `brainfuck` interpreter. Furthermore interpreter had to support the `braincopter` variant when input is loaded from `.png` image file where `(65536 * R + 256 * G + B) % 11` determines which command should we interpret.

Another supported variant was `rainloller` when command are interpreted as a specific coloured pixels. This mode adds two new command to move inside 2D data of the image. 

Besides loading the program support saving - you can save `brainfuck` code into the chosen image and interpret it then.

Implementation was a bit harder due to the ban of external imaging libraries. The source code thus implements reading different `.png` variants. 

### How to run
Check corectness of the program
```bash
python tests.py
```
Shows help and terminates
```bash
python brainx -h
```
Run interpreter in the interactive mode
```bash
python brainx
```

Commands and examples of conversion
```bash

python brainx --lc2f -i input.png -p dest.b

#Run the braincopter variant where the input is hidden to pixels of alreadyexisting image 
python brainx --f2lc -i input.b -i dest.png -o output.png

#Run the braincopter variant where the input is converted directly to pixels of a new image
python brainx --f2lc -i input.b -o output.png

```
