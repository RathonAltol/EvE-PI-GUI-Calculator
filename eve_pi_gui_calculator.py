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

P3_ITEMS = [
    "Biotech Research Reports",
    "Camera Drones",
    "Condensates",
    "Cryoprotectant Solution",
    "Data Chips",
    "Gel-Matrix Biopaste",
    "Guidance Systems",
    "Hazmat Detection Systems",
    "Hermetic Membranes",
    "High-Tech Transmitters",
    "Industrial Explosives",
    "Neocoms",
    "Nuclear Reactors",
    "Planetary Vehicles",
    "Robotics",
    "Smartfab Units",
    "Supercomputers",
    "Sythetic Synapses",
    "Transcranial Microcontrollers",
    "Ukomi Super Conductors",
    "Vaccines"
]

P2_ITEMS = [
    "Biocells",
    "Construction Blocks",
    "Consumer Electronics",
    "Coolant",
    "Enriched Uranium",
    "Fertilizer",
    "Genetically Enhanced Livestock",
    "Livestock",
    "Mechanical Parts",
    "Microfiber Shielding",
    "Minature Electronics",
    "Nanites",
    "Oxides",
    "Polyaramids",
    "Polytextiles",
    "Rocket Fuel",  # Fixed spelling from "Rocket Fule"
    "Silicate Glass",
    "Superconductors",
    "Supertensile Plastics",
    "Synthetic Oil",
    "Test Cultures",
    "Transmitter",
    "Viral Agent",
    "Water-Cooled CPU"
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
root.geometry("800x600")  # Set default window size

selected_p4 = {item: tk.BooleanVar(value=False) for item in P4_ITEMS}
selected_p2 = {item: tk.BooleanVar(value=False) for item in P2_ITEMS}
selected_p3 = {item: tk.BooleanVar(value=False) for item in P3_ITEMS}
entries = {}
p4_images = {}
p2_images = {}
p3_images = {}

# ----------------------- LOAD IMAGES (PRESERVE ASPECT RATIO) -----------------------

for item in P4_ITEMS:
    try:
        img = Image.open(f"{IMAGE_DIR}/{item}.png")
        img.thumbnail((50, 50), Image.Resampling.LANCZOS)
        p4_images[item] = ImageTk.PhotoImage(img)
    except FileNotFoundError:
        p4_images[item] = None

for item in P3_ITEMS:
    try:
        img = Image.open(f"{IMAGE_DIR}/{item}.png")
        img.thumbnail((50, 50), Image.Resampling.LANCZOS)
        p3_images[item] = ImageTk.PhotoImage(img)
    except FileNotFoundError:
        p3_images[item] = None

for item in P2_ITEMS:
    try:
        img = Image.open(f"{IMAGE_DIR}/{item}.png")
        img.thumbnail((50, 50), Image.Resampling.LANCZOS)
        p2_images[item] = ImageTk.PhotoImage(img)
    except FileNotFoundError:
        p2_images[item] = None

# ----------------------- UI COMPONENTS -----------------------

dropdown_frame = tk.Frame(root)
dropdown_frame.pack(padx=10, pady=10, anchor='n')

dropdown_menu = tk.Frame(root, relief=tk.RAISED, borderwidth=1)  # Removed fixed width
dropdown_menu.pack_propagate(True)  # Allow resizing based on child widgets
p2_dropdown_menu = tk.Frame(root, relief=tk.RAISED, borderwidth=1)
p2_dropdown_menu.pack_propagate(True)
p3_dropdown_menu = tk.Frame(root, relief=tk.RAISED, borderwidth=1)
p3_dropdown_menu.pack_propagate(True)
button_frame = tk.Frame(root)
input_frame = tk.Frame(root)
output_frame = tk.Frame(root)

output_area = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=60, height=20)
output_area.pack(padx=10, pady=10, fill='both', expand=True)
output_area.insert(tk.END, "Enter quantities and click Calculate to see required P1 materials.\n")

button_frame.pack(pady=10)
output_frame.pack(padx=10, pady=10, fill='both', expand=True)

# Add scrollable dropdown menus for P2, P3, and P4
p4_scrollbar = tk.Scrollbar(dropdown_menu, orient=tk.VERTICAL)
p4_canvas = tk.Canvas(dropdown_menu, yscrollcommand=p4_scrollbar.set, height=300)  # Limit height
p4_scrollbar.config(command=p4_canvas.yview)
p4_scrollbar.pack(side='right', fill='y')
p4_canvas.pack(side='left', fill='both', expand=True)
p4_inner_frame = tk.Frame(p4_canvas)
p4_canvas.create_window((0, 0), window=p4_inner_frame, anchor='nw')

p2_scrollbar = tk.Scrollbar(p2_dropdown_menu, orient=tk.VERTICAL)
p2_canvas = tk.Canvas(p2_dropdown_menu, yscrollcommand=p2_scrollbar.set, height=300)  # Limit height
p2_scrollbar.config(command=p2_canvas.yview)
p2_scrollbar.pack(side='right', fill='y')
p2_canvas.pack(side='left', fill='both', expand=True)
p2_inner_frame = tk.Frame(p2_canvas)
p2_canvas.create_window((0, 0), window=p2_inner_frame, anchor='nw')

p3_scrollbar = tk.Scrollbar(p3_dropdown_menu, orient=tk.VERTICAL)
p3_canvas = tk.Canvas(p3_dropdown_menu, yscrollcommand=p3_scrollbar.set, height=300)  # Limit height
p3_scrollbar.config(command=p3_canvas.yview)
p3_scrollbar.pack(side='right', fill='y')
p3_canvas.pack(side='left', fill='both', expand=True)
p3_inner_frame = tk.Frame(p3_canvas)
p3_canvas.create_window((0, 0), window=p3_inner_frame, anchor='nw')

# Update scroll region when content changes
def update_scroll_region(canvas, inner_frame):
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Enable mouse wheel scrolling for P2, P3, and P4 dropdowns
def bind_mouse_wheel(canvas):
    def _on_mousewheel(event):
        # Windows and MacOS
        if event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            canvas.yview_scroll(1, "units")
    # Windows and MacOS
    canvas.bind("<Enter>", lambda _: (
        canvas.bind_all("<MouseWheel>", _on_mousewheel),
        canvas.bind_all("<Button-4>", _on_mousewheel),
        canvas.bind_all("<Button-5>", _on_mousewheel)
    ))
    canvas.bind("<Leave>", lambda _: (
        canvas.unbind_all("<MouseWheel>"),
        canvas.unbind_all("<Button-4>"),
        canvas.unbind_all("<Button-5>")
    ))

bind_mouse_wheel(p4_canvas)
bind_mouse_wheel(p2_canvas)
bind_mouse_wheel(p3_canvas)

# ----------------------- FUNCTIONS -----------------------

def build_input_fields():
    """Build input fields for selected items."""
    for widget in input_frame.winfo_children():
        widget.destroy()  # Clear existing widgets in the input frame
    entries.clear()  # Clear the entries dictionary to avoid stale data

    # Add input fields for selected P4 items
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
            entries[item] = qty_entry  # Add the entry widget to the dictionary

    # Add input fields for selected P2 items
    for item, is_selected in selected_p2.items():
        if is_selected.get():
            row = tk.Frame(input_frame)
            row.pack(fill='x', pady=2)

            img = p2_images[item]
            if img:
                tk.Label(row, image=img).pack(side='left', padx=5)
            else:
                tk.Label(row, text="[No Image]", width=10).pack(side='left', padx=5)

            tk.Label(row, text=item, width=30, anchor='w').pack(side='left')

            qty_entry = tk.Entry(row, width=6)
            qty_entry.insert(0, "0")
            qty_entry.pack(side='left', padx=5)
            entries[item] = qty_entry  # Add the entry widget to the dictionary

    # Add input fields for selected P3 items
    for item, is_selected in selected_p3.items():
        if is_selected.get():
            row = tk.Frame(input_frame)
            row.pack(fill='x', pady=2)

            img = p3_images[item]
            if img:
                tk.Label(row, image=img).pack(side='left', padx=5)
            else:
                tk.Label(row, text="[No Image]", width=10).pack(side='left', padx=5)

            tk.Label(row, text=item, width=30, anchor='w').pack(side='left')

            qty_entry = tk.Entry(row, width=6)
            qty_entry.insert(0, "0")
            qty_entry.pack(side='left', padx=5)
            entries[item] = qty_entry  # Add the entry widget to the dictionary

    input_frame.pack(padx=10, pady=10, anchor='center')

def hide_all_dropdowns():
    """Hide all dropdown menus."""
    dropdown_menu.pack_forget()
    p2_dropdown_menu.pack_forget()
    p3_dropdown_menu.pack_forget()

def clear_output_area():
    """Clear the output area."""
    output_area.delete('1.0', tk.END)
    output_area.insert(tk.END, "Enter quantities above and click Calculate to see required P1 materials.\n")

def reset_tier(selected_dict, entries_dict):
    """Reset all items for the selected tier of PI."""
    # Uncheck all checkboxes
    for var in selected_dict.values():
        var.set(False)
    # Clear all quantity boxes
    for entry in entries_dict.values():
        entry.destroy()
    entries_dict.clear()

def reset_window_geometry():
    """Reset the window to its default size and shape."""
    root.geometry("800x600")

def toggle_dropdown():
    """Toggle visibility of P4 dropdown menu."""
    if dropdown_menu.winfo_ismapped():
        dropdown_menu.pack_forget()
    else:
        hide_all_dropdowns()
        reset_tier(selected_p4, entries)  # Reset P4 items
        clear_output_area()  # Clear output area when switching to P4
        dropdown_menu.pack(padx=10, pady=10, anchor='center', before=button_frame)
    reset_window_geometry()  # Ensure default size

def toggle_p3_dropdown():
    """Toggle visibility of P3 dropdown menu."""
    if p3_dropdown_menu.winfo_ismapped():
        p3_dropdown_menu.pack_forget()
    else:
        hide_all_dropdowns()
        reset_tier(selected_p3, entries)  # Reset P3 items
        clear_output_area()  # Clear output area when switching to P3
        p3_dropdown_menu.pack(padx=10, pady=10, anchor='center', before=button_frame)
    reset_window_geometry()  # Ensure default size

def toggle_p2_dropdown():
    """Toggle visibility of P2 dropdown menu."""
    if p2_dropdown_menu.winfo_ismapped():
        p2_dropdown_menu.pack_forget()
    else:
        hide_all_dropdowns()
        reset_tier(selected_p2, entries)  # Reset P2 items
        clear_output_area()  # Clear output area when switching to P2
        p2_dropdown_menu.pack(padx=10, pady=10, anchor='center', before=button_frame)
    reset_window_geometry()  # Ensure default size

def calculate_requirements():
    """Calculate P1 material requirements and display results."""
    output_area.delete('1.0', tk.END)
    total_p1, breakdown_lines, total_lines, input_errors = {}, [], [], []
    p4_totals = {}  # Store total P1 materials for each individual P4 item
    p3_totals = {}  # Store total P1 materials for each individual P3 item
    p2_totals = {}  # Store total P1 materials for each individual P2 item

    def recurse(item_name, qty_needed, parent_item=None):
        """Recursively calculate P1 material requirements."""
        if item_name not in p4_data:
            total_p1[item_name] = total_p1.get(item_name, 0) + qty_needed
            if parent_item:
                if parent_item in p4_totals:
                    p4_totals[parent_item][item_name] = p4_totals[parent_item].get(item_name, 0) + qty_needed
                elif parent_item in p3_totals:
                    p3_totals[parent_item][item_name] = p3_totals[parent_item].get(item_name, 0) + qty_needed
                elif parent_item in p2_totals:
                    p2_totals[parent_item][item_name] = p2_totals[parent_item].get(item_name, 0) + qty_needed
            return
        data = p4_data[item_name]
        multiplier = qty_needed / data.get('output_qty', 1)
        for input_item, input_qty in data.get('inputs', {}).items():
            recurse(input_item, input_qty * multiplier, parent_item)

    # Determine which tier is currently selected
    if dropdown_menu.winfo_ismapped():
        tier_label = "P4 Items Selected"
    elif p3_dropdown_menu.winfo_ismapped():
        tier_label = "P3 Items Selected"
    elif p2_dropdown_menu.winfo_ismapped():
        tier_label = "P2 Items Selected"
    else:
        tier_label = "Items Selected"

    # Calculate for P4 items
    for item, is_selected in selected_p4.items():
        if is_selected.get() and item in entries:
            try:
                qty = int(entries[item].get().strip())
            except ValueError:
                qty = 0
                input_errors.append(item)

            if qty > 0:
                breakdown_lines.append(f"{item} ({qty} units) requires:")
                p4_totals[item] = {}  # Initialize P1 totals for this P4 item
                recurse(item, qty, parent_item=item)
                for p1_name, p1_qty in p4_totals[item].items():
                    breakdown_lines.append(f"   - {p1_name}: {int(p1_qty)}")
            else:
                breakdown_lines.append(f"{item} (0 units) requires no P1 materials.")

    # Calculate for P3 items
    for item, is_selected in selected_p3.items():
        if is_selected.get() and item in entries:
            try:
                qty = int(entries[item].get().strip())
            except ValueError:
                qty = 0
                input_errors.append(item)

            if qty > 0:
                breakdown_lines.append(f"{item} ({qty} units) requires:")
                p3_totals[item] = {}  # Initialize P1 totals for this P3 item
                recurse(item, qty, parent_item=item)
                for p1_name, p1_qty in p3_totals[item].items():
                    breakdown_lines.append(f"   - {p1_name}: {int(p1_qty)}")
            else:
                breakdown_lines.append(f"{item} (0 units) requires no P1 materials.")

    # Calculate for P2 items
    for item, is_selected in selected_p2.items():
        if is_selected.get() and item in entries:
            try:
                qty = int(entries[item].get().strip())
            except ValueError:
                qty = 0
                input_errors.append(item)

            if qty > 0:
                breakdown_lines.append(f"{item} ({qty} units) requires:")
                p2_totals[item] = {}  # Initialize P1 totals for this P2 item
                recurse(item, qty, parent_item=item)
                for p1_name, p1_qty in p2_totals[item].items():
                    breakdown_lines.append(f"   - {p1_name}: {int(p1_qty)}")
            else:
                breakdown_lines.append(f"{item} (0 units) requires no P1 materials.")

    # Prepare totals for P1 materials
    if total_p1:
        for name, amt in total_p1.items():
            total_lines.append(f" - {name}: {int(amt)}")
    else:
        total_lines.append(" - None (no items selected).")

    # Handle input errors
    if input_errors:
        breakdown_lines.append("\nInvalid inputs for: " + ", ".join(input_errors))

    # Combine breakdown and totals into two columns
    max_lines = max(len(breakdown_lines), len(total_lines))
    breakdown_lines += [""] * (max_lines - len(breakdown_lines))  # Pad shorter column
    total_lines += [""] * (max_lines - len(total_lines))  # Pad shorter column

    output_area.insert(tk.END, f"{tier_label:<50}{'Total P1 materials needed:':<30}\n")
    output_area.insert(tk.END, "-" * 80 + "\n")
    for breakdown, total in zip(breakdown_lines, total_lines):
        output_area.insert(tk.END, f"{breakdown:<50}{total:<30}\n")

def clear_inputs():
    """Reset input fields, uncheck all selected items, clear the output area, and hide all dropdown menus."""
    # Remove all quantity boxes
    for entry in entries.values():
        entry.destroy()  # Remove the quantity box widget
    entries.clear()  # Clear the entries dictionary

    # Uncheck all checkboxes for P2, P3, and P4
    for item in selected_p4.values():
        item.set(False)
    for item in selected_p3.values():
        item.set(False)
    for item in selected_p2.values():
        item.set(False)

    # Clear the output area
    output_area.delete('1.0', tk.END)
    output_area.insert(tk.END, "Enter quantities and click Calculate to see required P1 materials.\n")

    # Hide all dropdown menus
    hide_all_dropdowns()

    # Clear the input frame (reset to initial state)
    for widget in input_frame.winfo_children():
        widget.destroy()

    # Reset window geometry
    reset_window_geometry()

def toggle_quantity_box(item, row, selected_dict, entries_dict, images_dict):
    """Show or hide the quantity box next to the selected item."""
    if selected_dict[item].get():
        # Create and show the quantity box next to the selected item
        qty_entry = tk.Entry(row, width=6)
        qty_entry.pack(side='left', padx=5)
        qty_entry.insert(0, "0")

        # Highlight the "0" when the entry gains focus
        qty_entry.bind("<FocusIn>", lambda event: qty_entry.select_range(0, tk.END))

        entries_dict[item] = qty_entry
    else:
        # Remove the quantity box if it exists
        if item in entries_dict:
            entries_dict[item].destroy()
            del entries_dict[item]

def enable_context_menu(widget):
    """Enable right-click context menu with copy and paste functionality."""
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="Copy", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="Paste", command=lambda: widget.event_generate("<<Paste>>"))

    def show_context_menu(event):
        menu.tk_popup(event.x_root, event.y_root)

    widget.bind("<Button-3>", show_context_menu)  # Bind right-click to show the menu

# Enable context menu for the output_area
enable_context_menu(output_area)

# ----------------------- UI BUILD -----------------------

button_container = tk.Frame(dropdown_frame)  # Container to center all buttons
button_container.pack(anchor='center', pady=10)

# Add "Select P2 Items" button (displayed first)
tk.Button(button_container, text="Select P2 Items", command=toggle_p2_dropdown).pack(side='left', padx=5)

# Add "Select P3 Items" button (displayed second)
tk.Button(button_container, text="Select P3 Items", command=toggle_p3_dropdown).pack(side='left', padx=5)

# Add "Select P4 Items" button (displayed third)
tk.Button(button_container, text="Select P4 Items", command=toggle_dropdown).pack(side='left', padx=5)

# Create dropdown menu with checkboxes, images, and quantity boxes for P4
for item in P4_ITEMS:
    row = tk.Frame(p4_inner_frame)
    row.pack(fill='x', pady=2)

    # Display image if available
    img = p4_images[item]
    if img:
        tk.Label(row, image=img).pack(side='left', padx=5)
    else:
        tk.Label(row, text="[No Image]", width=10).pack(side='left', padx=5)

    # Checkbox for selecting the P4 item
    tk.Checkbutton(row, text=item, variable=selected_p4[item], 
                   command=lambda i=item, r=row: toggle_quantity_box(i, r, selected_p4, entries, p4_images)).pack(side='left', anchor='w')

update_scroll_region(p4_canvas, p4_inner_frame)

# Populate P2 dropdown menu with quantity boxes and associate images
for item in P2_ITEMS:
    row = tk.Frame(p2_inner_frame)
    row.pack(fill='x', pady=2)

    # Display image if available
    img = p2_images[item]
    if img:
        tk.Label(row, image=img).pack(side='left', padx=5)
    else:
        tk.Label(row, text="[No Image]", width=10).pack(side='left', padx=5)

    # Checkbox for selecting the P2 item
    tk.Checkbutton(row, text=item, variable=selected_p2[item], 
                   command=lambda i=item, r=row: toggle_quantity_box(i, r, selected_p2, entries, p2_images)).pack(side='left', anchor='w')

update_scroll_region(p2_canvas, p2_inner_frame)

# Populate P3 dropdown menu with quantity boxes
for item in P3_ITEMS:
    row = tk.Frame(p3_inner_frame)
    row.pack(fill='x', pady=2)

    # Display image if available
    img = p3_images[item]
    if img:
        tk.Label(row, image=img).pack(side='left', padx=5)
    else:
        tk.Label(row, text="[No Image]", width=10).pack(side='left', padx=5)

    # Checkbox for selecting the P3 item
    tk.Checkbutton(row, text=item, variable=selected_p3[item], 
                   command=lambda i=item, r=row: toggle_quantity_box(i, r, selected_p3, entries, p3_images)).pack(side='left', anchor='w')

update_scroll_region(p3_canvas, p3_inner_frame)

# Populate P4 dropdown menu with quantity boxes
for item in P4_ITEMS:
    row = tk.Frame(p4_inner_frame)
    row.pack(fill='x', pady=2)

    # Display image if available
    img = p4_images[item]
    if img:
        tk.Label(row, image=img).pack(side='left', padx=5)
    else:
        tk.Label(row, text="[No Image]", width=10).pack(side='left', padx=5)

    # Checkbox for selecting the P4 item
    tk.Checkbutton(row, text=item, variable=selected_p4[item], 
                   command=lambda i=item, r=row: toggle_quantity_box(i, r, selected_p4, entries, p4_images)).pack(side='left', anchor='w')

update_scroll_region(p4_canvas, p4_inner_frame)

tk.Button(button_frame, text="Calculate", command=calculate_requirements).pack(side='left', padx=5)
tk.Button(button_frame, text="Clear", command=clear_inputs).pack(side='left', padx=5)

# Bind the Enter key to the calculate_requirements function
root.bind('<Return>', lambda event: calculate_requirements())

# ----------------------- MAIN LOOP -----------------------
root.mainloop()
