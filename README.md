# Wireworld
[Wireworld](https://en.wikipedia.org/wiki/Wireworld) is a cellular automaton which is well suited for simulating logic gates.

Each cell can be in one of four states:
1. empty
2. conductor   
3. electron head
4. electron tail

The simulation proceeds in discrete steps. Each step changes the cells in the following ways:
- empty &rarr; empty
- electron head &rarr; electron tail
- electron tail &rarr; conductor
- conductor &rarr; Electron head if one or two neighboring cells are electron heads, else it remains a conductor. A cell neighbors another if it is orthogonally or diagonally adjacent ([Moore neighborhood](https://en.wikipedia.org/wiki/Moore_neighborhood)).

Run wireworld.py to start it. Requires Python 3 and PyGame 2.
```
python wireworld.py
```

### Examples
An AND gate. Conductor cells are orange, electron heads are blue and electron tails are red. The inputs are on the left and the output is to the right.  
![and gate](screenshot_and_gate.png)

A half adder. Left are the two inputs. Top right is the ones output and bottom right is the twos output.  
![half_adder](screenshot_half_adder.png)

### Controls
| action | binding |
|---|---|
| change cell state | left mouse button |
| delete cell | ctrl + left mouse button |
| move the map | right mouse button |
| pause/unpause the simulation | space |
| single step | enter |
| increase speed | + |
| decrease speed | - |
| delete all electrons | backspace |
| delete all wires | ctrl + backspace |
| quit | esc |


### Optional Command Line Arguments
- **-h**, **--help**: Show a help message and exit.
- **-w**, **--window-size \<width> \<height>**: Specify the window width and height in pixels.
- **-c**, **--cell-width \<width>**: Specify the cell width in pixels.
