from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from transformers import pipeline
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

async def createblog_post(text):
    load_dotenv()  # Load API key from .env if using
    # Define response schema
    response_schema = [
        ResponseSchema(
            name="blog_title",
            description="SEO-friendly title of the blog post, must not exceed 150 characters."
        ),
        ResponseSchema(
            name="post_content",
            description="Don't include blog title again"
        ),
        ResponseSchema(
            name="tags",
            description="List the relevant tags for the post"
        ),
    ]

    # Output parser
    output_parser = StructuredOutputParser.from_response_schemas(response_schema)
    format_instructions = output_parser.get_format_instructions()

    # Prompt
    template = PromptTemplate(
        input_variables=["userText"],
        template="""
    You are a creative blog writer. Given the passage below, write a blog post and return a JSON with:
    - "blog_title": an SEO-friendly title
    - "post_content": the main content (do not repeat title)
    - "tags": list of 3-5 relevant hashtags

    Format your response *exactly* like this:

    {format_instructions}

    Passage:
    {userText}
    """.strip(),
        partial_variables={"format_instructions": format_instructions}
    )

    # GPT-4o Mini via OpenAI
    llm = ChatOpenAI(
        model="gpt-4o",  # OpenAI routes mini model under the hood
        temperature=0.7,
        max_tokens=1000
    )

    # Full Chain
    chain = template | llm | output_parser
    print("hello ---->")
    # Invoke chain
    try:
        result = chain.invoke({
            "userText": text
        })
        print("hello ----> 12345")
        print("Blog Title:", result["blog_title"])
        print("Blog Content:", result["post_content"])
        print("Tags:", result["tags"])
    except Exception as e:
        print("Error:", str(e))
    return result