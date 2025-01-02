# API
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from code_parsing import extract_hierarchy_with_code
from neo4j_lib import Neo4jLoader
from lg_neo4j  import build_workflow
from langchain_core.messages import SystemMessage, HumanMessage

import json
import os

app = FastAPI()

class LLMConfig(BaseModel):
    api_key: str
    model_name: str
    seed: int
    max_iteration: int

class DBConfig(BaseModel):
    collection_name: str
    #persistent_store: str

class Query(BaseModel):
    user_query: str

class CodeDescription(BaseModel):
    code_dir: str
    allowed_extn: str
    code_summary: str

class Code(BaseModel):
    file_location: str


@app.post("/code_parser_with_summary")
def code_parser_with_summary(codeDesc: CodeDescription):
    # Get user input for root path and allowed extensions
    root_path = codeDesc.code_dir #"/Users/aravind/Documents/Aravind/Knowledge/2024/stretch/Code/uc2"# input("Enter the root directory path: ").strip()
    extensions = codeDesc.allowed_extn# ".py"# input("Enter allowed file extensions (comma-separated, e.g., .py,.txt): ").strip()
    output_file = "code_parser.json"# input("Enter the output JSON file path (e.g., output.json): ").strip()
    includes = ["folders", "files","functions", "classes", "methods", "inline_code"]
    summary_flag = codeDesc.code_summary
    #"imports",
    # Convert extensions input into a list
    allowed_extensions = [ext.strip() for ext in extensions.split(",")]

    # Extract files and save to JSON
    file_data = extract_hierarchy_with_code(root_path, allowed_extensions, includes, output_file, summary_flag)
    
    # Print a summary
    
    response = f"Extracted {len(file_data)} files. File Location :" + output_file
    print(response)
    return response

@app.post("/ingest_data")
def ingest_data(code:Code):
    output_file = code.file_location #"code_parser.json"# input("Enter the output JSON file path (e.g., output.json): ").strip()
    print(output_file)
    try:
        with open(output_file, 'r', encoding='utf-8') as json_file:
            file_data = json.load(json_file)  # Load the JSON content
            print("File Data :\n")
            print(file_data)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
    
    NEO4J_URI = os.getenv('NEO4J_URI') #"neo4j+s://46323621.databases.neo4j.io"
    NEO4J_USER = os.getenv('NEO4J_USER') #"neo4j"
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD') #"1lz1W_N-3x0-O5nz0cPjRLR4vMHetvYnVAq_hz9NPTA"
    loader = Neo4jLoader(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    # Load the data into Neo4j
    result = loader.load_data(file_data)
    # Print a summary
    print(f"Extracted {len(file_data)} files.")
    return "Successuflly ingested" #result

class Configuration (BaseModel):
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str
    model_name: str
class Question (BaseModel):
    USER_INPUT: str

@app.post("/ask_code")
def ask_code( user_input: Question ):
    
    user_input = user_input.USER_INPUT
    graph = build_workflow()
    inputs = {
                "user_query": [HumanMessage(content=user_input)],
            }
    result = graph.invoke(inputs)
    if "Query not relevant to schema" in result['sub_query'][-1].content:
        final_result = result['sub_query'][-1].content
    else:
        final_result = result['final_results'][-1].content
        '''final_result = [
            {
                "input": result['user_query'][-1].content,
                "sub_queries": result['sub_query'][-1].content,
                "output": result['final_results'].content if result.get('final_results') else None
            }
        ]'''
    #print(final_result)
    return final_result
