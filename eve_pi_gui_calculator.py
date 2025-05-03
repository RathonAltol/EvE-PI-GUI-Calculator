import json
import tkinter as tk
from tkinter import scrolledtext

# Load P4 to P1 data from JSON file
try:
    with open('pi_p4_data.json', 'r') as f:
        p4_data = json.load(f)
except FileNotFoundError:
    raise SystemExit("Error: 'pi_p4_data.json' file not found. Please ensure it is in the same directory.")

# Hardcoded list of 8 P4 items
p4_items = [
    "Broadcast Node",
    "Integrity Response Drones",
    "Nano-Factory",
    "Organic Mortar Applicators",
    "Recursive Computing Module",
    "Self-Harmonizing Power Core",
    "Sterile Conduits",
    "Wetware Mainframe"
]

# Create main application window
root = tk.Tk()
root.title("EVE PI P4 -> P1 Calculator")

# Use a frame to hold the list of items and entries
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10, anchor='w')

entries = {}

for item in p4_items:
    row_frame = tk.Frame(input_frame)
    row_frame.pack(fill='x', pady=2)
    tk.Label(row_frame, text=item, width=30, anchor='w').pack(side='left')
    qty_entry = tk.Entry(row_frame, width=6)
    qty_entry.pack(side='left', padx=5)
    qty_entry.insert(0, "75")
    entries[item] = qty_entry

def calculate_requirements():
    output_area.delete('1.0', tk.END)
    total_p1 = {}
    output_lines = []
    input_errors = []

    def recurse(item_name, amount_needed):
        if item_name not in p4_data:
            # It's a P1 material
            total_p1[item_name] = total_p1.get(item_name, 0) + amount_needed
            return
        item_data = p4_data[item_name]
        output_qty = item_data.get('output_qty', 1)
        inputs = item_data.get('inputs', {})
        multiplier = amount_needed / output_qty
        for input_name, input_qty in inputs.items():
            recurse(input_name, input_qty * multiplier)

    for item, entry in entries.items():
        qty_text = entry.get().strip()
        if qty_text == "":
            quantity = 0
        else:
            try:
                quantity = int(qty_text)
            except ValueError:
                quantity = 0
                input_errors.append(item)
        if quantity < 0:
            input_errors.append(item)
            quantity = 0

        if quantity > 0:
            output_lines.append(f"{item} ({quantity} units) requires:")
            temp_p1 = {}
            def local_recurse(name, amt):
                if name not in p4_data:
                    temp_p1[name] = temp_p1.get(name, 0) + amt
                    return
                data = p4_data[name]
                out_qty = data.get('output_qty', 1)
                inputs = data.get('inputs', {})
                multiplier = amt / out_qty
                for sub_input, sub_amt in inputs.items():
                    local_recurse(sub_input, sub_amt * multiplier)
            local_recurse(item, quantity)
            for p1_name, req_amount in temp_p1.items():
                output_lines.append(f" - {p1_name}: {int(req_amount)}")
                total_p1[p1_name] = total_p1.get(p1_name, 0) + req_amount
            output_lines.append("")
        else:
            output_lines.append(f"{item} (0 units) requires no P1 materials.")
            output_lines.append("")

    output_lines.append("Total P1 materials required for all selected P4s:")
    if total_p1:
        for p1_name, total_amount in total_p1.items():
            output_lines.append(f" - {p1_name}: {int(total_amount)}")
    else:
        output_lines.append(" - None (no P4 items selected).")

    if input_errors:
        output_lines.append("")
        output_lines.append("(*) Note: Non-numeric or invalid inputs were detected for: "
                            + ", ".join(input_errors) + ". Treated as 0.")

    output_area.delete('1.0', tk.END)
    output_area.insert(tk.END, "\n".join(output_lines))

# Create Calculate button and output area AFTER function definition
calc_button = tk.Button(root, text="Calculate", command=calculate_requirements)
calc_button.pack(pady=5)

output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
output_area.pack(padx=10, pady=10, fill='both', expand=True)
output_area.insert(tk.END, "Enter quantities and click Calculate to see required P1 materials.\n")

root.mainloop()
