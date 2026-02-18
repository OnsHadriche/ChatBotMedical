from src.helper import download_embeddings
from langchain_pinecone import Pinecone
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.prompt import system_prompt
from store_index import docsearch


def rag_chatbot( input : str, k : int)->str :
    #Initialize LLM
    chatModel = ChatGroq(model="openai/gpt-oss-120b")
    #Define prompt 
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
    )
    #Define retriver 
    retriver = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": k}
    )
    
    question_answer_chain = create_stuff_documents_chain(
    llm=chatModel,
    prompt=prompt,)

    rag_chain = create_retrieval_chain(
        retriver,
        question_answer_chain,
    )
    response = rag_chain.invoke({"input":input})
    return str(response["answer"])
