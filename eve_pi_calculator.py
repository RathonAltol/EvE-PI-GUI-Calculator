import tkinter as tk
from tkinter import Canvas
from typing import Callable, Type, Optional
import json  # Import JSON module


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Eve Online PI Calculator")
        self.geometry("600x660")  # Increased height by 10% (600 -> 660)
        self.configure(bg="#2e2e2e")
        self.frames: dict[Type[tk.Frame], tk.Frame] = {}

        # Initialize frames
        for F in (WelcomePage, TierScreen, P1Screen, P2Screen, P3Screen, P4Screen):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(WelcomePage)

    def show_frame(self, frame_class: Type[tk.Frame]) -> None:
        frame = self.frames[frame_class]
        frame.tkraise()

    def create_rounded_button(self, parent: tk.Widget, text: str, command: Callable[[], None]) -> tk.Frame:
        frame = tk.Frame(parent, bg="#2e2e2e")
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
        # Use a font tuple instead of tkfont.Font object for create_text
        canvas.create_text(60, 25, text=text, fill="#ffffff", font="Arial 14 bold")

        # Bind click event
        canvas.bind("<Button-1>", lambda e: command())

        return frame


class WelcomePage(tk.Frame):
    def __init__(self, master: App):
        super().__init__(master, bg="#2e2e2e")

        # Header
        header = tk.Label(
            self,
            text="Eve Online PI Calculator",
            font="Arial 24 bold",
            fg="#ffffff",
            bg="#2e2e2e"
        )
        header.pack(pady=50)

        # Start Button
        start_button = master.create_rounded_button(
            self,
            text="Start",
            command=lambda: master.show_frame(TierScreen)
        )
        start_button.pack(pady=20)


class TierScreen(tk.Frame):
    def __init__(self, master: App):
        super().__init__(master, bg="#2e2e2e")

        # Header
        header = tk.Label(
            self,
            text="Select a Tier",
            font="Arial 24 bold",
            fg="#ffffff",
            bg="#2e2e2e"
        )
        header.pack(pady=50)

        # Tier Buttons
        tiers: list[tuple[str, Type[tk.Frame]]] = [("P1", P1Screen), ("P2", P2Screen), ("P3", P3Screen), ("P4", P4Screen)]
        for tier, screen in tiers:
            tier_button = master.create_rounded_button(
                self,
                text=tier,
                command=lambda t=tier, s=screen: self.handle_tier_button(master, t, s)
            )
            tier_button.pack(pady=10)

        # Quit Button
        quit_button = master.create_rounded_button(
            self,
            text="Quit",
            command=master.quit
        )
        quit_button.pack(pady=20)

    def handle_tier_button(self, master: App, tier: str, screen: Type[tk.Frame]) -> None:
        # Update the selected tier label in the target frame
        if tier == "P1":
            frame = master.frames[P1Screen]
            if isinstance(frame, P1Screen):
                frame.update_selected_tier_label(tier)
        # Navigate to the selected screen
        master.show_frame(screen)


class P1Screen(tk.Frame):
    def __init__(self, master: App):
        super().__init__(master, bg="#2e2e2e")

        # Label to display the selected tier
        self.selected_tier_label = tk.Label(
            self,
            text="Selected Tier: P1",
            font="Arial 16",
            fg="#ffffff",
            bg="#2e2e2e"
        )
        self.selected_tier_label.pack(pady=10)

        # Header row with P buttons
        button_row = tk.Frame(self, bg="#2e2e2e")
        button_row.pack(pady=20)

        # Navigation Buttons
        tiers: list[tuple[str, Optional[Type[tk.Frame]]]] = [("P1", P1Screen), ("P2", P2Screen), ("P3", P3Screen), ("P4", P4Screen)]
        for text, screen in tiers:
            button = master.create_rounded_button(
                button_row,
                text=text,
                command=lambda t=text, s=screen: self.navigate_to_tier(master, t, s)
            )
            button.pack(side=tk.LEFT, padx=10)

        # Add the first box
        self.box1 = Canvas(self, width=500, height=200, bg="#2e2e2e", highlightthickness=0)
        self.box1.pack(pady=11)
        self.box1.create_rectangle(5, 5, 495, 195, fill="#444444", outline="#ffffff", width=2)

        # Add a button row between the two boxes
        button_row = tk.Frame(self, bg="#2e2e2e")
        button_row.pack(pady=8)  # Reduced padding by 15% (9 -> 8)

        calculate_button = master.create_rounded_button(
            button_row,
            text="Calculate",
            command=self.calculate_action
        )
        calculate_button.pack(side=tk.LEFT, padx=10)

        clear_button = master.create_rounded_button(
            button_row,
            text="Clear",
            command=self.clear_action
        )
        clear_button.pack(side=tk.LEFT, padx=10)

        # Add the second box
        self.box2 = Canvas(self, width=500, height=200, bg="#2e2e2e", highlightthickness=0)
        self.box2.pack(pady=11)  # Reduced padding by 15% (13 -> 11)
        self.box2.create_rectangle(5, 5, 495, 195, fill="#555555", outline="#ffffff", width=2)

    def navigate_to_tier(self, master: App, tier: str, screen: Optional[Type[tk.Frame]]) -> None:
        # Update the selected tier label and load the P1 list if applicable
        self.selected_tier_label.config(text=f"Selected Tier: {tier}")
        if tier == "P1":
            self.load_p1_list()
        if screen:
            master.show_frame(screen)

    def load_p1_list(self) -> None:
        try:
            # Load the P1 list from the JSON file
            with open("/Users/rathon/Library/CloudStorage/OneDrive-NursingWithAPurpose/Development/Eve-PI-GUI-Calclator/pi_p4_data.json", "r") as file:
                data = json.load(file)
                p1_list = data.get("TIERS", {}).get("P1", [])
                # Clear the box and display the P1 list
                self.box1.delete("all")
                self.box1.create_rectangle(5, 5, 495, 195, fill="#444444", outline="#ffffff", width=2)
                self.box1.create_text(
                    250, 10,  # Start near the top of the box
                    text="\n".join(p1_list),
                    fill="#ffffff",
                    font="Arial 10",
                    justify="center",
                    anchor="n"  # Align text to the top
                )
        except FileNotFoundError:
            self.display_error("JSON file not found.")
        except json.JSONDecodeError:
            self.display_error("Error decoding JSON file.")

    def display_error(self, message: str) -> None:
        # Display an error message in the box
        self.box1.delete("all")
        self.box1.create_rectangle(5, 5, 495, 195, fill="#444444", outline="#ffffff", width=2)
        self.box1.create_text(
            250, 100,
            text=message,
            fill="#ff0000",
            font="Arial 12",
            justify="center"
        )

    def calculate_action(self) -> None:
        # Placeholder for the Calculate button action
        print("Calculate button clicked")

    def clear_action(self) -> None:
        # Placeholder for the Clear button action
        print("Clear button clicked")

    def update_selected_tier_label(self, tier: str) -> None:
        # Update the selected tier label
        self.selected_tier_label.config(text=f"Selected Tier: {tier}")


class P2Screen(P1Screen):
    def __init__(self, master: App):
        super().__init__(master)

        # Duplicate the boxes
        box1 = Canvas(self, width=500, height=200, bg="#2e2e2e", highlightthickness=0)
        box1.pack(pady=11)  # Reduced padding by 15% (13 -> 11)
        box1.create_rectangle(5, 5, 495, 195, fill="#444444", outline="#ffffff", width=2)

        box2 = Canvas(self, width=500, height=200, bg="#2e2e2e", highlightthickness=0)
        box2.pack(pady=11)  # Reduced padding by 15% (13 -> 11)
        box2.create_rectangle(5, 5, 495, 195, fill="#555555", outline="#ffffff", width=2)


class P3Screen(P1Screen):
    def __init__(self, master: App):
        super().__init__(master)

        # Duplicate the boxes
        box1 = Canvas(self, width=500, height=200, bg="#2e2e2e", highlightthickness=0)
        box1.pack(pady=11)  # Reduced padding by 15% (13 -> 11)
        box1.create_rectangle(5, 5, 495, 195, fill="#444444", outline="#ffffff", width=2)

        box2 = Canvas(self, width=500, height=200, bg="#2e2e2e", highlightthickness=0)
        box2.pack(pady=11)  # Reduced padding by 15% (13 -> 11)
        box2.create_rectangle(5, 5, 495, 195, fill="#555555", outline="#ffffff", width=2)


class P4Screen(P1Screen):
    def __init__(self, master: App):
        super().__init__(master)

        # Duplicate the boxes
        box1 = Canvas(self, width=500, height=200, bg="#2e2e2e", highlightthickness=0)
        box1.pack(pady=11)  # Reduced padding by 15% (13 -> 11)
        box1.create_rectangle(5, 5, 495, 195, fill="#444444", outline="#ffffff", width=2)

        box2 = Canvas(self, width=500, height=200, bg="#2e2e2e", highlightthickness=0)
        box2.pack(pady=11)  # Reduced padding by 15% (13 -> 11)
        box2.create_rectangle(5, 5, 495, 195, fill="#555555", outline="#ffffff", width=2)


if __name__ == "__main__":
    app = App()
    app.mainloop()
