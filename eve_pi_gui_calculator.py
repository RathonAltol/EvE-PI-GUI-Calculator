import json
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import ctypes  # Add this import for getting screen size

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

P1_ITEMS = [
    "Bacteria",
    "Biofuels",
    "Biomass",
    "Chirals Structures",
    "Electrolytes",
    "Industrial Fibers",
    "Oxygen",
    "Oxidizing Compound",
    "Plasmoids",
    "Precious Metals",
    "Proteins",
    "Reactive Metals",
    "Silicon",
    "Toxic Metals",
    "Water"
]

IMAGE_DIR = "Images"
JSON_FILE = "pi_p4_data.json"

DEFAULT_WIN_WIDTH = int(600 * 1.01)  # Increased by 1% from 600
DEFAULT_WIN_HEIGHT = 600
MACOS_MARGIN = 80  # Margin for menu bar/dock

# --- Fixed dropdown area size for all tiers ---
DROPDOWN_WIDTH = int(435 * 1.1)   # Increased by 10%
DROPDOWN_HEIGHT = int(420 * 1.1)  # Increased height for dropdowns

# ----------------------- LOAD DATA -----------------------

try:
    with open(JSON_FILE, 'r') as f:
        p4_data = json.load(f)
except FileNotFoundError:
    raise SystemExit(f"Error: '{JSON_FILE}' file not found.")

# ----------------------- INITIALIZE TK -----------------------

root = tk.Tk()
root.title("EVE PI P4 → P1 Calculator")
root.geometry(f"{DEFAULT_WIN_WIDTH}x{DEFAULT_WIN_HEIGHT}")  # Set default window size (width increased by 1%)

selected_p4 = {item: tk.BooleanVar(value=False) for item in P4_ITEMS}
selected_p2 = {item: tk.BooleanVar(value=False) for item in P2_ITEMS}
selected_p3 = {item: tk.BooleanVar(value=False) for item in P3_ITEMS}
selected_p1 = {item: tk.BooleanVar(value=False) for item in P1_ITEMS}
entries = {}
p4_images = {}
p2_images = {}
p3_images = {}
p1_images = {}

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

for item in P1_ITEMS:
    try:
        img = Image.open(f"{IMAGE_DIR}/{item}.png")
        img.thumbnail((50, 50), Image.Resampling.LANCZOS)
        p1_images[item] = ImageTk.PhotoImage(img)
    except FileNotFoundError:
        p1_images[item] = None

# ----------------------- UI COMPONENTS -----------------------

dropdown_frame = tk.Frame(root)
dropdown_frame.pack(padx=10, pady=10, anchor='n')

button_container = tk.Frame(dropdown_frame)  # Container to center all buttons
button_container.pack(anchor='center', pady=10)

# --- Main content frame to hold dropdown only (output area will be below button_frame) ---
main_content_frame = tk.Frame(root)
main_content_frame.pack(padx=10, pady=10, anchor='center', fill='x', expand=False)

# Move dropdown menus into main_content_frame
dropdown_menu = tk.Frame(main_content_frame, relief=tk.RAISED, borderwidth=1, width=600)
dropdown_menu.pack_propagate(True)
p2_dropdown_menu = tk.Frame(main_content_frame, relief=tk.RAISED, borderwidth=1, width=600)
p2_dropdown_menu.pack_propagate(True)
p3_dropdown_menu = tk.Frame(main_content_frame, relief=tk.RAISED, borderwidth=1, width=600)
p3_dropdown_menu.pack_propagate(True)
p1_dropdown_menu = tk.Frame(main_content_frame, relief=tk.RAISED, borderwidth=1, width=600)
p1_dropdown_menu.pack_propagate(True)

# Output area is now below the button_frame, not inside main_content_frame
button_frame = tk.Frame(root)
button_frame.pack(padx=10, pady=5, anchor='center')  # Always pack ONCE, directly above output_frame

output_frame = tk.Frame(root)
output_frame.pack(padx=0, pady=0, anchor='center', fill='both', expand=True)

input_frame = tk.Frame(root)  # input_frame stays outside, as before

output_area = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=60, height=int(10 * 0.9))  # Decreased default height by 10%
output_area.pack(padx=10, pady=10, fill='both', expand=True)
output_area.insert(tk.END, "Enter quantities and click Calculate to see required P1 materials.\n")

# --- Auto-resize output_area based on content and screen size ---

def get_screen_height():
    # Cross-platform way to get screen height
    try:
        return root.winfo_screenheight()
    except Exception:
        try:
            user32 = ctypes.windll.user32
            return user32.GetSystemMetrics(1)
        except Exception:
            return 1080  # fallback

def adjust_output_area_height(event=None):
    # Get number of lines in output_area
    num_lines = int(output_area.index('end-1c').split('.')[0])
    # Estimate line height in pixels
    font = output_area.cget("font")
    try:
        import tkinter.font as tkfont
        font_obj = tkfont.Font(font=font)
        line_height = font_obj.metrics("linespace")
    except Exception:
        line_height = 18  # fallback
    # Calculate desired height in pixels
    desired_height_px = num_lines * line_height + 20  # +20 for padding/scrollbar
    # Get available height: screen height minus window's y position and some margin
    screen_height = get_screen_height()
    root.update_idletasks()
    root_y = root.winfo_y()
    available_height = screen_height - root_y - 80  # 80px margin for taskbar/title
    # Clamp desired height
    max_height_px = max(90, min(available_height, int(400 * 0.9)))  # lower max height for output area, reduced by 10%
    final_height_px = min(desired_height_px, max_height_px)
    # Convert pixels to number of text lines (approx)
    height_lines = max(5, int(final_height_px / line_height))
    output_area.config(height=height_lines)

# Bind to content changes and window resize
def on_output_area_change(event=None):
    output_area.after_idle(adjust_output_area_height)

output_area.bind('<<Modified>>', on_output_area_change)
root.bind('<Configure>', lambda e: adjust_output_area_height())

# Reset the modified flag after handling
def reset_modified_flag(event=None):
    output_area.tk.call(output_area._w, 'edit', 'modified', 0)
output_area.bind('<<Modified>>', reset_modified_flag, add='+')

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

    # Add input fields for selected P1 items
    for item, is_selected in selected_p1.items():
        if is_selected.get():
            row = tk.Frame(input_frame)
            row.pack(fill='x', pady=2)

            img = p1_images[item]
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
    """Hide all dropdown menus (but never hide output area)."""
    dropdown_menu.pack_forget()
    p2_dropdown_menu.pack_forget()
    p3_dropdown_menu.pack_forget()
    p1_dropdown_menu.pack_forget()

def clear_output_area():
    """Clear the output area."""
    output_area.delete('1.0', tk.END)
    output_area.insert(tk.END, "Enter quantities above and click Calculate to see required P1 materials.\n")
    output_area.edit_modified(True)  # Trigger <<Modified>> event

def reset_tier(selected_dict, entries_dict):
    """Reset all items for the selected tier of PI."""
    # Uncheck all checkboxes
    for var in selected_dict.values():
        var.set(False)
    # Clear all quantity boxes
    for entry in entries_dict.values():
        entry.destroy()
    entries_dict.clear()

def get_available_screen_height():
    # Get screen height minus a margin for menu bar/dock
    try:
        screen_height = root.winfo_screenheight()
    except Exception:
        try:
            import ctypes
            user32 = ctypes.windll.user32
            screen_height = user32.GetSystemMetrics(1)
        except Exception:
            screen_height = 1080
    return max(400, screen_height - MACOS_MARGIN)

def resize_for_dropdown(dropdown_menu):
    """Resize window and adjust dropdown/output area heights so both are visible and fill available space."""
    # Only one dropdown is visible at a time
    available_height = get_available_screen_height()
    root.update_idletasks()
    above_height = (
        dropdown_frame.winfo_height() +
        button_frame.winfo_height() +
        40  # extra margin for paddings/titlebar
    )
    usable_height = max(300, available_height - above_height)
    # Fixed dropdown height for all tiers
    dropdown_height = DROPDOWN_HEIGHT
    min_output = int(90 * 0.9)  # lower min output area height, reduced by 10%
    output_height = max(min_output, usable_height - dropdown_height)
    # Set heights
    # Set all dropdown canvases to the fixed height
    for canvas in [p4_canvas, p2_canvas, p3_canvas, p1_canvas]:
        canvas.config(height=DROPDOWN_HEIGHT, width=DROPDOWN_WIDTH)
    output_area.config(height=int((output_height // 18) * 0.9))  # 18px per line approx, reduced by 10%
    # Resize window
    total_height = above_height + dropdown_height + output_height + 40
    root.geometry(f"{DEFAULT_WIN_WIDTH}x{int(total_height)}")
    # Ensure packing order
    dropdown_menu.pack(side='top', fill='x', padx=0, pady=(0, 5))
    output_frame.pack(side='top', fill='both', expand=True)
    output_area.pack_configure(fill='both', expand=True)
    root.update_idletasks()

def reset_window_geometry():
    """Reset the window to its default size and shape."""
    root.geometry(f"{DEFAULT_WIN_WIDTH}x{DEFAULT_WIN_HEIGHT}")
    # Reset output_area height
    output_area.config(height=int(10 * 0.9))  # Decreased default height by 10%

def toggle_dropdown():
    """Show P4 dropdown menu above output area, always keeping both visible."""
    hide_all_dropdowns()
    reset_tier(selected_p4, entries)
    clear_output_area()
    button_container.pack_forget()
    button_container.pack(padx=10, pady=10, anchor='n')
    _show_dropdown(dropdown_menu, p4_inner_frame, p4_canvas, P4_ITEMS, p4_images, selected_p4, entries)
    dropdown_menu.pack(side='top', fill='x', padx=0, pady=(0, 5))
    output_frame.pack(side='top', fill='both', expand=True)
    input_frame.pack_forget()
    input_frame.pack(padx=10, pady=10, anchor='center')
    # button_frame.pack_forget()  # REMOVE this line
    # button_frame.pack(padx=10, pady=5, anchor='center')  # REMOVE this line
    root.update_idletasks()
    resize_for_dropdown(dropdown_menu)

def toggle_p3_dropdown():
    """Show P3 dropdown menu above output area, always keeping both visible."""
    hide_all_dropdowns()
    reset_tier(selected_p3, entries)
    clear_output_area()
    button_container.pack_forget()
    button_container.pack(padx=10, pady=10, anchor='n')
    _show_dropdown(p3_dropdown_menu, p3_inner_frame, p3_canvas, P3_ITEMS, p3_images, selected_p3, entries)
    p3_dropdown_menu.pack(side='top', fill='x', padx=0, pady=(0, 5))
    output_frame.pack(side='top', fill='both', expand=True)
    input_frame.pack_forget()
    input_frame.pack(padx=10, pady=10, anchor='center')
    # button_frame.pack_forget()  # REMOVE this line
    # button_frame.pack(padx=10, pady=5, anchor='center')  # REMOVE this line
    root.update_idletasks()
    resize_for_dropdown(p3_dropdown_menu)

def toggle_p2_dropdown():
    """Show P2 dropdown menu above output area, always keeping both visible."""
    hide_all_dropdowns()
    reset_tier(selected_p2, entries)
    clear_output_area()
    button_container.pack_forget()
    button_container.pack(padx=10, pady=10, anchor='n')
    _show_dropdown(p2_dropdown_menu, p2_inner_frame, p2_canvas, P2_ITEMS, p2_images, selected_p2, entries)
    p2_dropdown_menu.pack(side='top', fill='x', padx=0, pady=(0, 5))
    output_frame.pack(side='top', fill='both', expand=True)
    input_frame.pack_forget()
    input_frame.pack(padx=10, pady=10, anchor='center')
    # button_frame.pack_forget()  # REMOVE this line
    # button_frame.pack(padx=10, pady=5, anchor='center')  # REMOVE this line
    root.update_idletasks()
    resize_for_dropdown(p2_dropdown_menu)

def toggle_p1_dropdown():
    """Show P1 dropdown menu above output area, always keeping both visible."""
    hide_all_dropdowns()
    reset_tier(selected_p1, entries)
    clear_output_area()
    button_container.pack_forget()
    button_container.pack(padx=10, pady=10, anchor='n')
    _show_dropdown(p1_dropdown_menu, p1_inner_frame, p1_canvas, P1_ITEMS, p1_images, selected_p1, entries)
    p1_dropdown_menu.pack(side='top', fill='x', padx=0, pady=(0, 5))
    output_frame.pack(side='top', fill='both', expand=True)
    input_frame.pack_forget()
    input_frame.pack(padx=10, pady=10, anchor='center')
    root.update_idletasks()
    resize_for_dropdown(p1_dropdown_menu)

def calculate_requirements():
    """Calculate P1 material requirements and display results."""
    output_area.delete('1.0', tk.END)
    total_p1, breakdown_lines, total_lines, input_errors = {}, [], [], []
    p4_totals = {}  # Store total P1 materials for each individual P4 item
    p3_totals = {}  # Store total P1 materials for each individual P3 item
    p2_totals = {}  # Store total P1 materials for each individual P2 item
    p1_totals = {}  # Store total for P1 items

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
                elif parent_item in p1_totals:
                    p1_totals[parent_item][item_name] = p1_totals[parent_item].get(item_name, 0) + qty_needed
            return
        data = p4_data[item_name]
        multiplier = qty_needed / data.get('output_qty', 1)
        for input_item, input_qty in data.get('inputs', {}).items():
            recurse(input_item, input_qty * multiplier, parent_item)

    # Determine which tier is currently selected
    if p1_dropdown_menu.winfo_ismapped():
        tier_label = "P1 Items Selected"
    elif dropdown_menu.winfo_ismapped():
        tier_label = "P4 Items Selected"
    elif p3_dropdown_menu.winfo_ismapped():
        tier_label = "P3 Items Selected"
    elif p2_dropdown_menu.winfo_ismapped():
        tier_label = "P2 Items Selected"
    else:
        tier_label = "Items Selected"

    # Calculate for P1 items
    for item, is_selected in selected_p1.items():
        if is_selected.get() and item in entries:
            try:
                qty = int(entries[item].get().strip())
            except ValueError:
                qty = 0
                input_errors.append(item)
            if qty > 0:
                breakdown_lines.append(f"{item} ({qty} units) requires:")
                p1_totals[item] = {}
                # For P1, just show the quantity (no further breakdown)
                p1_totals[item][item] = qty
                total_p1[item] = total_p1.get(item, 0) + qty
                breakdown_lines.append(f"   - {item}: {qty}")
            else:
                breakdown_lines.append(f"{item} (0 units) requires no P1 materials.")

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
    output_area.edit_modified(True)  # Trigger <<Modified>> event

    # Dynamically resize window so output_area reaches bottom of screen, but keep buttons visible
    root.update_idletasks()
    screen_height = get_screen_height()
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    # Estimate the height of all widgets above output_area (dropdowns, buttons, paddings)
    above_height = (
        dropdown_frame.winfo_height() +
        (dropdown_menu.winfo_height() if dropdown_menu.winfo_ismapped() else 0) +
        (p2_dropdown_menu.winfo_height() if p2_dropdown_menu.winfo_ismapped() else 0) +
        (p3_dropdown_menu.winfo_height() if p3_dropdown_menu.winfo_ismapped() else 0) +
        input_frame.winfo_height() +
        button_frame.winfo_height() +
        80  # extra margin for paddings/titlebar
    )
    # Calculate available height for output_area+output_frame
    margin = 40
    available_height = screen_height - root_y - above_height - margin
    # Set window height to fit everything, but not less than 250
    total_height = above_height + max(int(250 * 0.9), int(available_height * 0.9))  # Decreased by 10%
    root.geometry(f"{DEFAULT_WIN_WIDTH}x{int(total_height)}")
    # Expand output_area to fill output_frame
    output_frame.pack_configure(fill='both', expand=True)
    output_area.pack_configure(fill='both', expand=True)
    output_area.update_idletasks()

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
    for item in selected_p1.values():
        item.set(False)

    # Clear the output area
    output_area.delete('1.0', tk.END)
    output_area.insert(tk.END, "Enter quantities and click Calculate to see required P1 materials.\n")
    output_area.edit_modified(True)  # Trigger <<Modified>> event

    # Hide all dropdown menus
    hide_all_dropdowns()

    # Clear the input frame (reset to initial state)
    for widget in input_frame.winfo_children():
        widget.destroy()

    # Reset window geometry
    reset_window_geometry()
    # Do NOT repack button_frame here

def create_dropdown_row(parent_frame, item, img, selected_var, entries_dict):
    row = tk.Frame(parent_frame)
    row.pack(fill='x', expand=True, pady=2)
    row.grid_columnconfigure(2, weight=0)  # item name
    row.grid_columnconfigure(3, weight=1)  # spacer
    row.grid_columnconfigure(4, weight=0)  # entry

    if img:
        tk.Label(row, image=img).grid(row=0, column=0, padx=(0, 5), sticky='w')
    else:
        tk.Label(row, text="[No Image]", width=10).grid(row=0, column=0, padx=(0, 5), sticky='w')

    cb = tk.Checkbutton(row, variable=selected_var)
    cb.grid(row=0, column=1, padx=(0, 5), sticky='w')
    tk.Label(row, text=item, anchor='w').grid(row=0, column=2, sticky='w')
    # Flexible spacer
    spacer = tk.Frame(row)
    spacer.grid(row=0, column=3, sticky='ew')
    # Make the row expand horizontally
    row.pack_propagate(False)
    row.grid_columnconfigure(3, weight=1)

    qty_entry_ref = [None]  # mutable holder for the entry widget

    def on_toggle(*_):
        # Remove entry if exists
        if qty_entry_ref[0] is not None:
            qty_entry_ref[0].destroy()
            qty_entry_ref[0] = None
            if item in entries_dict:
                del entries_dict[item]
        # Add entry if checked and row still exists
        if selected_var.get() and row.winfo_exists():
            qty_entry = tk.Entry(row, width=6, justify='right')
            qty_entry.insert(0, "0")
            qty_entry.grid(row=0, column=4, padx=(5, 0), sticky='e')
            qty_entry_ref[0] = qty_entry
            entries_dict[item] = qty_entry
            # Auto-select the "0" and focus the entry
            qty_entry.focus_set()
            qty_entry.selection_range(0, tk.END)

    selected_var.trace_add('write', on_toggle)
    # Initial state: do not show entry unless checked
    if selected_var.get():
        on_toggle()

def populate_dropdown(inner_frame, items, images, selected_dict, entries_dict):
    # Clear current contents
    for widget in inner_frame.winfo_children():
        widget.destroy()
    # Add all items
    for item in items:
        create_dropdown_row(inner_frame, item, images[item], selected_dict[item], entries_dict)
    # Update scroll region
    update_scroll_region(inner_frame.master, inner_frame)

# ----------------------- SCROLLABLE DROPDOWN FRAMES -----------------------

def _bind_mousewheel(widget, target):
    def _on_mousewheel(event):
        if event.num == 5 or event.delta == -120:
            target.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            target.yview_scroll(-1, "units")
        elif event.delta < 0:
            target.yview_scroll(1, "units")
        elif event.delta > 0:
            target.yview_scroll(-1, "units")
    widget.bind("<MouseWheel>", _on_mousewheel)
    widget.bind("<Button-4>", _on_mousewheel)
    widget.bind("<Button-5>", _on_mousewheel)

def update_scroll_region(canvas, inner_frame):
    canvas.configure(scrollregion=canvas.bbox("all"))

def _expand_dropdown_to_fit(inner_frame, canvas, max_height=500, row_height=36, min_height=120):
    """
    Dynamically resize the dropdown canvas height to fit the number of visible rows, up to max_height.
    """
    # OVERRIDE: Always use fixed height for all dropdowns
    canvas.config(height=DROPDOWN_HEIGHT)
    canvas.update_idletasks()
    update_scroll_region(canvas, inner_frame)

def _show_dropdown(dropdown_menu, inner_frame, canvas, items, images, selected_dict, entries_dict):
    # Populate and expand dropdown
    populate_dropdown(inner_frame, items, images, selected_dict, entries_dict)
    # Set all dropdown canvases to the fixed height
    for c in [p4_canvas, p2_canvas, p3_canvas, p1_canvas]:
        c.config(height=DROPDOWN_HEIGHT)
    canvas.config(height=DROPDOWN_HEIGHT)
    canvas.update_idletasks()
    update_scroll_region(canvas, inner_frame)
    dropdown_menu.pack(padx=10, pady=10, anchor='center')

# P4 dropdown scrollable frame
p4_canvas = tk.Canvas(dropdown_menu, width=DROPDOWN_WIDTH, height=DROPDOWN_HEIGHT)
p4_scrollbar = tk.Scrollbar(dropdown_menu, orient="vertical", command=p4_canvas.yview)
p4_canvas.configure(yscrollcommand=p4_scrollbar.set)
p4_canvas.pack(side="left", fill="both", expand=True)
p4_scrollbar.pack(side="right", fill="y")
p4_inner_frame = tk.Frame(p4_canvas)
p4_canvas.create_window((0, 0), window=p4_inner_frame, anchor="nw")
p4_inner_frame.bind("<Configure>", lambda e: update_scroll_region(p4_canvas, p4_inner_frame))
_bind_mousewheel(p4_canvas, p4_canvas)

# P2 dropdown scrollable frame
p2_canvas = tk.Canvas(p2_dropdown_menu, width=DROPDOWN_WIDTH, height=DROPDOWN_HEIGHT)
p2_scrollbar = tk.Scrollbar(p2_dropdown_menu, orient="vertical", command=p2_canvas.yview)
p2_canvas.configure(yscrollcommand=p2_scrollbar.set)
p2_canvas.pack(side="left", fill="both", expand=True)
p2_scrollbar.pack(side="right", fill="y")
p2_inner_frame = tk.Frame(p2_canvas)
p2_canvas.create_window((0, 0), window=p2_inner_frame, anchor="nw")
p2_inner_frame.bind("<Configure>", lambda e: update_scroll_region(p2_canvas, p2_inner_frame))
_bind_mousewheel(p2_canvas, p2_canvas)

# P3 dropdown scrollable frame
p3_canvas = tk.Canvas(p3_dropdown_menu, width=DROPDOWN_WIDTH, height=DROPDOWN_HEIGHT)
p3_scrollbar = tk.Scrollbar(p3_dropdown_menu, orient="vertical", command=p3_canvas.yview)
p3_canvas.configure(yscrollcommand=p3_scrollbar.set)
p3_canvas.pack(side="left", fill="both", expand=True)
p3_scrollbar.pack(side="right", fill="y")
p3_inner_frame = tk.Frame(p3_canvas)
p3_canvas.create_window((0, 0), window=p3_inner_frame, anchor="nw")
p3_inner_frame.bind("<Configure>", lambda e: update_scroll_region(p3_canvas, p3_inner_frame))
_bind_mousewheel(p3_canvas, p3_canvas)

# P1 dropdown scrollable frame
p1_canvas = tk.Canvas(p1_dropdown_menu, width=DROPDOWN_WIDTH, height=DROPDOWN_HEIGHT)
p1_scrollbar = tk.Scrollbar(p1_dropdown_menu, orient="vertical", command=p1_canvas.yview)
p1_canvas.configure(yscrollcommand=p1_scrollbar.set)
p1_canvas.pack(side="left", fill="both", expand=True)
p1_scrollbar.pack(side="right", fill="y")
p1_inner_frame = tk.Frame(p1_canvas)
p1_canvas.create_window((0, 0), window=p1_inner_frame, anchor="nw")
p1_inner_frame.bind("<Configure>", lambda e: update_scroll_region(p1_canvas, p1_inner_frame))
_bind_mousewheel(p1_canvas, p1_canvas)

# Make output_area scrollable with mouse wheel as well
def _on_output_mousewheel(event):
    if event.num == 5 or event.delta == -120:
        output_area.yview_scroll(1, "units")
    elif event.num == 4 or event.delta == 120:
        output_area.yview_scroll(-1, "units")
    elif event.delta < 0:
        output_area.yview_scroll(1, "units")
    elif event.delta > 0:
        output_area.yview_scroll(-1, "units")

output_area.bind("<MouseWheel>", _on_output_mousewheel)
output_area.bind("<Button-4>", _on_output_mousewheel)
output_area.bind("<Button-5>", _on_output_mousewheel)

# P4 dropdown
populate_dropdown(p4_inner_frame, P4_ITEMS, p4_images, selected_p4, entries)
update_scroll_region(p4_canvas, p4_inner_frame)

# P2 dropdown
populate_dropdown(p2_inner_frame, P2_ITEMS, p2_images, selected_p2, entries)
update_scroll_region(p2_canvas, p2_inner_frame)

# P3 dropdown
populate_dropdown(p3_inner_frame, P3_ITEMS, p3_images, selected_p3, entries)
update_scroll_region(p3_canvas, p3_inner_frame)

# P1 dropdown
populate_dropdown(p1_inner_frame, P1_ITEMS, p1_images, selected_p1, entries)
update_scroll_region(p1_canvas, p1_inner_frame)

tk.Button(button_frame, text="Calculate", command=calculate_requirements).pack(side='left', padx=5)
tk.Button(button_frame, text="Clear", command=clear_inputs).pack(side='left', padx=5)

# Bind the Enter key to the calculate_requirements function
root.bind('<Return>', lambda event: calculate_requirements())

# Create the buttons after the toggle functions are defined
tk.Button(
    button_container,
    text="Select P1 Items",
    command=toggle_p1_dropdown,
    relief='raised'
).pack(side='left', padx=5)
tk.Button(button_container, text="Select P2 Items", command=toggle_p2_dropdown).pack(side='left', padx=5)
tk.Button(button_container, text="Select P3 Items", command=toggle_p3_dropdown).pack(side='left', padx=5)
tk.Button(button_container, text="Select P4 Items", command=toggle_dropdown).pack(side='left', padx=5)

# ----------------------- MAIN LOOP -----------------------
root.mainloop()
