# pyGameTools
Hi, this a very quick and dirty setup for game dev using pygame,
I made these for my personal use case only, but feel free to use or modify it

version <--> pygame-ce 2.4.0 (SDL 2.28.5, Python 3.12.1)

IMPORTANT before using -> delete placeholder.txt file from all data directories

Tools :--

Animator - (animation.py)

Features :-
Implemented ->
1. Picture set rendering based on frames

To be Implemented ->
1. Transform (scaling, rotations), visibility (opacity) change to picture during animation
- Maybe
2. Some buttons/Key press to play and stop or pause (pause not implemented yet)
3. Slider or buttons to distribute frames for each picture
4. Buttons/key press for applying transform effects to each picture
5. Saving an animation created using animator.py

Using ->
- use the Animation class to initialize the pictures and frames and whether to loop
- give path to the set of pictures that will be used in an animation
- along with the number of frames each picture will be displayed for
- just fill up the data/anims/ directory with set of pictures for a perticular animation
- call the .play() to play the animation
- example of this is in animator.py

------------------------------------------------------------------------------
Map Editor - (mapeditor.py)

Features :-
Implemented ->
1. Save and load Map
2. 2D map editing with Precision Tile placement & Grid based Tile placement
3. Preview and placement highlighting during placement

To be Implemented ->
1. Precision Tile deleting
2. Texture overlay for a collection of grid space
3. Setting a base grid size for a map before starting to edit
4. More flexible sprite loading and choosing

Using ->
- load map tiles in spritePath
- can use numbers for file names for the tiles

keys - use
- g -------------------- toggle grid mode for grid based placement
- mouse scroll up/down - scroll through different types of sprites loadded from data
- left shift ----------- toggle to change scroll through sprite types and sprites themselves
- mouse left click ----- place sprite on screen
- mouse right click ---- delete sprite on screen 