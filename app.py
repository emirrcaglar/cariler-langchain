from dotenv import load_dotenv
from langchain.schema import HumanMessage, AIMessage
from my_tools import (
    set_dataframe, set_vectorstore, 
    get_column_names, get_head, get_info, similarity_search
)
from token_count import count_tokens
from vector_store import get_vectorstore
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

# --- Data and Tool Setup ---
file_path = "data/cari_hesap_hareketleri.csv"

# 1. Initialize Vector Store
embeddings = OpenAIEmbeddings()
vectorstore = get_vectorstore(file_path, embeddings)
set_vectorstore(vectorstore)

# 2. Initialize DataFrame
df = pd.read_csv(file_path)
set_dataframe(df)

# 3. Initialize LLM and Tools
llm = ChatOpenAI(model="gpt-4o-mini")
tools = [get_column_names, get_head, get_info, similarity_search]

# --- Agent Setup ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. You have two types of tools:\n1. Pandas tools (get_column_names, get_head, get_info) for inspecting a DataFrame.\n2. A vector search tool (similarity_search) for finding relevant information in a vector store.\nDecide which tool is best to answer the user's question."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- Main Application Loop ---
chat_history = []
while True:
    query = input(">>> ")
    
    if query.lower() == 'q':
        break
    
    if query.lower() == 't':
        total_tokens = 0
        for message in chat_history:
            total_tokens += count_tokens(message.content)
        print(f"Total tokens in chat history: {total_tokens}")
        continue

    if query.lower() == 'h':
        for message in chat_history:
            print(message.content)
        continue

    response = agent_executor.invoke({"input": query, "chat_history": chat_history})
    print(response["output"])

    chat_history.extend([
        HumanMessage(content=query),
        AIMessage(content=response["output"])
    ])