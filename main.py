import tkinter as tk
from gui import WelcomeScreen, TierSelectionScreen, CalculationScreen

class PIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        self.frames = {}
        for F in (WelcomeScreen, TierSelectionScreen, CalculationScreen):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("WelcomeScreen")
        self.title("EVE PI Calculator")
        self.geometry("640x720")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        self.update_idletasks()
        self.geometry("")  # Auto-resize window to fit content

if __name__ == "__main__":
    app = PIApp()
    app.mainloop()
