
from src.tools.search import bing_tool as search_tool
from src.tools.crawl import crawl_tool
from src.llms.llm import get_llm_by_type

def search_and_summarize(query: str) -> str:
    '''
    Searches the web for a query, crawls the top result, and summarizes the content.

    Args:
        query (str): The query to search for.

    Returns:
        str: The summarized content of the top search result.
    '''
    llm = get_llm_by_type("reasoning")
    search_results = search_tool.invoke({"query": query})
    if not search_results:
        return "Error: No search results found."

    # This assumes search_results is a list of dicts with a 'url' key
    top_result_url = search_results[0]["url"]
    crawled_content = crawl_tool.invoke({"url": top_result_url})

    summary_prompt = f"Please summarize the following content:\n\n{crawled_content}"
    summary = llm.invoke(summary_prompt)

    return summary.content
