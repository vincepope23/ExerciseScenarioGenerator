import io
import json
import time
from pathlib import Path
from tqdm import tqdm

import pdfplumber

from scenariogenerator.backend.llm_client import llm_client_factory
from scenariogenerator.constants import DATA_DIR, PROMPTS_DIR, MISTRAL_API_KEY

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

# def get_ingest_prompt(file_name):
#     file_path = PROMPTS_DIR / file_name
#     with open(file_path, "r", encoding="utf-8") as f:
#         text = f.read()
#         return text

class ScenarioIngestor:

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

    def __init__(self):
        self.llm_client = llm_client_factory("mistral", MISTRAL_API_KEY)
        self.source_dir = DATA_DIR / 'Gefährdungsszenarien'
        self.main_dir = DATA_DIR

    def save_pdfs_as_md_files(self):
        for file_path in self.source_dir.iterdir():
            if not file_path.suffix.lower() == '.pdf':
                continue
            md_file_path_source = self.source_dir / file_path.with_suffix(".md").name
            if md_file_path_source.exists():
                continue
            md_text = pdf_to_md_text(file_path)
            with open(md_file_path_source, "w", encoding="utf-8") as f:
                f.write(md_text)
            print(f"Markdown-Datei gespeichert unter: {md_file_path_source}")

    def ingest_all(self):
        print('Start ingesting scenarios')
        self.save_pdfs_as_md_files()
        analyze_prompt = self._load_prompt("analyze_szenario_prompt.txt")
        json_prompt = self._load_prompt("md_to_json_prompt.txt")
        aspect_prompt = self._load_prompt("summarize_aspect_prompt.txt")

        index_md_all = "# Gefährdungsszenarien\n\n"
        index_md_all_path = self.main_dir / "Gefährdungsszenarien_index.md"

        for md_file_path in self.source_dir.glob("*.md"):
            print(md_file_path)
            md_text = md_file_path.read_text(encoding="utf-8")
            analyze_response = self.llm_client.query(analyze_prompt.format(text = md_text))
            print(f'Analyze response: {len(analyze_response)}')
            json_response = self.llm_client.query(json_prompt.format(text = analyze_response))
            print(f'JSON response: {len(json_response)}')
            scenario_dict = json.loads(json_response)
            scenario_dict["Quelle"] = str(self.source_dir / md_file_path.with_suffix(".pdf").name)
            gefahr = scenario_dict["Gefahr"].replace(" ", "_")
            print(gefahr)
            index_md_gefahr_path = self.main_dir / f"{gefahr}_index.md"
            index_md_all += f"- [{scenario_dict['Gefahr']}]({index_md_gefahr_path.name})\n"


            index_md_gefahr = f"# {scenario_dict['Gefahr']}\n\n"
            for aspect in tqdm(self.index_keys):
                detail_path = self.main_dir / f"{gefahr}_{aspect}.md"
                index_md_gefahr += f"- [{aspect}]({detail_path.name})\n"
                if detail_path.exists():
                    continue
                aspect_response = self.llm_client.query(aspect_prompt.format(item=aspect, text=md_text))
                time.sleep(20)
                detail_path.write_text(
                    f"Quelle:[{scenario_dict['Quelle']}]({scenario_dict['Quelle']})\n\n## {aspect}\n\n{aspect_response}",
                    encoding="utf-8")

            index_md_gefahr_path.write_text(index_md_gefahr, encoding="utf-8")
            print(index_md_all)

        index_md_all_path.write_text(index_md_all, encoding="utf-8")

    def _load_prompt(self, filename: str) -> str:
        return (PROMPTS_DIR / filename).read_text(encoding="utf-8")
