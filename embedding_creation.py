from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Your extract_course_data function
from bs4 import BeautifulSoup
from langchain.schema import Document
import requests

def extract_course_data():
    url = "https://brainlox.com/courses/category/technical"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    courses = []
    course_cards = soup.find_all('div', class_='courses-content')
    
    for card in course_cards:
        title_tag = card.find('h3')
        description_tag = card.find('p')
        link_tag = card.find('a', href=True)

        if title_tag and description_tag and link_tag:
            title = title_tag.text.strip()
            description = description_tag.text.strip()
            link = link_tag['href']

            doc = Document(page_content=description, metadata={'title': title, 'url': link})
            courses.append(doc)

    return courses

# Embedding and Vector Store
def create_embeddings(documents):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Combine title and description for embedding
    course_texts = [doc.metadata['title'] + " " + doc.page_content for doc in documents]
    embeddings = model.encode(course_texts)

    return embeddings, course_texts

def store_embeddings(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    # Add embeddings to FAISS index
    index.add(embeddings)

    # Save the index to a file
    faiss.write_index(index, "course_embeddings.index")

    return index

# Main integration
if __name__ == "__main__":
    # Step 1: Extract course data
    extracted_courses = extract_course_data()

    # Step 2: Create embeddings
    embeddings, course_texts = create_embeddings(extracted_courses)

    # Step 3: Store in FAISS vector store
    faiss_index = store_embeddings(np.array(embeddings))

    print("Embeddings and vector store created successfully.")
