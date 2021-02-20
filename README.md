# Wireworld

[Wireworld](https://en.wikipedia.org/wiki/Wireworld) is a cellular automaton which is well suited for simulating logic gates.

Each cell can be in one of four states:
1. empty
2. conductor   
3. electron head
4. electron tail

The simulation proceeds in discrete steps. Each step changes the cells change in the following ways:
- empty &rarr; empty
- electron head &rarr; electron tail
- electron tail &rarr; conductor
- conductor &rarr; Electron head if one or two neighboring cells are electron heads, else it remains a conductor. A cell neighbors another if it is orthogonally or diagonally adjacent ([Moore neighborhood](https://en.wikipedia.org/wiki/Moore_neighborhood)).


### Controls
- **Left click**: Increment cell state.
- **Right click**: Decrement cell state.
- **Space**: Pause/unpause the simulation.
- **S**: Single step.
- **+**: Double the speed.
- **-**: Halve the speed.
- **Backspace**: Delete all electrons.
- **Ctrl + Backspace**: Delete all wires.
- **ESC**: Quit.
- **F1**: Show debug info.

### Ideas for improvement
- Scrolling and zooming the map.
- Saving and loading of maps.
- Selecting groups of cells for
    - copy and paste,
    - saving and loading,
    - mass increment or decrement of cell state,
    - mass deletion.
- Easier drawing of lines, maybe by holding ctrl.
- Save the last n steps to make it possible to go back a few steps?
