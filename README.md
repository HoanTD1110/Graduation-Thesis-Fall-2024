# AI-chatbot

anaconda, python=3.9.15


# Create environment
```
conda create -n chatbot python=3.9
conda activate chatbot
pip install -r requirements.txt
```

# Create database (run only one time)
Insert using default embedding
```
python src/insert_data/default_insert.py
```

Insert using OpenAI embedding
```
python src/insert_data/openai_insert.py
```
# Run
```
flask --app main run
```
