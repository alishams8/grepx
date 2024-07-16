from llama_index.llms.together import TogetherLLM
from llama_index.embeddings.together import TogetherEmbedding
import logging
import sys
import os
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