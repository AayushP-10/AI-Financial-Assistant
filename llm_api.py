import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ClaudeAPI:
    def __init__(self):
        self.api_url = os.getenv('API_URL')
        self.model = os.getenv('MODEL')
        self.api_key = os.getenv('API_KEY')
        print("Loaded API_URL:", self.api_url)  # Debug print
        if not self.api_url or not self.model or not self.api_key:
            raise ValueError("API_URL, MODEL, or API_KEY not found in environment variables")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_response(self, data_snippet: str, user_question: str) -> str:
        """
        Send a request to the Groq API and get the response.
        
        Args:
            data_snippet (str): Formatted string of the CSV data
            user_question (str): User's question about the data
            
        Returns:
            str: Model's response
        """
        system_prompt = """You are a financial data assistant. Analyze the following CSV data and answer user questions clearly, using data where appropriate. \
        If you notice any patterns or trends, mention them. Be concise but informative."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the data:\n{data_snippet}\n\nQuestion: {user_question}"}
        ]

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": messages
                }
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Unexpected API response format: {str(e)}") 