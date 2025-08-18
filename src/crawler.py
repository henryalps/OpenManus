import requests
from bs4 import BeautifulSoup

class Crawler:
    def crawl(self, url: str):
        """
        Crawls a web page and returns its text content.

        Args:
            url (str): The URL of the web page to crawl.

        Returns:
            str: The text content of the web page.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text and clean it up
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            return text
        except requests.exceptions.RequestException as e:
            return f"Error fetching the URL: {e}"
        except Exception as e:
            return f"An error occurred: {e}"
