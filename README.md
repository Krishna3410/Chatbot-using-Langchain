# Course Query Bot

A conversational chatbot built using Langchain, Flask, and TensorFlow. This application allows users to query a collection of technical courses extracted from [Brainlox](https://brainlox.com/courses/category/technical) and receive relevant information.

## Features

- **Data Extraction**: Automatically extracts course data from the Brainlox website.
- **Embeddings**: Creates embeddings for the extracted course data to enable effective querying.
- **Flask RESTful API**: Serves as the backend to handle user queries and return relevant course information.
- **Interactive Web Interface**: A user-friendly interface built with HTML and Bootstrap for easy interaction with the chatbot.

## Technologies Used

- **Python**: The main programming language used for development.
- **Flask**: A lightweight WSGI web application framework for building the RESTful API.
- **Langchain**: A framework for developing applications powered by language models.
- **TensorFlow**: For creating embeddings from the course data.
- **BeautifulSoup**: For web scraping to extract course data from the Brainlox website.
- **Bootstrap**: A CSS framework for creating responsive web interfaces.
