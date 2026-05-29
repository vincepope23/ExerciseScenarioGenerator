import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

ROOT_DIR = Path(__file__).parent.parent
PROMPTS_DIR = ROOT_DIR / "prompts"
DATA_DIR = ROOT_DIR / Path("data")
INDEX_FILE = DATA_DIR / "Gefährdungsszenarien_index.md"

RELEVANT_SECTIONS = [
    'Phasen',
    'Schwerestufen',
    'Einflussfaktoren',
    'Auswirkungen'
]

GEFAHR_OPTIONS = [

    "Andrang Schutzsuchender",
    "Bergsturz",
    "Bewaffneter Konflikt",
    "Biologischer Anschlag",
    "Biologischer Unfall",
    "Bioterrorismus",
    "Chemieunfall",
    "Chemischer Anschlag",
    "Cyberangriff",
    #"Dammbruch",
    "Erdbeben",
    "Erdgasausfall",
    "Erdölmangellage",
    "Flugzeugabsturz",
    "Gasmangellage",
    "Gefahrgutunfall",
    "Gesellschaftliche Unruhen",
    "Hagelschlag",
    "Hitzewelle",
    "Hochwasser",
    "Invasive Arten",
    "KKW-Unfall",
    "Kältewelle",
    "Lawinenwinter",
    "Meteoriteneinschlag",
    "Mobilfunkausfall",
    "Nuklearterroranschlag",
    "Pandemie",
    "Radioaktiver Anschlag",
    "Radiologischer Anschlag",
    "Schiffsverkehrseinschränkungen",
    "Sonnensturm",
    "Starker Schneefall",
    "Starkregen",
    "Stauanlagen-Unfall",
    "Stromausfall",
    "Strommangellage",
    "Sturm",
    "Terroranschlag",
    "Tierseuche",
    "Toxinanschlag",
    "Trockenheit",
    "Vulkanausbruch",
    "Waldbrand"
    "Tierseuche",
    "Toxinanschlag",
    "Trockenheit",
    "Unfall B-Betrieb",
    "Vulkanausbruch",
    "Waldbrand",
    "Cyberangriff",
]