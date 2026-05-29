from scenariogenerator.constants import PROMPTS_DIR


def load_szenario_verlauf_prompt() -> str:
    prompt_path = PROMPTS_DIR / "szenario_verlauf_prompt.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


