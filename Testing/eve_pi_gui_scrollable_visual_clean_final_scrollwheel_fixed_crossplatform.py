
import tkinter as tk
from tkinter import ttk
import json
import os
from PIL import Image, ImageTk

with open("pi_p4_data.json") as f:
    DATA = json.load(f)
    PI_DATA = DATA["PI_DATA"]
    TIERS = DATA["TIERS"]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EVE PI Calculator")
        self.geometry("600x700")
        self.frames = {}

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        for F in (WelcomeScreen, CalculationScreen):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomeScreen")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        center_frame = tk.Frame(self)
        center_frame.grid(row=1, column=1, padx=20)

        tk.Label(center_frame, text="EVE PI Calculator", font=("Arial", 24)).pack(pady=20)
        tk.Button(center_frame, text="Start", font=("Arial", 14), width=12,
                  command=lambda: controller.show_frame("CalculationScreen")).pack()

class CalculationScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.images = []

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10, anchor="center")
        self.tier_buttons = {}

        for tier in ["P1", "P2", "P3", "P4"]:
            btn = tk.Button(self.button_frame, text=tier, width=6,
                            command=lambda t=tier: self.load_tier(t))
            btn.pack(side=tk.LEFT, padx=10)
            self.tier_buttons[tier] = btn

        self.material_container = tk.LabelFrame(self, text="Select Materials")
        self.material_container.pack(fill="both", expand=True, padx=40, pady=5, anchor="center")
        self.canvas = tk.Canvas(self.material_container)
        self.scrollbar = tk.Scrollbar(self.material_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        
        # Enable mousewheel scrolling on multiple OS
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_mousewheel_linux(event):
            self.canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<Button-4>", _on_mousewheel_linux))
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<Button-5>", _on_mousewheel_linux))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<Button-4>"))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<Button-5>"))
    

        self.button_row = tk.Frame(self)
        self.button_row.pack(pady=5, anchor="center")
        tk.Button(self.button_row, text="Calculate", command=self.calculate).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_row, text="Clear", command=self.clear_selections).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_row, text="Return to Welcome", command=lambda: controller.show_frame("WelcomeScreen")).pack(side=tk.LEFT, padx=5)

        self.output_frame = tk.LabelFrame(self, text="Calculation Output")
        self.output_frame.pack(fill="both", expand=True, padx=40, pady=5, anchor="center")
        self.output_display = tk.Text(self.output_frame, height=12, font=("Courier", 10), wrap="none")
        self.output_scroll = tk.Scrollbar(self.output_frame, command=self.output_display.yview)
        self.output_display.configure(yscrollcommand=self.output_scroll.set)
        self.output_display.pack(side="left", fill="both", expand=True)
        self.output_scroll.pack(side="right", fill="y")

        self.selection_data = {}
        self.current_tier = None

    def _accumulate_until_tier(self, target, item, qty, target_tier):
        if item not in PI_DATA:
            return
        inputs = PI_DATA[item].get("inputs", {})
        for name, base_amt in inputs.items():
            total_amt = base_amt * qty
            if name in TIERS[target_tier]:
                target[name] = target.get(name, 0) + total_amt
            else:
                self._accumulate_until_tier(target, name, total_amt, target_tier)


    def load_tier(self, tier):
        self.current_tier = tier
        self.output_display.delete(1.0, tk.END)
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.selection_data = {}
        self.images.clear()

        items = TIERS[tier]

        for item in items:
            row = tk.Frame(self.scrollable_frame)
            row.pack(anchor="w", pady=2)

            var = tk.BooleanVar()
            chk = tk.Checkbutton(row, variable=var)
            chk.pack(side="left")

            img_path = f"images/{item}.png"
            if os.path.exists(img_path):
                img = Image.open(img_path).resize((32, 32))
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(row, image=photo)
                img_label.image = photo
                img_label.pack(side="left", padx=5)
                self.images.append(photo)
            else:
                tk.Label(row, text="[No Image]").pack(side="left", padx=5)

            tk.Label(row, text=item, width=30, anchor="w").pack(side="left", padx=5)

            entry_container = tk.Frame(row)
            entry_container.pack(side="left", padx=5)
            entry_container.pack_forget()

            qty_entry = tk.Entry(entry_container, width=6)
            qty_entry.insert(0, "0")
            qty_entry.pack()
            qty_entry.bind("<Return>", lambda event: self.calculate())

            def make_toggle_callback(v=var, c=entry_container, e=qty_entry):
                def callback():
                    if v.get():
                        c.pack(side="left", padx=5)
                        e.focus()
                        e.selection_range(0, tk.END)
                    else:
                        c.pack_forget()
                return callback

            chk.config(command=make_toggle_callback())

            self.selection_data[item] = (var, qty_entry)

    def clear_selections(self):
        self.output_display.delete(1.0, tk.END)
        for var, entry in self.selection_data.values():
            var.set(False)
            entry.delete(0, tk.END)
            entry.insert(0, "0")

    
    def calculate(self):
        if not self.current_tier:
            return

        results = {}
        skipped_items = []

        for item, (var, entry) in self.selection_data.items():
            if var.get():
                try:
                    qty = int(entry.get())
                    if qty <= 0:
                        continue
                except ValueError:
                    continue

                if item not in PI_DATA:
                    skipped_items.append(item)
                    continue

                if self.current_tier == "P1":
                    self._accumulate_until_tier(results, item, qty, "P0")
                else:
                    self._accumulate_until_tier(results, item, qty, "P1")

        self.output_display.delete(1.0, tk.END)
        if skipped_items:
            self.output_display.insert(tk.END, "[Skipped items with no PI_DATA entries:]\n")
            for s_item in skipped_items:
                self.output_display.insert(tk.END, f"- {s_item}\n")

        for key, val in results.items():
            self.output_display.insert(tk.END, f"{val} x {key}\n")


if __name__ == "__main__":
    app = App()
    app.mainloop()
