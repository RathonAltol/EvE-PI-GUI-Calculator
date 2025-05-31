import tkinter as tk
from tkinter import Canvas

class WelcomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Eve Online PI Calculator")
        self.geometry("600x600")  # Increased height by 50%
        self.configure(bg="#2e2e2e")  # Dark mode background

        # Header
        header = tk.Label(
            self,
            text="Eve Online PI Calculator",
            font=("Arial", 24, "bold"),
            fg="#ffffff",  # White text
            bg="#2e2e2e"
        )
        header.pack(pady=50)

        # Start Button with rounded corners
        start_button = self.create_rounded_button(
            text="Start",
            command=self.show_tier_screen
        )
        start_button.pack(pady=20)

    from typing import Callable

    def create_rounded_button(self, text: str, command: 'Callable[[], None]') -> tk.Frame:
        frame = tk.Frame(self, bg="#2e2e2e")
        canvas = Canvas(frame, width=124, height=54, bg="#2e2e2e", highlightthickness=0)
        canvas.pack()

        # Draw white border
        canvas.create_oval(8, 8, 42, 42, fill="#2e2e2e", outline="#ffffff", width=2)
        canvas.create_oval(82, 8, 116, 42, fill="#2e2e2e", outline="#ffffff", width=2)
        canvas.create_rectangle(22, 8, 102, 42, fill="#2e2e2e", outline="#ffffff", width=2)

        # Draw rounded rectangle inside the border
        canvas.create_oval(10, 10, 40, 40, fill="#444444", outline="#444444")
        canvas.create_oval(80, 10, 110, 40, fill="#444444", outline="#444444")
        canvas.create_rectangle(25, 10, 95, 40, fill="#444444", outline="#444444")

        # Add text
        canvas.create_text(60, 25, text=text, fill="#ffffff", font=("Arial", 14, "bold"))

        # Bind click event
        canvas.bind("<Button-1>", lambda e: command())

        return frame

    def show_tier_screen(self):
        self.destroy()  # Close the welcome screen
        TierScreen().mainloop()  # Open the tier screen


class TierScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Select Tier")
        self.geometry("600x600")  # Match the height of the welcome screen
        self.configure(bg="#2e2e2e")  # Dark mode background

        # Header
        header = tk.Label(
            self,
            text="Select a Tier",
            font=("Arial", 24, "bold"),
            fg="#ffffff",  # White text
            bg="#2e2e2e"
        )
        header.pack(pady=50)

        # Tier Buttons
        for tier in ["P1", "P2", "P3", "P4"]:
            tier_button = self.create_rounded_button(
                text=tier,
                command=lambda t=tier: self.select_tier(t)
            )
            tier_button.pack(pady=10)

    from typing import Callable

    def create_rounded_button(self, text: str, command: 'Callable[[], None]') -> tk.Frame:
        frame = tk.Frame(self, bg="#2e2e2e")
        canvas = Canvas(frame, width=124, height=54, bg="#2e2e2e", highlightthickness=0)
        canvas.pack()

        # Draw white border
        canvas.create_oval(8, 8, 42, 42, fill="#2e2e2e", outline="#ffffff", width=2)
        canvas.create_oval(82, 8, 116, 42, fill="#2e2e2e", outline="#ffffff", width=2)
        canvas.create_rectangle(22, 8, 102, 42, fill="#2e2e2e", outline="#ffffff", width=2)

        # Draw rounded rectangle inside the border
        canvas.create_oval(10, 10, 40, 40, fill="#444444", outline="#444444")
        canvas.create_oval(80, 10, 110, 40, fill="#444444", outline="#444444")
        canvas.create_rectangle(25, 10, 95, 40, fill="#444444", outline="#444444")

        # Add text
        canvas.create_text(60, 25, text=text, fill="#ffffff", font=("Arial", 14, "bold"))

        # Bind click event
        canvas.bind("<Button-1>", lambda e: command())

        return frame

    def select_tier(self, tier: str) -> None:
        print(f"Tier {tier} selected!")  # Placeholder for actual functionality


if __name__ == "__main__":
    app = WelcomePage()
    app.mainloop()
