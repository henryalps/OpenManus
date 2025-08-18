from .tool_registry import register_tool
from .bash_tool import bash_tool
from .code_executor import execute_python_code
from .crawl import crawl_tool
from .python_repl import python_repl_tool
from .search import bing_tool
from .tts import text_to_speech
from .tool_creator import create_tool

register_tool("bash", bash_tool, "src.tools.bash_tool", "bash_tool")
register_tool("execute_python_code", execute_python_code, "src.tools.code_executor", "execute_python_code")
register_tool("crawl", crawl_tool, "src.tools.crawl", "crawl_tool")
register_tool("python_repl", python_repl_tool, "src.tools.python_repl", "python_repl_tool")
register_tool("search", bing_tool, "src.tools.search", "bing_tool")
register_tool("text_to_speech", text_to_speech, "src.tools.tts", "text_to_speech")
register_tool("create_tool", create_tool, "src.tools.tool_creator", "create_tool")

from .graphrag import build_knowledge_graph, query_knowledge_graph
register_tool("build_knowledge_graph", build_knowledge_graph, "src.tools.graphrag", "build_knowledge_graph")
register_tool("query_knowledge_graph", query_knowledge_graph, "src.tools.graphrag", "query_knowledge_graph")

from .prompt_manager import create_prompt, update_prompt, delete_prompt
register_tool("create_prompt", create_prompt, "src.tools.prompt_manager", "create_prompt")
register_tool("update_prompt", update_prompt, "src.tools.prompt_manager", "update_prompt")
register_tool("delete_prompt", delete_prompt, "src.tools.prompt_manager", "delete_prompt")
