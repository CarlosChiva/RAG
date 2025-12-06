# RAG Excel Service

This service enables users to interact with Excel files using natural language queries. It provides capabilities to upload Excel files, explore their structure, search for specific data, and edit cells within the files.

## Features

- **File Management**: Upload and list Excel files
- **Data Exploration**: View structure and content of Excel files
- **Natural Language Queries**: Ask questions about Excel data using natural language
- **Data Editing**: Edit specific cells in Excel files with confirmation
- **Security**: JWT-based authentication and backup creation before edits

## Architecture

The service is built with:
- FastAPI for the web framework
- LangChain for natural language processing
- FAISS for vector storage
- Ollama for language model
- Pandas for Excel manipulation

## Endpoints

### Authentication
- `POST /upload_file` - Upload an Excel file
- `GET /list_files` - List uploaded files
- `GET /get_file` - Download a specific file
- `POST /upload_file_edited` - Upload an edited file

### LLM Interaction
- `GET /llm-query` - WebSocket endpoint for natural language queries

## Usage

1. Start the service
2. Upload an Excel file using `/upload_file`
3. Use the WebSocket endpoint `/llm-query` to ask questions about the data
4. The agent will respond with search results, exploration, or editing capabilities

## Security

- All operations require JWT authentication
- Before editing any cell, the system creates a backup
- Editing requires explicit confirmation (`confirmacion=SI`)

## Dependencies

- Python 3.12+
- FastAPI
- LangChain
- FAISS
- Ollama
- Pandas
- OpenPyXL

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Start the service: `uvicorn main:app --host 0.0.0.0 --port 8000`
