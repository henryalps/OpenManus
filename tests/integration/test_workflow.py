import pytest 
from src.workflow.graph import build_graph

def test_workflow_initialization():
    """Test that the LangGraph workflow can be initialized."""
    graph = build_graph()
    assert graph is not None