# mini-project-1
This mini project is about how to read book.txt in input folder, build graph using graphrag out of it and convert this mini graph into parquet using. Then a custom code which convert those into csv. This csv files are then imported and uses inside the neo4j for query and visualization.

step 1: 
```
python -m venv venv
pip install -r requirements.txt
```
step 2: create your own openapi key
```
export GRAPHRAG_API_KEY=''
```
step 3: run this to create graphrag auto create landing yaml and folder structure
```
python -m graphrag.index --init  --root .
```
step 4: after setting all the required yaml file and also copying book.txt, running this will create parquet file of graph based on prompt given in prompts folder
```
python -m graphrag.index --root .
```
step 5: using following commands output of local and global search will be generated. Will explain difference of these type of searches in the other mini project series.
```
python -m graphrag.query --root . --method global "What are the top themes in this story?"             
python -m graphrag.query --root . --method local "Who is Scrooge, and what are his main relationships?"
```
step 6: if you want to visualize or query using neo4j, you need to install neo4j community edition. After installation, you need to import those csv files into neo4j.
```
brew install openjdk@17
echo 'export JAVA_HOME=$(/usr/libexec/java_home -v 17)' >> ~/.zshrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.zshrc
source ~/.zshrc
```
```
cd ~/Documents
curl -O https://dist.neo4j.org/neo4j-community-5.21.2-unix.tar.gz
tar -xf neo4j-community-5.21.2-unix.tar.gz
cd neo4j-community-5.21.2
./bin/neo4j start
./bin/neo4j status
```

```
http://localhost:7474/browser/
```

step 7: enjoy!