
# ThoughtCraft: AI-Powered Text Summarizer Web App

**Author**: Vaishnavi Dade  
**Date**: July 3, 2024  

## 📘 Overview

**ThoughtCraft** is a web application that transforms unstructured thoughts into clean, well-formatted blog posts using AI. Built with **FastAPI**, **LangChain**, **Jinja2 templates**, and a **MongoDB backend**, it enables users to input raw text, which is summarized, structured, and stored in a database for seamless access.

## ✨ Features

- **Text Summarization**: Converts raw user input into concise, structured blog posts using AI models (e.g., GPT-4o).
- **Input Validation**: Ensures meaningful input (5–300 words) using Pydantic for robust error handling.
- **Asynchronous Backend**: Utilizes FastAPI and `motor` for non-blocking operations and efficient database interactions.
- **Dynamic Rendering**: Displays input forms and generated blog posts on the same page using Jinja2 templates.
- **MongoDB Storage**: Saves generated blog posts in a MongoDB database for persistence.
- **API Documentation**: Auto-generated Swagger UI at `/docs` for easy API exploration.

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- MongoDB (running locally on `mongodb://localhost:27017`)
- Optional: NVIDIA CUDA Toolkit for GPU support (if using Hugging Face models)

### Step 1: Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies
Install the required Python packages:
```bash
pip install langchain llama-index "fastapi[all]" "transformers[torch]" langchain-community openai motor uvicorn
pip install -U "huggingface_hub[cli]"
```

Save dependencies to a `requirements.txt` file:
```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```

### Step 3: Hugging Face CLI Login
For Hugging Face model access, log in using your Hugging Face token:
```bash
huggingface-cli login
```

### Step 4: MongoDB Setup
- Ensure MongoDB is running locally.
- **Database Name**: `blog`
- **Collection Name**: `posts`
- **Default URI**: `mongodb://localhost:27017`

## 🚀 Running the App

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
2. Access the app at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
3. Explore API documentation at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 📝 Usage

### API Endpoints

#### 1. Summarize Text
- **URL**: `/summarize`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "text": "Hello Framework",
    "model": "LangChain"
  }
  ```
- **Response**:
  ```json
  {
    "summary": "Placeholder summary for text: Hello how are you using model: LangChain"
  }
  ```

#### 2. Blog Generation
- **URL**: `/submit_thought`
- **Method**: POST
- **Input**: Form data with a `thought` field (5–300 words).
- **Process**:
  - Validates input length using Pydantic’s `field_validator`.
  - Processes input through the GPT-4o model.
  - Renders the generated blog post on the same page using Jinja2.
  - Saves the result in MongoDB.

#### Example Input
- **Thought**: "The golden hour casts a warm glow over the hills, inspiring thoughts of peace and reflection."
- **Rendered Blog Output**:
  ```markdown
  **Title**: The Magic of Golden Hour Reflections  
  **Tags**: #Poetry, #Sunset, #EveningThoughts  
  **Post**: A beautifully written blog post based on your input.
  ```

### Templates
- **create_post.html**: Displays a form for submitting thoughts and renders the generated blog post below it.

## 🛠️ Development Notes

- **Backend**: Fully asynchronous using `async/await` for non-blocking operations.
- **Error Handling**:
  - Model errors (e.g., API failures).
  - Validation errors (e.g., invalid input length).
  - Database write failures.
- **FastAPI Features**:
  - Routing with `@app.get` and `@app.post`.
  - Pydantic `BaseModel` for JSON input/output validation.
  - Auto-generated Swagger UI at `/docs`.

## ⚙️ Challenges and Solutions

### Challenge 1: Model Selection
- **Issue**: Initially used Hugging Face models (e.g., `flan-t5`, `bart-large-cnn`), which were slow or failed in CPU-only environments due to their size and resource demands.
- **Solution**: Switched to OpenAI’s GPT-4o model (cloud-based):
  - No local model download or GPU required.
  - Fast, high-quality, instruction-following output.
  - Produces structured JSON, compatible with LangChain parsing.
  - Cost-effective (~$0.0003–0.0009 per 1K tokens).

### Challenge 2: Validating User Input
- **Issue**: Invalid inputs (e.g., numbers, lists, or non-strings) could break blog generation or produce poor output.
- **Solution**: Implemented Pydantic for strict input validation:
  - Ensures only valid string inputs are accepted.
  - Raises clear errors for invalid inputs (e.g., integers, empty values).
  - Enhances API robustness and user experience.

### Challenge 3: Input Length Validation & Error Handling
- **Issue**: Blog input text must be 5–300 words to ensure meaningful content without overloading the system.
- **Solution**:
  - Used Pydantic to validate input length in the API layer.
  - Rejects invalid requests with custom error messages:
    ```json
    {
      "detail": [
        {
          "type": "value_error",
          "loc": ["body", "content"],
          "msg": "Value error, Idea must have at least 5 words.",
          "input": "string",
          "ctx": {"error": {}}
        }
      ]
    }
    ```
  - Testing:
    - Short input (e.g., "Hi") → Fails.
    - Overly long input (>300 words) → Fails.
    - Valid input → Succeeds.

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

Please ensure your code follows the project’s style guidelines and includes tests where applicable.

## 📬 Feedback

Feel free to fork this repository or reach out with suggestions to extend the project. For issues or feature requests, open an issue on the repository.

