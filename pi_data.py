import json
import os
from collections import defaultdict

# Load PI data
with open("pi_p4_data.json") as f:
    PI_DATA = json.load(f)

P1_ITEMS = [k for k, v in PI_DATA.items() if all(i not in PI_DATA or not PI_DATA[i].get("inputs") for i in v["inputs"])]
P2_ITEMS = [k for k, v in PI_DATA.items() if any(i in P1_ITEMS for i in v["inputs"])]
P3_ITEMS = [k for k, v in PI_DATA.items() if any(i in P2_ITEMS for i in v["inputs"])]
P4_ITEMS = [k for k, v in PI_DATA.items() if all(i in P3_ITEMS for i in v["inputs"])]

TIERS = {
    "P1": P1_ITEMS,
    "P2": P2_ITEMS,
    "P3": P3_ITEMS,
    "P4": P4_ITEMS
}

def calculate_p1_requirements(item, qty):
    data = PI_DATA[item]
    out_qty = data["output_qty"]
    requirements = []
    for p0, amt in data["inputs"].items():
        total = (amt / out_qty) * qty
        requirements.append((p0, int(total)))
    return requirements

def recurse_requirements(name, needed_qty, p1_totals, p0_totals):
    if name not in PI_DATA:
        return
    data = PI_DATA[name]
    out_qty = data["output_qty"]
    multiplier = needed_qty / out_qty
    for sub, sub_qty in data["inputs"].items():
        total = sub_qty * multiplier
        if sub not in PI_DATA:
            continue
        sub_data = PI_DATA[sub]
        sub_inputs = sub_data.get("inputs", {})
        if len(sub_inputs) == 1 and all(i not in PI_DATA or not PI_DATA[i].get("inputs") for i in sub_inputs):
            p1_totals[sub] += total
            for p0_item, p0_qty in sub_inputs.items():
                p0_totals[p0_item] += (p0_qty / sub_data["output_qty"]) * total
