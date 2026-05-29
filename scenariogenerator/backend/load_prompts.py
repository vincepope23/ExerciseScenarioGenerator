from scenariogenerator.constants import PROMPTS_DIR


def load_szenario_verlauf_prompt() -> str:
    prompt_path = PROMPTS_DIR / "szenario_verlauf_prompt_bare.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def load_user_input_prompt()-> str:
    prompt_path = PROMPTS_DIR / "prompt_text_frontend.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()
