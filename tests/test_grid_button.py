import tkinter as tk
from gameOthello.gridButton import GridButton

root = tk.Tk()

def test_gridButton_init():
    coordinates = (0, 0)
    image = tk.PhotoImage(width=50, height=50)
    button = GridButton(coordinates, image)
    assert button.coordinates == coordinates
    assert button["fg"] == "black"
    assert button["bg"] == "#009067"
    assert button["image"] == str(image)
    assert button["width"] == 50
    assert button["height"] == 50
    assert button["borderwidth"] == 0
    assert button["border"] == 0
    assert button["highlightthickness"] == 0
    assert button["activebackground"] == "#009067"
    assert button["compound"] == "center"


def test_gridButton_activate():
    coordinates = (0, 0)
    image = tk.PhotoImage(width=50, height=50)
    button = GridButton(master=root, coordinates=coordinates, image=image)
    function_called = False

    def test_function(event):
        nonlocal function_called
        function_called = True

    button.activate(test_function)
    assert button["activebackground"] == "green"
    assert "test_function" in button.bind("<ButtonPress-1>")


def test_gridButton_deactivate():
    coordinates = (0, 0)
    image = tk.PhotoImage()
    button = GridButton(coordinates, image)
    button.deactivate()
    assert button["activebackground"] == "#009067"
    # Verify that the button does not have any binding for ButtonPress-1 event
    assert button.bind("<ButtonPress-1>") == ""