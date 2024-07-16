from llama_index.llms.together import TogetherLLM
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.core import SimpleDirectoryReader
import logging
import sys
import os
import requests
import nest_asyncio
from llama_index.core import Settings
from IPython.display import Markdown, display
nest_asyncio.apply()


from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

HUGGING_FACE_API_KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN")


llm = TogetherLLM(
    model="NousResearch/Nous-Hermes-2-Mistral-7B-DPO",
    api_key=HUGGING_FACE_API_KEY
)
embed_model = TogetherEmbedding(
    model_name="togethercomputer/m2-bert-80M-8k-retrieval",
    api_key=HUGGING_FACE_API_KEY
)

Settings.embed_model = embed_model
Settings.llm = llm


# Create the directory
os.makedirs('data', exist_ok=True)

# Download the file
url = 'https://www.gutenberg.org/cache/epub/2852/pg2852.txt'
file_path = 'data/The Hound of the Baskervilles.txt'

response = requests.get(url)
with open(file_path, 'wb') as file:
    file.write(response.content)

# Load the document using SimpleDirectoryReader
documents = SimpleDirectoryReader(
    input_files=[file_path]
).load_data()

# Optional: Print the loaded documents to verify
print(documents)