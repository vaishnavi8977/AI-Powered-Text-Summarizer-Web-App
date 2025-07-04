# project: AI-Powered-Text-Summarizer-Web-App
Author: VAISHNAVI DADE  
DATE: 07/03/2024  
Install libraries: langchain, llama-index, transformers, fastapi, uvicorn, streamlit (pip install)   

pip install langchain  
pip install llama-index  
pip install "fastapi[all]"  
pip install "transformers[torch]"  

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

