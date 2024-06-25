import fitz  # PyMuPDF
import openai
import numpy as np
import faiss
from openai import OpenAI

from setopenai import setupopenai
setupopenai()

client = OpenAI()

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def split_text(text, max_tokens=2048):
    # Split text into chunks with a maximum number of tokens
    tokens = text.split()
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunks.append(" ".join(tokens[i:i + max_tokens]))
    return chunks

def get_embeddings(text):
    response = client.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding

pdf_path = "books/joe-celkos-sql-puzzles-and-answers-0123735963_compress.pdf"
book_text = extract_text_from_pdf(pdf_path)

# Split the book text into smaller chunks
sections = book_text.split("\n\n")  # Split by double newlines for example
sections = [chunk for section in sections for chunk in split_text(section)]

embeddings = [get_embeddings(section) for section in sections]

embeddings_array = np.array(embeddings).astype('float32')

index = faiss.IndexFlatL2(embeddings_array.shape[1])
index.add(embeddings_array)

def retrieve_relevant_text(query_embedding, index, texts, k=5):
    distances, indices = index.search(np.array([query_embedding]).astype('float32'), k)
    return [texts[i] for i in indices[0]]

system_prompt = """
You are an AI SQL tutor specialized in guiding users through SQL problems. 
For each problem, provide hints up to 4 attempts. If there are multiple solutions, 
ask the user if they would like to explore another solution and provide hints for that as well. 
If the user finds it hard, offer more hints and detailed explanations.
"""

def generate_response(system_prompt, context):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context}
        ]
    )
    return response.choices[0].message.content

def interactive_sql_tutor():
    # Retrieve a random problem from the sections
    import random
    initial_question = random.choice(sections)
    
    user_attempts = 0
    max_attempts = 4
    
    print(f"Tutor: Let's start with a SQL puzzle. Here is your first problem: {initial_question}")
    
    while True:
        user_input = input("User: ")
        user_embedding = get_embeddings(user_input)
        relevant_texts = retrieve_relevant_text(user_embedding, index, sections)
        
        if user_attempts < max_attempts:
            hint_context = (
                f"Hint attempt {user_attempts + 1}:\n{user_input}\n\n"
                f"Relevant Information:\n{''.join(relevant_texts)}"
            )
            response = generate_response(system_prompt, hint_context)
            print(f"Tutor: {response}")
            user_attempts += 1
        else:
            detailed_explanation = (
                f"Let's go over this problem in detail. Here is an explanation:\n{''.join(relevant_texts)}"
            )
            response = generate_response(system_prompt, detailed_explanation)
            print(f"Tutor: {response}")
            user_attempts = 0  # Reset attempts for the next question

interactive_sql_tutor()
