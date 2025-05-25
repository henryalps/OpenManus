import logging
from src.tools.browser import browser_tool  # Import the existing browser tool
from .decorators import create_logged_tool

logger = logging.getLogger(__name__)

# Initialize Bing search tool using browser tool with logging
LoggedBrowserSearch = create_logged_tool(
    browser_tool.__class__
)  # Use the class of browser_tool
bing_tool = LoggedBrowserSearch(
    name="bing_search", description="Search Bing using a headless browser."
)  # Updated name and description
