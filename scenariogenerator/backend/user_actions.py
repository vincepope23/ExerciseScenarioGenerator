

from scenariogenerator.backend.constants import INDEX_FILE, DATA_DIR, RELEVANT_SECTIONS
from scenariogenerator.backend.llm_client import llm_client_factory
from scenariogenerator.backend.load_prompts import load_szenario_verlauf_prompt, get_file_path


def get_gefahr_options():
    return [
        "Chemischer Anschlag",
        "Erdölmangellage",
        "Hagelschlag",
        "Starker Schneefall",
        "Starkregen"
    ]

def get_prompt(gefahr: str) -> str:
    scenario_prompt = load_szenario_verlauf_prompt()
    gefahr_path = get_file_path(gefahr, INDEX_FILE.read_text(encoding="utf-8"))
    gefahr_index_file = (DATA_DIR / gefahr_path).read_text(encoding="utf-8")

    relevant_text = []
    for item in RELEVANT_SECTIONS:
        file_path = get_file_path(item, gefahr_index_file)
        if file_path:
            relevant_text.append((DATA_DIR / file_path).read_text(encoding="utf-8"))

    relevant_text = '\n\n'.join(relevant_text)
    return scenario_prompt.format(text=relevant_text, gefahr=gefahr)

def generate_szenario(prompt: str, model: str, api_token: str | None = None) -> str:
    client = llm_client_factory(model, api_token)
    return client.query(prompt)