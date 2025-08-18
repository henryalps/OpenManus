import pytest
from src.tools.tool_creator import create_tool
from src.tools.tool_registry import get_tool

from src.tools.prompt_manager import create_prompt, update_prompt, delete_prompt
from src.prompts.prompt_registry import get_prompt
from src.tools.graphrag import build_knowledge_graph, query_knowledge_graph

def test_create_tool():
    """Test that a new tool can be created and used."""
    tool_code = """
def my_new_tool(a: int, b: int) -> int:
    \"\"\"A new tool that adds two numbers.\"\"\"
    return a + b
"""
    create_tool({"name": "my_new_tool", "code": tool_code})
    new_tool = get_tool("my_new_tool")
    assert new_tool is not None
    assert new_tool.invoke({"a": 1, "b": 2}) == 3

def test_create_prompt():
    """Test that a new prompt can be created."""
    create_prompt({"name": "my_new_prompt", "prompt": "This is a new prompt."})
    new_prompt = get_prompt("my_new_prompt")
    assert new_prompt is not None
    assert new_prompt == "This is a new prompt."

def test_update_prompt():
    """Test that an existing prompt can be updated."""
    create_prompt({"name": "my_prompt_to_update", "prompt": "This is the original prompt."})
    update_prompt({"name": "my_prompt_to_update", "prompt": "This is the updated prompt."})
    updated_prompt = get_prompt("my_prompt_to_update")
    assert updated_prompt is not None
    assert updated_prompt == "This is the updated prompt."

def test_delete_prompt():
    """Test that a prompt can be deleted."""
    create_prompt({"name": "my_prompt_to_delete", "prompt": "This is a prompt to delete."})
    delete_prompt({"name": "my_prompt_to_delete"})
    deleted_prompt = get_prompt("my_prompt_to_delete")
    assert deleted_prompt is None

def test_build_knowledge_graph(mocker):
    """Test the build_knowledge_graph tool."""
    mock_driver = mocker.patch("src.tools.graphrag.GraphDatabase.driver")
    mock_embedder = mocker.patch("src.tools.graphrag.OpenAIEmbeddings")
    mock_llm = mocker.patch("src.tools.graphrag.OpenAILLM")
    mock_pipeline_instance = mocker.MagicMock()
    mock_pipeline_instance.run = mocker.MagicMock()
    mock_pipeline = mocker.patch("src.tools.graphrag.SimpleKGPipeline", return_value=mock_pipeline_instance)
    mocker.patch("asyncio.run", return_value=None)

    result = build_knowledge_graph("Some text.")

    mock_driver.assert_called_once()
    mock_embedder.assert_called_once()
    mock_llm.assert_called_once()
    mock_pipeline.assert_called_once()
    mock_pipeline_instance.run_async.assert_called_once_with(text="Some text.")
    assert result == "Knowledge graph built successfully."

def test_query_knowledge_graph(mocker):
    """Test the query_knowledge_graph tool."""
    mocker.patch("src.tools.graphrag.GraphDatabase.driver")
    mocker.patch("src.tools.graphrag.OpenAIEmbeddings")
    mocker.patch("src.tools.graphrag.OpenAILLM")
    mocker.patch("neo4j_graphrag.retrievers.VectorRetriever")
    mocker.patch("neo4j_graphrag.generation.GraphRAG")
    result = query_knowledge_graph("A query.")
    assert result is not None
