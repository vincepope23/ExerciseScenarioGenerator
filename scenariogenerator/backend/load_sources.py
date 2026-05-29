import re

from scenariogenerator.constants import DATA_DIR, INDEX_FILE, RELEVANT_SECTIONS


def load_main_index_file():
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return f.read()

def get_topic_file(topic, gefahr_index_file: str) -> str | None:
    file_path = get_file_path(topic, gefahr_index_file)
    if file_path:
        return (DATA_DIR / file_path).read_text(encoding="utf-8")
    return None

def get_all_relevant_texts(gefahr):
    text_var_dict = {'gefahr': gefahr}
    gefahr_path = get_file_path(gefahr, INDEX_FILE.read_text(encoding="utf-8"))
    gefahr_index_file = (gefahr_path).read_text(encoding="utf-8")
    for aspect in RELEVANT_SECTIONS:
        file_path = get_file_path(aspect, gefahr_index_file)
        if file_path:
            relevant_text = file_path.read_text(encoding="utf-8")
            text_var_dict["gefahr_" + aspect.lower()] = relevant_text
    return text_var_dict

def get_file_path(keyword: str, markdown_text: str) -> str | None:
    pattern = rf'\[{keyword}\]\((.*?)\)'
    match = re.search(pattern, markdown_text)
    return DATA_DIR / match.group(1) if match else None