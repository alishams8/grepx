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
TOGETHER_API_TOKEN = os.getenv("TOGETHER_API_TOKEN")
Weaviate_TOKEN = os.getenv("Weaviate_TOKEN")
OpenAI_TOKEN = os.getenv("OPEN_API")

llm = TogetherLLM(
    model="NousResearch/Nous-Hermes-2-Mistral-7B-DPO",
    api_key=TOGETHER_API_TOKEN
)
embed_model = TogetherEmbedding(
    model_name="togethercomputer/m2-bert-80M-8k-retrieval",
    api_key=TOGETHER_API_TOKEN
)

Settings.embed_model = embed_model
Settings.llm = llm


# Create the directory
# os.makedirs('data', exist_ok=True)

# # Download the file
# url = 'https://www.gutenberg.org/cache/epub/2852/pg2852.txt'
file_path = 'data/The Hound of the Baskervilles.txt'

# response = requests.get(url)
# with open(file_path, 'wb') as file:
#     file.write(response.content)

# # Load the document using SimpleDirectoryReader
documents = SimpleDirectoryReader(
    input_files=[file_path]
).load_data()

# # Optional: Print the loaded documents to verify
# print(documents)


from llama_index.core import KnowledgeGraphIndex
from llama_index.core import StorageContext
from llama_index.graph_stores.neo4j import Neo4jGraphStore


graph_store = Neo4jGraphStore(
    username="neo4j",
    password="neo4jneo4j",
    url="bolt://localhost",
    database="neo4j",
)

storage_context = StorageContext.from_defaults(graph_store=graph_store)

# NOTE: can take a while!
index = KnowledgeGraphIndex.from_documents(
    documents,
    storage_context=storage_context,
    max_triplets_per_chunk=2,
    include_embeddings=True,
)



query_engine = index.as_query_engine(
    include_text=False,
    response_mode="tree_summarize",
    similarity_top_k=5,
    verbose=True,
)


from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.core import StorageContext
import weaviate

# cloud
cluster_url = "https://agtomjarmeix6u0jiy3a.c0.europe-west3.gcp.weaviate.cloud"
api_key = Weaviate_TOKEN

client = weaviate.connect_to_wcs(
    cluster_url=cluster_url,
    auth_credentials=weaviate.auth.AuthApiKey(api_key),
)

# local
# client = connect_to_local()

vector_store = WeaviateVectorStore(
    weaviate_client=client, index_name="LlamaIndex" ,embed_model=embed_model
)
storage_context_vector = StorageContext.from_defaults(vector_store=vector_store)
index_vector = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context_vector , embeddings=embed_model
)

query_engine_vector = index_vector.as_query_engine(verbose=True)


from llama_index.core.tools import QueryEngineTool, ToolMetadata
import pandas as pd

from llama_agents import (
    AgentService,
    ToolService,
    LocalLauncher,
    MetaServiceTool,
    ControlPlaneServer,
    SimpleMessageQueue,
    AgentOrchestrator,
)

from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.llms.openai import OpenAI


# TODO: Try optimize descriptions 
tool_KG = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="NEO4J",
        description=(
            "This is a knowledge graph query engine. Users can input queries with specific keywords or patterns, "
            "which the agent translates into Cypher queries to search and retrieve information from the Neo4j graph database. "
            "Use a detailed plain text question as input to this tool."
        ),
    ),
)

tool_vector = QueryEngineTool(
    query_engine=query_engine_vector,
    metadata=ToolMetadata(
        name="VECTOR",
        description=(
            "This is a vector store query engine. Users can input queries with specific keywords or patterns, "
            "which the agent translates into vector representations to perform similarity searches within the vector database. "
            "Use a detailed plain text question as input to this tool."
        ),
    ),
)


# create our multi-agent framework components
message_queue = SimpleMessageQueue()
control_plane = ControlPlaneServer(
    message_queue=message_queue,
    orchestrator=AgentOrchestrator( llm=OpenAI(model="gpt-3.5-turbo-0125", api_key="sk-"),),
)

# define Tool Service
tool_service = ToolService(
    message_queue=message_queue,
    tools=[tool_KG,tool_vector],
    running=True,
    step_interval=0.5,
)

# define meta-tools here
meta_tool_KG = MetaServiceTool.from_tool_service(
        tool_KG.metadata.name,
        message_queue=message_queue,
        tool_service=tool_service,
    )


meta_tool_vector = MetaServiceTool.from_tool_service(
        tool_vector.metadata.name,
        message_queue=message_queue,
        tool_service=tool_service,
    )

# define Agent and agent service

# TODO: optimize agent description 
worker1 = FunctionCallingAgentWorker.from_tools(
    [tool_KG],
    llm=OpenAI(model="gpt-3.5-turbo-0125", api_key=OpenAI_TOKEN),
)
agent1 = worker1.as_agent()
agent_server_1 = AgentService(
    agent=agent1,
    message_queue=message_queue,
    description="The Knowledge Graph Agent Service .Use it for exploring entity relationships hierarchical data queries, and multi-hop queries. Perfect for detailed document searches based on content relationships.",
    service_name="KG_AGENT",
)


worker2 = FunctionCallingAgentWorker.from_tools(
    [meta_tool_vector],
    llm=OpenAI(model="gpt-3.5-turbo-0125", api_key=OpenAI_TOKEN),
)
agent2 = worker2.as_agent()
agent_server_2 = AgentService(
    agent=agent2,
    message_queue=message_queue,
    description="The Vector Store Agent Service Ideal for finding similar documents,and provide generalized answers",
    service_name="VECTOR_AGENT",
)

import logging

# change logging level to enable or disable more verbose logging
logging.getLogger("llama_agents").setLevel(logging.INFO)

## Define Launcher
launcher = LocalLauncher(
    [agent_server_1,agent_server_2,tool_service],
    control_plane,
    message_queue,
)

question ="""What key evidence does Sherlock Holmes find in the portrait of Hugo Baskerville?"""
result = launcher.launch_single(question)