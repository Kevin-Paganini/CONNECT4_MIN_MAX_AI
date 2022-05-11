Connect 4 Game

To run the GUI game (main program):
In the command prompt, navigate to the unzipped Connect 4 folder, and type: python VisualGame.py

Problems that may occur (hopefully not):
Our game uses non default font. I assume it comes preinstalled on the machine, since
neither of us installed it intentionally, nor did we install anything other than pygame.

To fix: on line 29 of Pyboard.py, there is a commented out default windows font path.
Uncommenting this will use the default font on the machine

To run the text game:
In the command prompt, navigate to the unzipped Connect 4 folder, and type: python main.py

Dependencies:
random
pygame
numpy
time
sys
csv
deepcopy from copy
convolve2d from scipy.signal

