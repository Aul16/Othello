import tkinter as tk


# Customized button to let the game know the coordinates of the button clicked
class GridButton(tk.Button):
    def __init__(self, coordinates, image, *args, **kwargs) -> None:
        """
        Button Object Generator
        """
        super().__init__(
            fg="black",
            bg="#009067",
            image=image,
            width=50,
            height=50,
            borderwidth=0,
            border=0,
            highlightthickness=0,
            activebackground="#009067",
            compound="center",
            *args,
            **kwargs
        )
        self.coordinates = coordinates

    def activate(self, function):
        super().configure(activebackground="green")
        self.bind("<ButtonPress-1>", function)

    def deactivate(self):
        super().configure(activebackground="#009067")
        self.bind("<ButtonPress-1>")
