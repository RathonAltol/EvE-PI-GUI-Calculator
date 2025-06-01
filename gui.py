import tkinter as tk
from tkinter import scrolledtext, Entry, Checkbutton, IntVar
from PIL import Image, ImageTk
from pi_data import TIERS, PI_DATA, calculate_p1_requirements, recurse_requirements
from collections import defaultdict
import os

class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Welcome to the EVE PI Calculator", font=("Arial", 24)).pack(pady=40)
        tk.Label(self, text="Click Start to begin", font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="Start", command=lambda: controller.show_frame("TierSelectionScreen")).pack(pady=20)

class TierSelectionScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        wrapper = tk.Frame(self)
        wrapper.place(relx=0.5, rely=0.5, anchor="center")
        button_frame = tk.Frame(wrapper)
        button_frame.pack(pady=(0, 20))
        for tier in ["P1", "P2", "P3", "P4"]:
            tk.Button(button_frame, text=tier, width=6,
                      command=lambda t=tier: controller.frames["CalculationScreen"].load_tier(t)).pack(side=tk.LEFT, padx=10)
        tk.Button(wrapper, text="Return to Welcome", command=lambda: controller.show_frame("WelcomeScreen")).pack()

class CalculationScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_items = {}
        self.selected_tier = None
        self.tier_label = tk.Label(self, text="", font=("Arial", 12))
        self.tier_label.pack(pady=(10, 0))
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=(2, 10))
        self.tier_buttons = {}
        for tier in ['P1', 'P2', 'P3', 'P4']:
            btn = tk.Button(self.button_frame, text=tier, width=6,
                          command=lambda t=tier: self.load_tier(t))
            btn.pack(side=tk.LEFT, padx=5)
            self.tier_buttons[tier] = btn
        self.button_frame.pack(pady=(2, 10))
        self.selection_frame = tk.LabelFrame(self, text="Select Materials", padx=10, pady=10)
        self.selection_frame.pack(padx=(20, 10), pady=(5, 10), fill="both", expand=True)
        self.canvas = tk.Canvas(self.selection_frame, height=275, relief="flat", bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.selection_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas)
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        def _on_mousewheel_linux_up(event):
            self.canvas.yview_scroll(-1, "units")
        def _on_mousewheel_linux_down(event):
            self.canvas.yview_scroll(1, "units")
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind("<MouseWheel>", _on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind("<MouseWheel>"))
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind("<Button-4>", _on_mousewheel_linux_up))
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind("<Button-5>", _on_mousewheel_linux_down))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind("<Button-4>"))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind("<Button-5>"))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y", padx=(0, 0))
        action_frame = tk.Frame(self)
        action_frame.pack(pady=(0, 10))
        button_wrapper = tk.Frame(action_frame)
        button_wrapper.pack()
        tk.Button(button_wrapper, text="Calculate", command=self.calculate).pack(side=tk.LEFT, padx=10)
        tk.Button(button_wrapper, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=10)
        self.output_frame = tk.LabelFrame(self, text="Output", padx=10, pady=10)
        self.output_frame.pack(padx=20, pady=(0, 10), fill="both", expand=True)
        self.output_display = scrolledtext.ScrolledText(self.output_frame, wrap=tk.WORD, height=8)
        self.output_display.pack(fill="both", expand=True)
        tk.Button(self, text="Return to Welcome", command=lambda: controller.show_frame("WelcomeScreen")).pack(pady=(0, 10))

    def load_tier(self, tier):
        self.tier_label.config(text=f"Current Tier: {tier}")
        self.tier_label.pack_configure(pady=(20, 5))
        for t, btn in self.tier_buttons.items():
            if t == tier:
                btn.config(state='disabled', foreground=btn['bg'], relief='flat')
            else:
                btn.config(state='normal', foreground='black', relief='raised')
        self.controller.geometry("640x720")
        self.controller.show_frame("CalculationScreen")
        self.selected_tier = tier
        self.selected_items = {}
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        for item in sorted(TIERS[tier]):
            row = tk.Frame(self.scroll_frame)
            row.pack(fill="x", pady=2)
            var = IntVar()
            entry = Entry(row, width=6)
            entry.pack(side="left", padx=5)
            entry.pack_forget()
            entry.insert(0, "0")
            entry.select_range(0, "end")
            entry.bind("<Return>", lambda event: self.calculate())
            def toggle_entry(v=var, e=entry):
                if v.get():
                    e.pack(side="left", padx=5)
                    e.focus()
                    e.select_range(0, "end")
            chk = Checkbutton(row, variable=var, command=toggle_entry)
            chk.pack(side="left")
            img_path = os.path.join("images", f"{item}.png")
            if os.path.exists(img_path):
                image = Image.open(img_path).resize((32, 32))
                photo = ImageTk.PhotoImage(image)
                lbl_img = tk.Label(row, image=photo)
                lbl_img.image = photo
                lbl_img.pack(side="left", padx=5)
            tk.Label(row, text=item, width=35, anchor="w").pack(side="left")
            self.selected_items[item] = {"var": var, "entry": entry}

    def calculate(self):
        self.output_display.delete(1.0, tk.END)
        p1_totals = defaultdict(float)
        p0_totals = defaultdict(float)
        output = []
        for item, meta in self.selected_items.items():
            if meta["var"].get():
                try:
                    qty = int(meta["entry"].get())
                    if self.selected_tier == "P1":
                        for p0, total in calculate_p1_requirements(item, qty):
                            output.append(f"{item} requires {total} {p0}")
                except ValueError:
                    output.append(f"{item}: INVALID INPUT")
        if self.selected_tier != "P1":
            for item, meta in self.selected_items.items():
                if meta["var"].get():
                    try:
                        qty = int(meta["entry"].get())
                        recurse_requirements(item, qty, p1_totals, p0_totals)
                    except ValueError:
                        output.append(f"{item}: INVALID INPUT")
            output.append("\nTotal P1 materials required:")
            for p1, amt in sorted(p1_totals.items()):
                output.append(f"  - {p1}: {int(amt)}")
        if self.selected_tier == "P1" and not output:
            output.append("No valid items selected.")
        elif self.selected_tier != "P1" and not p1_totals:
            output.append("No valid items selected.")
        self.output_display.insert(tk.END, "\n".join(output))

    def clear(self):
        self.output_display.delete(1.0, tk.END)
        for item in self.selected_items.values():
            item["var"].set(0)
            item["entry"].delete(0, tk.END)
            item["entry"].insert(0, "0")
