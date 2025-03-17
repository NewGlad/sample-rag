import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from pydbantic import Database, DataBaseModel, Default, PrimaryKey, Unique

from sample_rag.models import Item
from sample_rag.pdf_utils import (DATASET_BASE_PATH, extract_text_from_pdf,
                                  parse_document)

loop = asyncio.get_event_loop()


def time_now_str():
    return datetime.now().isoformat()


# embeds the plain pydantic model to database model to handle metadata / db specific fields separately
class DatabaseItem(DataBaseModel, Item):
    # to avoid possible duplicates, filename will be a primary ID in db to ensure uniqueness
    filename: str = PrimaryKey()
    created_at: str = Default(default=time_now_str)


async def populate_database() -> list[Item]:
    db_items: list[DatabaseItem] = []
    for document_path in DATASET_BASE_PATH.glob("*.pdf"):
        document_text = extract_text_from_pdf(document_path.name)
        item = parse_document(document_text)
        db_items.append(DatabaseItem(filename=document_path.name, **item.dict()))
    await DatabaseItem.insert_many(db_items)


ITEMS_DATABASE = loop.run_until_complete(
    Database.create("sqlite:///rag_data.db", tables=[DatabaseItem])
)

# TODO: call `populate` somewhere
