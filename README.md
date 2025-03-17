# PDF Document Search Solution with LLM

## Overview

This repository demonstrates a search solution built on PDF documents using a Language Model (LLM). The primary goal is to enable precise and advanced search capabilities on structured data extracted from PDF files using a Retrieval Augmented Generation (RAG) approach.

## Project Goals

- **RAG with PDF Documents:**  
  Develop a system that ingests PDF documents with defined content, extracts relevant data, and stores it in a structured format for efficient retrieval.

- **Search Tool Development:**  
  Build a simple search tool that accepts user queries directly from the code (no additional UI is required). The PDF documents are accessed from a fixed location on the file system.

## Why Not a Basic Semantic Search?

While embedding-based semantic search with top_n document retrieval is a popular approach, it is not ideal for this project due to the nature of the queries we expect. Test queries include:

1. **Exact filtering by product details:**  
   - Example: "How much does the XBO 4000 W/HS XL OFR weigh?"
2. **Complex numeric filters:**  
   - Example: "Give me all lamps with at least 1500W and a lifetime of more than 3000 hours."
3. **Order and aggregation queries:**  
   - Example: "What is the smallest unit I can order?"
4. **Exact matching with identifiers:**  
   - Example: "Which luminaire has the SCIP number dd2ddf15-037b-4473-8156-97498e721fb3?"

Semantic search that simply retrieves a fixed number of top documents based on similarity would not suffice for these cases because:

- **Exact filtering is required:** The queries often involve precise matching and numeric comparisons.
- **Advanced data operations:** The solution needs to handle queries that require filtering by thresholds and computing min/max values.
  
The chosen approach is to **parse PDF documents** and store their contents in a database. This allows the LLM to leverage SQL queries over the structured data or read the entire document from the file system if needed.

## How It Works

1. **PDF Ingestion:**  
   PDF documents located in a predetermined directory are parsed to extract the necessary data fields.

2. **Data Structuring and Storage:**  
   The extracted data is stored in a structured database, which makes it possible to execute complex SQL queries for exact matches and numeric filtering.

3. **Search Query Processing:**  
   The LLM, integrated with a tool for executing SQL queries, processes user queries and either:
   - Generates a corresponding SQL query for structured data search, or
   - Reads and retrieves entire documents directly from the file system when needed.

## Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/newglad/sample-rag.git
   cd your-repo
   

2. **Install the dependencies:**
    ```bash
    poetry install

3. **Run the project:**
    ```bash
    poetry run python main.py
