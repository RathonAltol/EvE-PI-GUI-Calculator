import shutil
import os
from cx_Freeze import setup, Executable

# Remove the build directory if it exists
def remove_readonly(func, path, exc_info):
    """Clear the readonly bit and retry."""
    os.chmod(path, 0o700)
    func(path)

build_dir = "build"
if os.path.exists(build_dir):
    shutil.rmtree(build_dir, onerror=remove_readonly)

# Include additional files (images and JSON data)
include_files = [
    ("Images", "Images"),  # Include the Images folder
    "pi_p4_data.json"      # Include the JSON file
]

# Dependencies
build_exe_options = {
    "packages": ["tkinter", "PIL", "json"],
    "include_files": include_files
}

# Executable configuration
base = None
if os.name == "nt":
    base = "Win32GUI"  # Use "Win32GUI" for GUI applications on Windows

setup(
    name="EVE PI GUI Calculator",
    version="1.0",
    description="A GUI calculator for EVE Online Planetary Interaction.",
    options={"build_exe": build_exe_options},
    executables=[Executable("eve_pi_gui_calculator.py", base=base)]
)
