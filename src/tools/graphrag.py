import asyncio
from neo4j import GraphDatabase
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.llm import OpenAILLM

from src.config.env import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD
from langchain_core.tools import tool

@tool
def build_knowledge_graph(text: str) -> str:
    """
    Builds a knowledge graph from a string of text.

    Args:
        text (str): The text to build the knowledge graph from.

    Returns:
        str: A message indicating the knowledge graph was built successfully.
    """
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

        node_types = ["Person", "House", "Planet"]
        relationship_types = ["PARENT_OF", "HEIR_OF", "RULES"]
        patterns = [
            ("Person", "PARENT_OF", "Person"),
            ("Person", "HEIR_OF", "House"),
            ("House", "RULES", "Planet"),
        ]

        embedder = OpenAIEmbeddings(model="text-embedding-3-large")
        llm = OpenAILLM(
            model_name="gpt-4o",
            model_params={
                "max_tokens": 2000,
                "response_format": {"type": "json_object"},
                "temperature": 0,
            },
        )

        kg_builder = SimpleKGPipeline(
            llm=llm,
            driver=driver,
            embedder=embedder,
            schema={
                "node_types": node_types,
                "relationship_types": relationship_types,
                "patterns": patterns,
            },
            on_error="IGNORE",
            from_pdf=False,
        )

        asyncio.run(kg_builder.run_async(text=text))
        driver.close()
        return "Knowledge graph built successfully."
    except Exception as e:
        return f"Error building knowledge graph: {e}"

@tool
def query_knowledge_graph(query: str) -> str:
    """
    Queries the knowledge graph and returns a response.

    Args:
        query (str): The query to ask the knowledge graph.

    Returns:
        str: The response from the knowledge graph.
    """
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

        embedder = OpenAIEmbeddings(model="text-embedding-3-large")
        llm = OpenAILLM(model_name="gpt-4o", model_params={"temperature": 0})

        retriever = VectorRetriever(driver, "vector-index", embedder)
        rag = GraphRAG(retriever=retriever, llm=llm)

        response = rag.search(query_text=query)
        driver.close()
        return response.answer
    except Exception as e:
        return f"Error querying knowledge graph: {e}"
