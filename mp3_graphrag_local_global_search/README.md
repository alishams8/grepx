## GraphRAG local vs Global search

| Aspect        | Global Search                                                       | Local Search                                                                           |
|---------------|---------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| Scope         | Whole dataset reasoning                                             | Entity-based reasoning                                                                 |
| Data Source   | LLM-generated community reports from the graph hierarchy            | Structured data from the knowledge graph and unstructured data from input documents    |
| Method        | Map-reduce approach using community reports                         | Uses entities and their information from the knowledge graph and input documents       |
| Use Case      | Suitable for holistic questions about the entire dataset (e.g., main themes) | Suitable for questions about specific entities and their properties                    |
| Configuration | Extensive parameters including map-reduce prompts and general knowledge inclusion | Simpler set of configuration parameters                                                |
