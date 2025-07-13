
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

## 🔑 Setting Up OpenAI API

The project uses OpenAI's GPT-4o model for blog generation, which requires an API key. Follow these steps to set up the OpenAI API:

1. **Create an OpenAI Account**:
   - Visit [https://platform.openai.com/signup](https://platform.openai.com/signup).
   - Sign up with your email or log in if you already have an account.

2. **Obtain an OpenAI API Key**:
   - Navigate to the [API Keys](https://platform.openai.com/api-keys) section in your OpenAI dashboard.
   - Click "Create API Key" and copy the generated key.
   - **Important**: Store the key securely, as it cannot be retrieved later.

3. **Configure the API Key**:
   - Create a `.env` file in the project root directory.
   - Add the following line to the `.env` file, replacing `your_openai_api_key` with your actual key:
     ```bash
     OPENAI_API_KEY=your_openai_api_key
     ```
   - The project uses the `python-dotenv` library to load the API key. The `load_dotenv()` function in the code automatically reads the `.env` file:
     ```python
     from dotenv import load_dotenv
     load_dotenv()  # Loads OPENAI_API_KEY from .env
     ```

4. **Verify Integration**:
   - The OpenAI API key is used by the `ChatOpenAI` model in the blog generation function:
     ```python
     from langchain_community.chat_models import ChatOpenAI
     llm = ChatOpenAI(
         model="gpt-4o",
         temperature=0.7,
         max_tokens=1000
     )
     ```
   - Ensure the `.env` file is in the project root and not committed to version control (e.g., add `.env` to `.gitignore`).



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
- **Issue**: Initially, Hugging Face models like `flan-t5` and `bart-large-cnn` were used for text summarization and blog generation. These models were unsuitable for the project due to:
  - **CPU Limitations**: Hugging Face models are large (4–12 GB of RAM) and computationally intensive, leading to slow inference (minutes per request) or crashes on CPU-only systems. The project environment lacked GPU support, making these models impractical.
  - **NVIDIA GPU Issues**: An attempt to use an NVIDIA GPU with the CUDA Toolkit was made, but it failed due to system-specific compatibility issues, such as unsupported GPU architecture, driver mismatches, or insufficient CUDA memory.
  - **Model Size and Latency**: Even with GPU support, Hugging Face models required local model downloads and significant memory, increasing deployment complexity.
- **Solution**: Switched to OpenAI’s GPT-4o model (cloud-based), integrated via the `ChatOpenAI` class in LangChain:
  ```python
  from langchain_community.chat_models import ChatOpenAI
  llm = ChatOpenAI(
      model="gpt-4o",
      temperature=0.7,
      max_tokens=1000
  )
  ```
  - **Benefits**:
    - **No Local Compute Required**: GPT-4o runs on OpenAI’s cloud, eliminating the need for local GPU or high-memory CPU.
    - **Fast Inference**: Provides near-instantaneous responses, even for complex blog generation tasks.
    - **High-Quality Output**: Delivers instruction-following, structured JSON output compatible with LangChain’s `StructuredOutputParser` for reliable parsing.
    - **Cost-Effective**: Affordable for students (~$0.0003–0.0009 per 1K tokens), ideal for lightweight, scalable deployments.
    - **Ease of Integration**: Requires only an API key, loaded via `dotenv`, simplifying setup compared to managing local model weights.

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

