# About

This repository demonstrates how to import generated Parquet files into Neo4j using APOC procedures and taken from this repo: https://gist.github.com/jexp/74bd5a43305550236321eab8f0c723c0 . 

However, this is more suitable if you want to use procedures of APOC:
https://github.com/neo4j-contrib/neo4j-apoc-procedures

If you want to have simpler ingestion without third party use amp1_graphrag_neo4j mini project!

## Create a virtual environment
python -m venv venv

## Activate the virtual environment
source venv/bin/activate

## Install packages from requirements.txt
pip install -r requirements.txt

## Install Jupyter kernel in the virtual environment
python -m ipykernel install --user --name=venv


## libraries requirements from apoc:
```
cp ragtest/output/*/artifacts/*.parquet $NEO4J_HOME/import

echo 'apoc.import.file.enabled=true' >> $NEO4J_HOME/conf/apoc.conf

cd $NEO4J_HOME/plugins
cp ../labs/*apoc*.jar .
curl -OL https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/5.21.0/apoc-5.21.0-extended.jar
curl -OL https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/5.21.0/apoc-hadoop-dependencies-5.21.0-all.jar
cd ..
bin/neo4j console
*/
```