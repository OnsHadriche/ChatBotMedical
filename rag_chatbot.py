from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.prompt import system_prompt
from store_index import docsearch

# ==========================================
# Memory
# ==========================================
memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="input",
    output_key="answer",
    return_messages=True
)

# ==========================================
# LLM
# ==========================================
chatModel = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3,
    max_tokens=1024
)

# ==========================================
# Prompt — order matters!
# ==========================================
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),          # must have {context}
    MessagesPlaceholder(variable_name="chat_history"),  # history before human
    ("human", "{input}"),
])

# ==========================================
# Chains
# ==========================================
question_answer_chain = create_stuff_documents_chain(
    llm=chatModel,
    prompt=prompt,
)

retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}              # ✅ retrieve more chunks
)

rag_chain = create_retrieval_chain(
    retriever,
    question_answer_chain,
)

# ==========================================
# Chat Function
# ==========================================
def rag_chat_medical(input_text: str) -> str:
    # Load memory
    memory_vars = memory.load_memory_variables({})
    chat_history = memory_vars.get("chat_history", [])

    # Debug: print retrieved docs to terminal
    docs = retriever.get_relevant_documents(input_text)
    print(f"\n🔍 Query: {input_text}")
    print(f"📄 Retrieved {len(docs)} chunks:")
    for i, doc in enumerate(docs):
        print(f"  [{i+1}] {doc.page_content[:150]}...")

    # Invoke RAG chain
    response = rag_chain.invoke({
        "input": input_text,
        "chat_history": chat_history
    })

    answer = response.get("answer", "I could not find an answer.")

    # Save to memory
    memory.save_context(
        {"input": input_text},
        {"answer": answer}
    )

    print(f"✅ Answer: {answer[:200]}...")
    return str(answer)