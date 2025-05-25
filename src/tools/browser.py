from langchain.tools import BaseTool


class BrowserTool(BaseTool):
    name: str = "browser"
    description: str = "Placeholder browser tool"

    def _run(self, instruction: str) -> str:
        return "Browser tool placeholder"

    async def _arun(self, instruction: str) -> str:
        return "Browser tool placeholder"


browser_tool = BrowserTool()
