import asyncio
import logging

from sample_rag.agent import Agent
from sample_rag.database import ITEMS_DATABASE, populate_database

logging.basicConfig(level=logging.INFO)


logger = logging.getLogger()

cursor = ITEMS_DATABASE.engine.execute("select count(*) from DatabaseItem")
database_size = cursor.scalars().first()
if not database_size:
    logger.info("Database does not exist, preparing data in the very first run...")
    asyncio.run(populate_database())
    logger.info("Database is ready!")

agent = Agent()


test_questions = [
    "How much does the XBO 4000 W/HS XL OFR weigh?",
    "Which luminaire is best suited for my home theater?",
    "Give me all lamps with at least 1500W and a lifetime of more than 3000 hours.",
    "What is the smallest unit I can order?",
    "Which luminaire has the SCIP number dd2ddf15-037b-4473-8156-97498e721fb3?",
]

for question in test_questions:
    print("=" * 15)
    print(f"Question: {question}")
    answer = agent.answer(question)
    print(f"Answer: {answer}")
