import json
import logging
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from sample_rag.database import ITEMS_DATABASE
from sample_rag.models import Item
from sample_rag.pdf_utils import extract_text_from_pdf

load_dotenv()
openai_client = OpenAI()

logger = logging.getLogger()


class Agent:
    __openai_tools_defition = [
        {
            "type": "function",
            "function": {
                "name": "tool_read_pdf_content",
                "description": """
                    Allows to read entire content of arbitrary document from dataset folder in text format.
                """,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "File name of required document",
                        }
                    },
                    "required": ["filename"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        },
        {
            "type": "function",
            "function": {
                "name": "tool_execute_sql",
                "description": "Executes given SQL query in the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sql_query": {
                            "type": "string",
                            "description": "SQL query for finding a required data",
                        }
                    },
                    "required": ["sql_query"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        },
    ]

    def __init__(self, openai_model: str = "gpt-4o"):
        self.openai_model = openai_model

    def _tool_execute_sql(self, sql_query: str) -> list[Item]:
        try:
            cursor = ITEMS_DATABASE.engine.execute(sql_query)
            db_items = cursor.mappings().all()
            return f"query results: {db_items}"
        except Exception as e:
            logger.exception("`tool_execute_sql` error")
            return f"query error: {e}"

    def _tool_read_pdf_content(filename: Path) -> str:
        if not filename.exists():
            return "read pdf error: given file does not exist"
        return extract_text_from_pdf(filename)

    def answer(self, question: str) -> str:
        return self._answer_imlp(question, messages=None)

    def _answer_imlp(self, question: str, messages: list | None) -> str:
        if messages is None:
            messages = [
                {
                    "role": "system",
                    "content": """
                You are advanced sales assistant.
                In the next message, you will get a customer question about the available assortment.
                Your task is to answer the questions as much precise as possible.
                Feel free to use available tools: tool_read_pdf_content,  tool_execute_sql.

                Database details:
                    Engine: sqlite3
                    
                    !IMPORTANT!
                    For filtering text fields instead of equality (operator =), use fuzzy comparison using `like`.
                    For example, instead of `varchar_field = "a"` use `varchar_field like "%a%"`
                    This will provide a more sustainable results.
                    Also, if you wasn't able to find required data in the database, you have to make one or two more query trying find required data. 
             
                    Table schema:
                    ```
                        CREATE TABLE IF NOT EXISTS "DatabaseItem" (
                            product_name VARCHAR(60) NOT NULL, 
                            product_family VARCHAR(60) NOT NULL, 
                            color_temperature VARCHAR(60) NOT NULL, 
                            power_range VARCHAR(60) NOT NULL, 
                            color_rendering_index VARCHAR(60) NOT NULL, 
                            description VARCHAR(60) NOT NULL, 
                            advantages VARCHAR(60) NOT NULL, 
                            application_areas VARCHAR(60) NOT NULL, 
                            rated_current FLOAT NOT NULL, 
                            current_control_min FLOAT NOT NULL, 
                            current_control_max FLOAT NOT NULL, 
                            rated_power FLOAT NOT NULL, 
                            rated_voltage FLOAT NOT NULL, 
                            diameter FLOAT NOT NULL, 
                            length FLOAT NOT NULL, 
                            length_excluding_base FLOAT NOT NULL, 
                            light_center_length FLOAT NOT NULL, 
                            electrode_gap FLOAT NOT NULL, 
                            product_weight FLOAT NOT NULL, 
                            cable_length FLOAT NOT NULL, 
                            max_ambient_temperature FLOAT NOT NULL, 
                            lifespan FLOAT NOT NULL, 
                            anode_socket VARCHAR(60) NOT NULL, 
                            cathode_socket VARCHAR(60) NOT NULL, 
                            reach_declaration_date VARCHAR(60) NOT NULL, 
                            primary_product_number VARCHAR(60) NOT NULL, 
                            candidate_substance VARCHAR(60) NOT NULL, 
                            candidate_substance_cas VARCHAR(60) NOT NULL, 
                            scip_declaration_number VARCHAR(60) NOT NULL, 
                            ean VARCHAR(60) NOT NULL, 
                            metel_code VARCHAR(60) NOT NULL, 
                            packaging_product_code VARCHAR(60) NOT NULL, 
                            packaging_product_name VARCHAR(60) NOT NULL, 
                            packaging_unit INTEGER NOT NULL, 
                            dimension_length FLOAT NOT NULL, 
                            dimension_width FLOAT NOT NULL, 
                            dimension_height FLOAT NOT NULL, 
                            volume FLOAT NOT NULL, 
                            gross_weight FLOAT NOT NULL, 
                            filename VARCHAR(60) NOT NULL, 
                            created_at VARCHAR(60), 
                            PRIMARY KEY (filename)
                        );
                ```
            """,
                },
                {"role": "user", "content": question},
            ]

        completion = openai_client.beta.chat.completions.parse(
            model=self.openai_model,
            messages=messages,
            n=1,
            temperature=0.1,
            tools=self.__openai_tools_defition,
        )
        if not completion.choices[0].message.tool_calls:
            # final result
            return completion.choices[0].message.content

        for tool_call in completion.choices[0].message.tool_calls:
            messages.append(completion.choices[0].message.model_dump())
            tool_name = tool_call.function.name
            tool_arguments = json.loads(tool_call.function.arguments)

            if tool_name == "tool_read_pdf_content":
                result = self._tool_read_pdf_content(tool_arguments["filename"])
            elif tool_name == "tool_execute_sql":
                result = self._tool_execute_sql(tool_arguments["sql_query"])
            else:
                logger.error("Unknown tool name %s", tool_name)
                raise ValueError(f"Unknown tool name: {tool_name}")

            messages.append(
                {"role": "tool", "tool_call_id": tool_call.id, "content": result}
            )
        return self._answer_imlp(question, messages)
