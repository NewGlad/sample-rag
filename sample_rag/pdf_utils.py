from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

from sample_rag.models import Item

load_dotenv()
openai_client = OpenAI()

DATASET_BASE_PATH = Path("dataset")


def extract_text_from_pdf(filename: Path) -> str:
    reader = PdfReader(DATASET_BASE_PATH / filename)
    text = (
        "Filename: "
        + filename
        + "\n"
        + "\n".join(page.extract_text() for page in reader.pages)
    )
    return text


def parse_document(document_text: str) -> Item:
    completion = openai_client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": "Your task is to parse given text to specified pydantic schema. Please provide result as much accurate as possible",
            },
            {"role": "user", "content": f"Document: ```{document_text}```"},
        ],
        response_format=Item,
    )
    return completion.choices[0].message.parsed
