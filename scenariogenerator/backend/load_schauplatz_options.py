import json

from scenariogenerator.constants import DATA_DIR

def load_schauplatz_options(gefahr_key):
    print(gefahr_key)
    file_path = DATA_DIR / "schauplatz/gd_schauplatz_v3.2.json"
    with open(file_path, "r", encoding="utf-8") as f:
        schauplatz_json = json.load(f)
    print(schauplatz_json.keys())
    details = schauplatz_json["gefaehrdungen"][gefahr_key]["hauptschauplätze"]
    print(details)
    return [d['label'] for d in details]

def load_ausdehnung(gefahr_key, location):
    file_path = DATA_DIR / "schauplatz/gd_schauplatz_v3.2.json"
    with open(file_path, "r", encoding="utf-8") as f:
        schauplatz_json = json.load(f)

    details = schauplatz_json["gefaehrdungen"][gefahr_key]["hauptschauplätze"]
    for d in details:
        if d['label'] == location:
            return d['raeumliche_ausdehnung']
    return None  # or raise an error if location is not found