import os

PATH = os.path.dirname(os.path.abspath(__file__))  # Get the path of the main.py file

# Install all packages
if "\\" in PATH:
    os.system(f"pip install -r {PATH}\\requirements.txt")  # Windows case
else:
    os.system(f"pip install -r {PATH}/requirements.txt")  # Other cases

# Verify that all packages are installed
try:
    import PIL
except ImportError:
    print(
        "Please verify that pip command is working or install manually the package PIL (pillow)"
    )
    exit()

# Import game window
from graphicalOthello import game_window

# Main function to start the game if everything is installed
if __name__ == "__main__":
    # start game
    game_window()
