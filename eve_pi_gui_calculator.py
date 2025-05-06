import json
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk

# ----------------------- CONSTANTS -----------------------

P4_ITEMS = [
    "Broadcast Node",
    "Integrity Response Drones",
    "Nano-Factory",
    "Organic Mortar Applicators",
    "Recursive Computing Module",
    "Self-Harmonizing Power Core",
    "Sterile Conduits",
    "Wetware Mainframe"
]

IMAGE_DIR = "Images"
JSON_FILE = "pi_p4_data.json"

# ----------------------- LOAD DATA -----------------------

try:
    with open(JSON_FILE, 'r') as f:
        p4_data = json.load(f)
except FileNotFoundError:
    raise SystemExit(f"Error: '{JSON_FILE}' file not found.")

# ----------------------- INITIALIZE TK -----------------------

root = tk.Tk()
root.title("EVE PI P4 → P1 Calculator")

selected_p4 = {item: tk.BooleanVar(value=False) for item in P4_ITEMS}
entries = {}
p4_images = {}

# ----------------------- LOAD IMAGES (PRESERVE ASPECT RATIO) -----------------------

for item in P4_ITEMS:
    try:
        img = Image.open(f"{IMAGE_DIR}/{item}.png")
        img.thumbnail((50, 50), Image.Resampling.LANCZOS)
        p4_images[item] = ImageTk.PhotoImage(img)
    except FileNotFoundError:
        p4_images[item] = None

# ----------------------- UI COMPONENTS -----------------------

dropdown_frame = tk.Frame(root)
dropdown_frame.pack(padx=10, pady=10, anchor='n')

dropdown_menu = tk.Frame(root, relief=tk.RAISED, borderwidth=1)  # Removed fixed width
dropdown_menu.pack_propagate(True)  # Allow resizing based on child widgets
button_frame = tk.Frame(root)
input_frame = tk.Frame(root)
output_frame = tk.Frame(root)

output_area = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=60, height=20)
output_area.pack(padx=10, pady=10, fill='both', expand=True)
output_area.insert(tk.END, "Enter quantities and click Calculate to see required P1 materials.\n")

button_frame.pack(pady=10)
output_frame.pack(padx=10, pady=10, fill='both', expand=True)

# ----------------------- FUNCTIONS -----------------------

def build_input_fields():
    for widget in input_frame.winfo_children():
        widget.destroy()
    for item, is_selected in selected_p4.items():
        if is_selected.get():
            row = tk.Frame(input_frame)
            row.pack(fill='x', pady=2)

            img = p4_images[item]
            if img:
                tk.Label(row, image=img).pack(side='left', padx=5)
            else:
                tk.Label(row, text="[No Image]", width=10).pack(side='left', padx=5)

            tk.Label(row, text=item, width=30, anchor='w').pack(side='left')

            qty_entry = tk.Entry(row, width=6)
            qty_entry.insert(0, "0")
            qty_entry.pack(side='left', padx=5)
            entries[item] = qty_entry
    input_frame.pack(padx=10, pady=10, anchor='center')

def toggle_dropdown():
    """Toggle visibility of dropdown menu."""
    if dropdown_menu.winfo_ismapped():
        dropdown_menu.pack_forget()
    else:
        # Ensure dropdown menu is packed and visible
        dropdown_menu.pack(padx=10, pady=10, anchor='center', before=button_frame)

def calculate_requirements():
    """Calculate P1 material requirements and display results."""
    output_area.delete('1.0', tk.END)
    total_p1, output_lines, input_errors = {}, [], []
    p4_totals = {}  # Store total P1 materials for each individual P4 item

    def recurse(item_name, qty_needed, p4_item=None):
        """Recursively calculate P1 material requirements."""
        if item_name not in p4_data:
            total_p1[item_name] = total_p1.get(item_name, 0) + qty_needed
            if p4_item:
                p4_totals[p4_item][item_name] = p4_totals[p4_item].get(item_name, 0) + qty_needed
            return
        data = p4_data[item_name]
        multiplier = qty_needed / data.get('output_qty', 1)
        for input_item, input_qty in data.get('inputs', {}).items():
            recurse(input_item, input_qty * multiplier, p4_item)

    total_p4_qty = 0  # Track the total quantity of all selected P4 items

    for item, is_selected in selected_p4.items():
        if is_selected.get():
            try:
                qty = int(entries[item].get().strip())
            except ValueError:
                qty = 0
                input_errors.append(item)

            if qty > 0:
                total_p4_qty += qty  # Add to the total P4 quantity
                output_lines.append(f"{item} ({qty} units) requires:")
                p4_totals[item] = {}  # Initialize P1 totals for this P4 item
                recurse(item, qty, p4_item=item)
                for p1_name, p1_qty in p4_totals[item].items():
                    output_lines.append(f"   - {p1_name}: {int(p1_qty)}")
            else:
                output_lines.append(f"{item} (0 units) requires no P1 materials.")

    output_lines.append("\nCalculated Totals for the P1 materials needed for the Tier of PI you selected:")
    if total_p1:
        for name, amt in total_p1.items():
            output_lines.append(f" - {name}: {int(amt)}")
    else:
        output_lines.append(" - None (no P4 items selected).")

    output_lines.append(f"\nTotal quantity of all selected P4 items: {total_p4_qty}")

    if input_errors:
        output_lines.append("\nInvalid inputs for: " + ", ".join(input_errors))

    output_area.insert(tk.END, "\n".join(output_lines))

def clear_inputs():
    """Reset input fields, uncheck all selected P4 items, clear the output area, and hide the P4 list."""
    # Remove all quantity boxes
    for entry in entries.values():
        entry.destroy()  # Remove the quantity box widget
    entries.clear()  # Clear the entries dictionary

    # Uncheck all checkboxes
    for item in selected_p4.values():
        item.set(False)

    # Clear the output area
    output_area.delete('1.0', tk.END)
    output_area.insert(tk.END, "Enter quantities and click Calculate to see required P1 materials.\n")

    # Hide the dropdown menu
    dropdown_menu.pack_forget()

    # Clear the input frame (reset to initial state)
    for widget in input_frame.winfo_children():
        widget.destroy()

def toggle_quantity_box(item, row):
    """Show or hide the quantity box next to the selected P4 item."""
    if selected_p4[item].get():
        # Create and show the quantity box next to the selected P4 item
        qty_entry = tk.Entry(row, width=6)
        qty_entry.pack(side='left', padx=5)
        qty_entry.insert(0, "0")
        entries[item] = qty_entry
    else:
        # Remove the quantity box if it exists
        if item in entries:
            entries[item].destroy()
            del entries[item]

# ----------------------- UI BUILD -----------------------

button_container = tk.Frame(dropdown_frame)  # Container to center all buttons
button_container.pack(anchor='center', pady=10)

# Add "Select P2 Items" button
tk.Button(button_container, text="Select P2 Items", command=lambda: print("Select P2 Items clicked")).pack(side='left', padx=5)

# Add "Select P3 Items" button
tk.Button(button_container, text="Select P3 Items", command=lambda: print("Select P3 Items clicked")).pack(side='left', padx=5)

# Add "Select P4 Items" button
tk.Button(button_container, text="Select P4 Items", command=toggle_dropdown).pack(side='left', padx=5)

# Create dropdown menu with checkboxes, images, and quantity boxes
for item in P4_ITEMS:
    row = tk.Frame(dropdown_menu)
    row.pack(fill='x', pady=2)

    # Display image if available
    img = p4_images[item]
    if img:
        tk.Label(row, image=img).pack(side='left', padx=5)
    else:
        tk.Label(row, text="[No Image]", width=10).pack(side='left', padx=5)

    # Checkbox for selecting the P4 item
    tk.Checkbutton(row, text=item, variable=selected_p4[item], 
                   command=lambda i=item, r=row: toggle_quantity_box(i, r)).pack(side='left', anchor='w')

tk.Button(button_frame, text="Calculate", command=calculate_requirements).pack(side='left', padx=5)
tk.Button(button_frame, text="Clear", command=clear_inputs).pack(side='left', padx=5)

# ----------------------- MAIN LOOP -----------------------
root.mainloop()
