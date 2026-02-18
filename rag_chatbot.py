from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.prompt import system_prompt
from store_index import docsearch

# Persistent short-term memory for the session


memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="input",
    output_key="answer",
    return_messages=True
)
# Initialize LLM and prompt once (no need to recreate each time)
chatModel = ChatGroq(model="openai/gpt-oss-120b")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="chat_history")
    ]
)

# Document QA chain
question_answer_chain = create_stuff_documents_chain(
    llm=chatModel,
    prompt=prompt,
)

# RAG chain with memory
retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}  # you can adjust k per use
)
rag_chain = create_retrieval_chain(
    retriever,
    question_answer_chain,
)

def rag_chat_medical(input: str) -> str:
    """
    Chatbot function with short-term memory.
    The chatbot remembers previous inputs within the same session.
    """
    #load memory
    memory_variables = memory.load_memory_variables({})
    #Invoke Rag
    response = rag_chain.invoke({"input": input,"chat_history": memory_variables["chat_history"]})
    #Get response of llm
    answer = response["answer"]
    #Save memory
    memory.save_context(
        {"input":input},
        {"answer": answer}
    )
    return str(answer)
