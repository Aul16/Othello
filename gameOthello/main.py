import os

PATH = os.path.dirname(os.path.abspath(__file__))  # Get the path of the main.py file

# Verify that all packages are installed
try:
    import PIL
except ImportError:
    if input("Do you want to install libraries ? (y/n) : ") == "y":
        os.system(f"pip install -r {PATH}/requirements.txt")
    else:
        print(
        "Please install the required libraries by running the following command : \n pip install -r requirements.txt"
        )
        exit()

# Import game window
from graphicalOthello import game_window

# Main function to start the game if everything is installed
if __name__ == "__main__":
    # start game
    game_window()
