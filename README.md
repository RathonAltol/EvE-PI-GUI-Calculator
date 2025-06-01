# EVE PI GUI Calculator

A graphical tool for calculating Planetary Interaction (PI) material requirements in EVE Online. This tool allows you to select PI product tiers and quantities, and see the required input materials, using a modern Python/Tkinter GUI.

## Features
- Select PI product tier (P1, P2, P3, P4)
- Choose products and input desired quantities
- See all required lower-tier materials
- Scrollable, image-enhanced interface
- Auto-resizing window

## Requirements
- Python 3.8+
- Pillow (for image support)

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/EvE-PI-GUI-Calculator.git
   cd EvE-PI-GUI-Calculator
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Make sure `pi_p4_data.json` and the `images/` folder are in the project directory.
2. Run the tool:
   ```bash
   python main.py
   ```
3. The GUI will open. Use the interface to select tiers, products, and quantities.

## Project Structure
- `main.py` - Entry point for the application
- `gui.py` - All GUI classes and logic
- `pi_data.py` - Data loading and calculation logic
- `utils.py` - Utility functions (if needed)
- `pi_p4_data.json` - PI data file
- `images/` - Folder with product images
- `requirements.txt` - Python dependencies

## Notes
- Images for each PI product should be named exactly as the product (e.g., `Biotech Research Reports.png`) and placed in the `images/` folder.
- The tool auto-resizes the window to fit the current content.

## License
MIT
