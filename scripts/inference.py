from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.prompts import ChatPromptTemplate
from openai import OpenAI

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the user's question based on the below context:{context}
This is the question:{question}
"""

def init_db(model_name):
    embedding_function = HuggingFaceInstructEmbeddings(model_name=model_name)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    return db

client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
# client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def generate_response(query, db, use_embedding=False):
    if use_embedding:
        results = db.similarity_search_with_relevance_scores(query, k=4)
        context_text = " ".join([doc.page_content for doc, _score in results])
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(context=context_text, question=query)
    else:
        prompt = query

    response = client.chat.completions.create(
        model="mistral",
        messages=[{"role": "user", "content": str(prompt)}],
        temperature=0.7,
    )
    
    return response.choices[0].message.content
