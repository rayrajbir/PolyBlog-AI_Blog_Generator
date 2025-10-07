from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

class GroqLLM:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

    def get_llm(self):
        try:
            llm = ChatGroq(api_key=self.api_key, model="llama-3.1-8b-instant")
            return llm
        except Exception as e:
            print(f"Error occurred with exception: {e}")
            return None
