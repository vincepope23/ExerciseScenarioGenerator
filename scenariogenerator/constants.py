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
    'Einflussfaktoren'
]

GEFAHR_OPTIONS = [
    "Chemischer Anschlag",
    "Erdölmangellage",
    "Hagelschlag",
    "Starker Schneefall",
    "Starkregen"
]