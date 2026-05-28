import re
from pathlib import Path


def load_szenario_verlauf_prompt() -> str:
    module_dir = Path(__file__).parent.parent
    prompt_path = module_dir / "prompts" / "szenario_verlauf_prompt.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def get_file_path(keyword: str, markdown_text: str) -> str | None:
    pattern = rf'\[{keyword}\]\((.*?)\)'
    match = re.search(pattern, markdown_text)
    return match.group(1) if match else None