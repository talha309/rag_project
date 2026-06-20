from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5",
    api_key = GEMINI_API_KEY
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="model/text-embedding-001",
    api_key=GEMINI_API_KEY
)

