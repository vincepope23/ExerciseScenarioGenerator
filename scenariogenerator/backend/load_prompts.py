import re

def load_szenario_verlauf_prompt() -> str:
    with open("scenariogenerator/prompts/szenario_verlauf_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def get_file_path(keyword: str, markdown_text: str) -> str | None:
    pattern = rf'\[{keyword}\]\((.*?)\)'
    match = re.search(pattern, markdown_text)
    return match.group(1) if match else None