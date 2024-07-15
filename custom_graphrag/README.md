## About

RAG is a very powerful tool for retrieving information stored in-house, which commonly used LLMs don’t have access to. While RAGs excel with unstructured data, they are less effective with structured data like CSV files. This is where GraphRAG plays a significant role.


simple queries after creation of noe4j graph:

```
MATCH (o:Product)-[:IS_ORDERED_IN]->(p:Order)
RETURN o, p;

MATCH (c:Customer)-[:ORDERED]->(o:Order)
RETURN c, o;

MATCH (o:Order)-[:HAS_BEEN_ORDERED]->(c:Customer)
RETURN o, c;
```

set following in neo4j.conf:

```
dbms.security.procedures.unrestricted=apoc.*

```

## bringing local LLM up and running:

1- Download and install Ollama onto the available supported platforms 
2- Fetch available LLM model via: ollama pull llama3

## create your own model
ollama create mario -f ./Modelfile
ollama run mario
for more info: https://github.com/ollama/ollama
