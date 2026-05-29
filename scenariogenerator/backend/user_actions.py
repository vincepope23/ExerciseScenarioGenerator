from scenariogenerator.backend.constants import GEFAHR_OPTIONS, MISTRAL_API_KEY
from scenariogenerator.backend.llm_client import llm_client_factory
from scenariogenerator.backend.load_prompts import load_szenario_verlauf_prompt
from scenariogenerator.backend.load_sources import get_all_relevant_texts


def get_gefahr_options():
    return GEFAHR_OPTIONS

def get_prompt(gefahr: str) -> str:
    scenario_prompt = load_szenario_verlauf_prompt()
    relevant_texts = get_all_relevant_texts(gefahr)
    return scenario_prompt.format(text=relevant_texts, gefahr=gefahr)

def generate_szenario(prompt: str, model) -> str:
    assert MISTRAL_API_KEY is not None, "MISTRAL_API_KEY not defined"
    client = llm_client_factory(model, MISTRAL_API_KEY)
    return client.query(prompt)