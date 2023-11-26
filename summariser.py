import openai
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

def summarise (chunk):
    
    load_dotenv()

    openai.api_base = os.getenv("OPENAI_API_BASE")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    api_key = openai.api_key 
    docs = [Document(page_content=chunk)]
    prompt_template="""
        You are a world best summariser. Concisely summarise the text below into bullet points, capturing essential points and core ideas. Include relevant examples, omit excess details, and ensure the summary's length matches the original's complexity:
    
        {text}
    """
    PROMPT = PromptTemplate(template = prompt_template,input_variables = ["text"])
    llm=ChatOpenAI(openai_api_base=openai.api_base,openai_api_key=api_key, temperature=0,model_name="gpt-3.5-turbo-1106", max_tokens=15000)
    chain = load_summarize_chain(llm, chain_type="stuff",prompt=PROMPT)
    summary = chain.run (docs)
    
    return summary