import json
import os
from collections import defaultdict

# Load all tier files from pi_data folder
PI_DATA = {}
TIERS = {}
TIER_FILES = [
    ("P1", "pi_data/pi_p1.json"),
    ("P2", "pi_data/pi_p2.json"),
    ("P3", "pi_data/pi_p3.json"),
    ("P4", "pi_data/pi_p4.json"),
]
TIER_DICTS = {}
for tier, filename in TIER_FILES:
    if not os.path.exists(filename):
        print(f"ERROR: Required PI data file missing: {filename}")
        print("Please ensure all pi_data/pi_pX.json files exist.")
        exit(1)
    try:
        with open(filename) as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: Could not load or parse {filename}: {e}")
        exit(1)
    TIER_DICTS[tier] = data
    PI_DATA.update(data)
    TIERS[tier] = list(data.keys())

def resolve_input_ref(ref):
    if ref.startswith("@"):
        tier, name = ref[1:].split(":", 1)
        return TIER_DICTS[tier][name]
    return None

def get_inputs(item_data):
    inputs = {}
    for k, v in item_data["inputs"].items():
        if k.startswith("@"):
            # Reference to another item
            ref_data = resolve_input_ref(k)
            inputs[k] = (ref_data, v)
        else:
            inputs[k] = v
    return inputs

def calculate_p1_requirements(item, qty):
    data = PI_DATA[item]
    out_qty = data["output_qty"]
    requirements = []
    for p0, amt in data["inputs"].items():
        if p0.startswith("@"):
            p0_name = p0.split(":", 1)[1]
        else:
            p0_name = p0
        total = (amt / out_qty) * qty
        requirements.append((p0_name, int(total)))
    return requirements

def recurse_requirements(name, needed_qty, p1_totals, p0_totals):
    if name not in PI_DATA:
        return
    data = PI_DATA[name]
    out_qty = data["output_qty"]
    multiplier = needed_qty / out_qty
    for sub, sub_qty in data["inputs"].items():
        if sub.startswith("@"):
            sub_name = sub.split(":", 1)[1]
        else:
            sub_name = sub
        total = sub_qty * multiplier
        if sub_name not in PI_DATA:
            continue
        sub_data = PI_DATA[sub_name]
        sub_inputs = sub_data.get("inputs", {})
        if len(sub_inputs) == 1 and all(i not in PI_DATA or not PI_DATA[i].get("inputs") for i in sub_inputs):
            p1_totals[sub_name] += total
            for p0_item, p0_qty in sub_inputs.items():
                p0_totals[p0_item] += (p0_qty / sub_data["output_qty"]) * total
