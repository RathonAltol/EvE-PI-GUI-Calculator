import tkinter as tk
from typing import Type

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Eve Online PI Calculator")
        self.geometry("600x400")
        self.configure(bg="#2e2e2e")
        self.frames: dict[type, tk.Frame] = {}

        # Make the root window expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Initialize frames
        for F in (WelcomeScreen,):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(WelcomeScreen)

    def show_frame(self, frame_class: Type[tk.Frame]) -> None:
        frame = self.frames[frame_class]
        frame.tkraise()

class WelcomeScreen(tk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master, bg="#2e2e2e")
        # Make the frame expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Center the header text in the window
        header = tk.Label(
            self,
            text="Welcome to Eve Online PI Calculator",
            font="Arial 24 bold",
            fg="#ffffff",  # Use 'fg' instead of 'foreground' for consistency
            bg="#2e2e2e"
        )
        header.grid(row=0, column=0, sticky="s", pady=(0, 10))  # Stick to bottom of cell, less padding

        # Start Button directly under the header, centered in its cell
        start_button = tk.Button(
            self,
            text="Start",
            font="Arial 14 bold",
            fg="#ffffff",
            bg="#444444",
            activebackground="#555555",
            activeforeground="#ffffff"
        )
        start_button.grid(row=1, column=0, sticky="n")  # Stick to top of cell

if __name__ == "__main__":
    app = App()
    app.mainloop()
