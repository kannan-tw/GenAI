from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain_core.messages import SystemMessage, HumanMessage
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from langchain_neo4j import GraphCypherQAChain, Neo4jGraph

from langchain_core.prompts.prompt import PromptTemplate
import os

SimplifierPrompt = """
Role: 
You are a Neo4j Cypher query expert specializing in breaking down 
and simplifying user queries using the provided schema.
Task:
Break the user question into smaller sub-queries if the question is complex and relevant to the schema. 
    Otherwise, don't break the question.
If user question is not relevant, explain why and ask for refinement.
Simplify or validate the user query and ensure it is semantically correct and 
feasible based on the schema. If the query is irrelevant or unclear, 
provide actionable feedback.

Instructions:

Semantic Validation:

    Ensure the query makes sense given the schema's structure and properties.
    Note: Name of files, class can be anything, it can be property of the node. Ignore properties from validation.
    It doesn't need to match the schema 100% 
        but should be interpretable and feasible to translate into Cypher. 

    If the query does not align with the schema:
        Explain why the query is not relevant to the schema.
        Provide relevant minimum 3 examples or suggestions based on the schema to help the user rephrase or refine their query.
    If parts of the query are invalid or ambiguous, then
        you must help user by providing refined queries with best suitable examples. That enable user to refine the question.
Breakdown:
    Don't break the question unnecessarily.
    IF and only if the user question is COMPLEX, 
        Split the query into smaller, schema-based parts only if needed. 
        Must leverage user provided node properties rather generic names or placeholders.
    If no split is required, then respond user's original question.
Avoid Cypher:
    Do not write Cypher queries.

Examples for reference:
Simplify the query: "Retrieve the code of the file named 'stream-be.py'" into sequential steps. Each step should:

1. Find the file node with the name 'stream-be.py'.
2. Retrieve the file_code directly for the file node 'stream-be.py'.

Output:
If relevant and split:
    Sub-queries:  
    1. [Sub-query 1]  
    2. [Sub-query 2]  
If relevant but no split:
    Respond user's original query.
If not relevant:
    Query not relevant to schema. Reason: [reason with appropriate examples]. 
    Please refine your question. 

Schema:
{schema}

"""

CypherQueryTemplate = """
Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Leverage examples for reference only, do not use as it is. 
If a property or node doesn't exist, suggest alternative queries based on the schema.
Use name or property values which is provided by user. 

Avoid hardcoding properties like "specific_folder_name", 
    instead leverage properties of nodes user another query if it is not provided by user instead of placeholder.

Schema:
{schema}
Note: 
- Most important note: Ask user for more information if you foresee there will be 0 query or more than 2 queries.
- Do not include any explanations or apologies in your responses.
- Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
- Do not include any text except the generated Cypher statement.
- Leverage provided property name, ask user to provide specific name of the properpty, 
rather using generic names.
- Directly use the file name in every query.
- Avoid referring to previously "found nodes" in subsequent steps.

Examples: Here are a few examples of generated Cypher statements for particular questions but not use as it is:
# How many methods or functions are there for each Python file?

MATCH (f:file)-[:CONTAINS]->(m:function)
WHERE f.name ENDS WITH '.py'
RETURN f.name AS PythonFile, COUNT(m) AS FunctionCount


# count of function for each python files
MATCH (f:file)-[*]-(m:function)
WHERE f.name ENDS WITH '.py'
RETURN f.name AS PythonFile, COUNT(m) AS FunctionCount

MATCH (c:class)-[:contains]->(m:method)-[:contains]-(mc:method_code)
WHERE c.name =  'async'
RETURN m.name AS MethodName, mc.code_summary AS MethodSummary

The question is:
{question}

Important: In the generated Cypher query, the RETURN statement must explicitly 
include the property values used in the query's filtering condition, 
alongside the main information requested from the original question.

"""




class SubQuery(BaseModel):
    """Instructions on how to prompt the LLM."""
    sub_queries: str

class AgentState(TypedDict):
    user_query: Annotated[list, add_messages]
    sub_query: Annotated[list, add_messages]
    neo4j_schema: Annotated[list, add_messages]
    final_results: Annotated[list, add_messages]

def neo4j_graph(state):

    
    NEO4J_URI = os.getenv('NEO4J_URI') 
    NEO4J_USER = os.getenv('NEO4J_USER') 
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD') 
    

    neo4j_instance = Neo4jGraph(url=NEO4J_URI, 
                    username=NEO4J_USER, 
                    password=NEO4J_PASSWORD,)
    
    neo4j_instance.refresh_schema()
    schema = neo4j_instance.schema
    print("\n*** Fetched Neo4j Schema ***\n")
    return {"neo4j_schema": [schema]}

def simplifier(state):

    model_name = os.getenv('MODEL_NAME') 
    llm = ChatOpenAI(model=model_name, temperature=0, max_retries=1)
    llm_with_tool = llm.bind_tools([SubQuery])
    llm_with_so = llm.with_structured_output(SubQuery)
    user_query = state['user_query'][-1] 
    schema = state["neo4j_schema"][-1]
    messages = [
        SystemMessage(content=SimplifierPrompt.format(schema=schema)), 
        HumanMessage(content=f"User Query: \n{user_query}")
    ]
    
    response = llm_with_so.invoke(messages)
    
    return {"sub_query": response.sub_queries}

def isValidQuestion(state):
    sub_query = state['sub_query'][-1]
    if "query not relevant to schema" in sub_query.content.lower():
        print("\n")
        print(sub_query.content)
        return 'incorrect'
    else:
        print("\n*** Given question is simplified as :*** \n", sub_query.content)
        return 'correct'


def translate_to_cypher(state):
    
    NEO4J_URI = os.getenv('NEO4J_URI') 
    NEO4J_USER = os.getenv('NEO4J_USER')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD') 
    model_name = os.getenv('MODEL_NAME') 

    graph = Neo4jGraph(url=NEO4J_URI, 
                   username=NEO4J_USER, 
                   password=NEO4J_PASSWORD,)
                   #enhanced_schema=True,)

    llm = ChatOpenAI(model=model_name, temperature=0, max_retries=1)
    queries = state["sub_query"][-1]
    schema = state["neo4j_schema"][-1]
    
    CYPHER_GENERATION_PROMPT = PromptTemplate(
        input_variables=["schema", "question"], template=CypherQueryTemplate
    )
    try:
        chain = GraphCypherQAChain.from_llm(
            llm=ChatOpenAI(temperature=0, model="gpt-4o-mini"), 
            graph=graph, 
            verbose=True, 
            
            qa_llm=ChatOpenAI(temperature=0, model="gpt-4o-mini"),
            cypher_prompt = CYPHER_GENERATION_PROMPT,
            
            validate_cypher=True,
            use_function_response=True,
            function_response_system="Respond as a developer! Use provided data but must not make up the response.",
            allow_dangerous_requests=True
        )
        query_results =[]
        sub_queries = queries.content.split('\n')
        if len(sub_queries) == 1:
            sub_queries = queries
            result = chain.invoke({"query": sub_queries})
            query_results.append(
                result['result']
            )
            
        else:
            for sub_query in sub_queries:
                result = chain.invoke({"query": sub_query})
                query_results.append(
                    result['result']
                )
    except Exception as e:
        print ("\n*** Error occurred while generating cypher ***\n", e)
    print("\n*** Generated the response ***\n")
    print(query_results)
    return {"final_results": query_results}

def build_workflow():
    memory = MemorySaver()
    workflow = StateGraph(AgentState)

    workflow.add_edge(START, "neo4j_graph")
    workflow.add_node("neo4j_graph", neo4j_graph)
    workflow.add_node("simplifier", simplifier)
    workflow.add_node("translate_to_cypher", translate_to_cypher)
    workflow.add_edge("neo4j_graph", "simplifier")
    
    workflow.add_conditional_edges(
    "simplifier", 
    isValidQuestion, 
    {
        "correct": "translate_to_cypher", 
        "incorrect": END}
    )
    workflow.add_edge("translate_to_cypher", END)
    graph = workflow.compile()


    return graph


                

