from flask import Flask, request, jsonify
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize Flask app
app = Flask(__name__)

# Load pre-trained FAISS index and SentenceTransformer model
index = faiss.read_index("course_embeddings.index")  # Load the FAISS index you saved earlier
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Load the original course data from data_extraction.py
from data_extraction import extract_course_data  # Updated to match your file name
extracted_courses = extract_course_data()  # Use the course data you extracted earlier

@app.route('/query', methods=['POST'])
def query():
    # Extract query from the POST request
    data = request.json
    query_text = data.get('query', '')

    if not query_text:
        return jsonify({"error": "No query provided"}), 400

    # Step 1: Create an embedding for the query
    query_embedding = model.encode([query_text])

    # Step 2: Search FAISS index for the most similar courses
    distances, indices = index.search(np.array(query_embedding), k=5)  # Find the top 5 closest courses

    # Step 3: Retrieve and format the results
    results = []
    for idx in indices[0]:
        course = extracted_courses[idx]
        results.append({
            "title": course.metadata['title'],
            "description": course.page_content,
            "url": course.metadata['url']
        })

    return jsonify(results)

# Add a home route for the root URL
@app.route('/')
def home():
    return "Welcome to the Course Query API. Please use the /query endpoint."

# Add a custom handler for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "This route is not available. Use the /query endpoint."}), 404

if __name__ == '__main__':
    app.run(debug=True)
