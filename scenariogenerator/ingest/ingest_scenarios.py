import io
import time
from pathlib import Path

import pdfplumber

from scenariogenerator.backend.llm_client import llm_client_factory
from scenariogenerator.constants import DATA_DIR, PROMPTS_DIR, MISTRAL_API_KEY

index_keys = [
    "Rollen",
    "Hilfsmittel",
    "Massnahmen",
    "Rechtsgrundlagen",
    "Phasen",
    "Schwerestufen",
    "Auswirkungen",
    "Einflussfaktoren",
    "Ereignisbeispiele"
]

def pdf_to_md_text(file_path: Path):
    with open(file_path, "rb") as f:
        pdf_file = io.BytesIO(f.read())

    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def save_pdfs_as_md_files():
    source_dir = DATA_DIR / 'Gefährdungsszenarien'

    for file_path in source_dir.iterdir():
        if not file_path.suffix.lower() == '.pdf':
            continue

        md_file_path_source = source_dir / file_path.with_suffix(".md").name
        if md_file_path_source.exists():
            continue

        md_text = pdf_to_md_text(file_path)

        with open(md_file_path_source, "w", encoding="utf-8") as f:
            f.write(md_text)
        print(f"Markdown-Datei gespeichert unter: {md_file_path_source}")

def get_analyze_scenario_prompt():
    file_path = PROMPTS_DIR / "analyze_szenario_prompt.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        return text

def get_md_to_json_prompt():
    file_path = PROMPTS_DIR / "md_to_json_prompt.md"
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

def get_aspect_detail_prompt():
    file_path = PROMPTS_DIR / "summarize_aspect_prompt.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

def analyze_scenario(md_text_raw):
    prompt = get_analyze_scenario_prompt().format(md_text_raw)
    client = llm_client_factory("mistral", MISTRAL_API_KEY)
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content

def extract_aspect_json_from_scenario_md(md_text_scenario):
    prompt_json = get_md_to_json_prompt.format(md_text_scenario)
    client = llm_client_factory("mistral", MISTRAL_API_KEY)
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {"role": "user", "content": prompt_json}
        ],
    )
    return response.choices[0].message.content

def summarize_aspects(json_dict, md_text_scenario):
    md_content_all = "# Gefährdungsszenarien\n\n"
    gefahr = json_dict['Gefahr']
    gefahr = gefahr.replace(' ', '_')
    gefahr_file = DATA_DIR / Path(gefahr + '_index.md')
    json_dict[gefahr] = gefahr_file
    md_content_all += f"- [{json_dict['Gefahr']}]({Path(gefahr + '_index.md')})\n"
    md_content_szenario = f"# {json_dict['Gefahr']}\n\n"

    prompt_template = get_aspect_detail_prompt()
    for key in index_keys:
        output_path_detail = str(DATA_DIR / Path(f"{gefahr}_{key}.md"))
        md_content_szenario += f"- [{key}]({output_path_detail.split('/')[-1]})\n"
        response_collection = []

        if Path(output_path_detail).exists():
            print(f"{output_path_detail} existiert bereits")
            continue

        for item in json_dict[key]:
            print(item)

            detail_prompt = prompt_template.format(md_text_scenario, item)

            client = llm_client_factory("mistral", MISTRAL_API_KEY)
            response_detail = client.chat.complete(
                model="mistral-large-latest",
                messages=[
                    {"role": "user", "content": detail_prompt}
                ],
            ).choices[0].message.content
            time.sleep(30)

            response_detail = f"## {item}\n\n{response_detail}"
            print(response_detail)
            response_collection.append(response_detail)

            combined_text = f" # {key}\n\n {"\n\n".join(response_collection)}"

            with open(output_path_detail, "w", encoding="utf-8") as f:
                f.write(f"Quelle:[{json_dict['Quelle']}]({json_dict['Quelle']})\n\n{combined_text}")

        with open(gefahr_file, "w", encoding="utf-8") as f:
            f.write(md_content_szenario)

    output_path = DATA_DIR / Path("Gefährdungsszenarien_index.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content_all)
