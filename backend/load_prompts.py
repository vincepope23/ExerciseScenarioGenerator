def load_szenario_verlauf_prompt() -> str:
    with open("prompts/szenario_verlauf_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()


