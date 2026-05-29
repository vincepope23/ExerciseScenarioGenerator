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
    "Absturz Luftfahrtobjekt",
    "Andrang Schutzsuchender",
    "Anschlag mit konventionellen Mitteln",
    "Anschlag toxische Industriechemikalie",
    "Ausbreitung invasiver Arten",
    "Ausfall Mobilfunk",
    "Bergsturz",
    "Bewaffneter Konflikt",
    "Biologischer Anschlag",
    "Bioterrorismus",
    "Chemieunfall",
    "Chemischer Anschlag",
    "Erdgasausfall",
    "Erdölmangellage",
    "Erdbeben",
    "Einschränkung Schiffsverkehr",
    "Gasmangellage",
    "Gefahrgutunfall",
    "Gefahrgutunfall Schiene",
    "Gesellschaftliche Unruhen",
    "Hagelschlag",
    "Hitzewelle",
    "Hochwasser",
    "KKW-Unfall",
    "Kältewelle",
    "Lawinenwinter",
    "Meteoriteneinschlag",
    "Nuklearterroranschlag",
    "Pandemie",
    "Radiologischer Anschlag",
    "Sonnensturm",
    "Starker Schneefall",
    "Starkregen",
    "Stauanlagen-Unfall",
    "Stromausfall",
    "Strommangellage",
    "Sturm",
    "Tierseuche",
    "Toxinanschlag",
    "Trockenheit",
    "Unfall B-Betrieb",
    "Vulkanausbruch",
    "Waldbrand",
    "Cyberangriff",
]
