# project: AI-Powered-Text-Summarizer-Web-App
Author: VAISHNAVI DADE  
DATE: 07/03/2024  
Install libraries: langchain, llama-index, transformers, fastapi, uvicorn, streamlit (pip install)   

pip install langchain  
pip install llama-index  
pip install "fastapi[all]"  
pip install "transformers[torch]"  
pip install -U langchain-community
pip install openai langchain


create virtual env
python -m venv venv
venv\Scripts\activate
pip install -r requirement.txt

pip install -U "huggingface_hub[cli]"
login to huggingface cli using token command is here 
huggingface-cli login


Run model on GPU : install https://developer.nvidia.com/cuda-toolkit


to run the app http://127.0.0.1:8000/

URL to check app is working local 
http://127.0.0.1:8000/

Swagger UI
http://127.0.0.1:8000/docs 


Step1:
Using FastAPi set the POST request /summarize and import .env
verify POST request by passing sample Json
http://127.0.0.1:8000/summarize
request:
{
  "text": "Hello Framework",
  "model": "LangChain"
}

response: 
{
  "summary": "Placeholder summary for text: Hello how are you using model: LangChain"
}

# Challenge1 Model Selection :
Originally used Hugging Face models like flan-t5 and bart-large-cnn. These models are large and require GPU for efficient execution.

Project environment is CPU-only; GPU not available. Hugging Face models were slow or failed in CPU-only setup.

Switched to OpenAI’s gpt-4o model (API-based).

gpt-4o runs via cloud — no local model download or GPU needed. Provides fast, high-quality, instruction-following output. Produces clean structured JSON, useful with LangChain parsing. More reliable than small Hugging Face models for blog generation.

Cost-effective for students (approx. $0.0003–0.0009 per 1K tokens). Ideal for lightweight, scalable, and low-cost deployments.


# Challenge 2 Validating User Input 
The project requires the user to input a string user need type his ideas to create structured and meaningfull vlog.
The input is used to generate a structured and meaningful blog post via AI.
Invalid input like numbers, lists, or non-string types can break the generation or result in poor output.
To handle this, we use Pydantic for strict input validation.

Pydantic ensures that:
Only valid string inputs are accepted.
Any invalid input (like integers or empty values) raises a clear error.
This protects the AI chain from processing faulty data.
Adds robustness to the API and improves the overall user experience.
Makes the application more reliable and production-ready. 



# FastAPI Notes
- Routing: `@app.get`, `@app.post` define endpoints.
- Async: `async def` for non-blocking operations.
- Pydantic: `BaseModel` validates JSON input/output.
- Swagger UI: Auto-generated at `/docs`.

# Challenge 3: Input Length Validation & Error Handling
The user must provide blog input text between 5 to 300 words.

This ensures the content is meaningful for blog generation while preventing overly short or long inputs.

Validation is handled using a Pydantic model in the API layer.

If the input does not meet the length requirement, the API:

Rejects the request

Returns a custom error message explaining the issue

This prevents unnecessary model invocation and improves UX.

Makes the system more resilient, controlled, and user-friendly.

Easy to test by:

Sending short inputs (e.g., "Hi" → should fail)

Sending overly long content (>300 words → should fail)

Sending valid input within range → should succeed
{
    "detail": [
        {
            "type": "value_error",
            "loc": [
                "body",
                "content"
            ],
            "msg": "Value error, Idea must have at least 5 words.",
            "input": "string",
            "ctx": {
                "error": {}
            }
        }
    ]
}