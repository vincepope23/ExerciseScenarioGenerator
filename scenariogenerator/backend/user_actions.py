from scenariogenerator.backend.load_schauplatz_options import load_schauplatz_options, load_ausdehnung
from scenariogenerator.constants import GEFAHR_OPTIONS, MISTRAL_API_KEY
from scenariogenerator.backend.llm_client import llm_client_factory
from scenariogenerator.backend.load_prompts import load_szenario_verlauf_prompt, load_user_input_prompt
from scenariogenerator.backend.load_sources import get_all_relevant_texts


def get_gefahr_options():
    return GEFAHR_OPTIONS

def get_user_input_prompt():
    return load_user_input_prompt()

def get_locations(gefahr):
    return load_schauplatz_options(gefahr)

def generate_szenario(gefahr: str, location: str, user_input: str, model) -> str:
    assert MISTRAL_API_KEY is not None, "MISTRAL_API_KEY not defined"
    client = llm_client_factory(model, MISTRAL_API_KEY)
    scenario_prompt = load_szenario_verlauf_prompt()
    text_var_dict = get_all_relevant_texts(gefahr)
    text_var_dict["userinput_text"] = user_input
    text_var_dict["hauptschauplatz"] = location
    text_var_dict["räumliche_ausdehnung"] = load_ausdehnung(gefahr, location)
    complete_prompt = scenario_prompt.format(**text_var_dict)
    print(complete_prompt)
    print(len(complete_prompt))
    return client.query(complete_prompt)