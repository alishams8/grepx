
```
python -m venv venv
pip install -r requirements.txt
```

```
export GRAPHRAG_API_KEY=''
```

```
python -m graphrag.index --init  --root .
```

```
python -m graphrag.index --root .
```

```
python -m graphrag.query --root . --method global "What are the top themes in this story?"             
python -m graphrag.query --root . --method local "Who is Scrooge, and what are his main relationships?"
```

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