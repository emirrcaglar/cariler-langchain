from dotenv import load_dotenv
from langchain.schema import HumanMessage, AIMessage
from my_tools import (
    set_dataframe, set_vectorstore, 
    get_column_names, get_head, get_info, similarity_search,
    describe_column, filter_data, get_value_counts, math_operation,
    group_by, apply_aggregation, select_columns
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
tools = [
    get_column_names, get_head, get_info, similarity_search,
    describe_column, filter_data, get_value_counts, math_operation,
    group_by, apply_aggregation, select_columns
    ]

# --- Agent Setup ---
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant. You have two types of tools:\n
     1. Pandas tools (select_columns, get_column_names, get_head, get_info etc.) for inspecting a DataFrame.\n
     2. A vector search tool (similarity_search) for finding relevant information in a vector store.\n
     Decide which tool is best to answer the user's question.
     Turkish is your main output language."""),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- Main Application Loop ---
chat_history = []
total_actual_tokens = 0
while True:
    query = input(">>> ")
    
    if query.lower() == 'q':
        break
    
    if query.lower() == 't':
        total_token_count = 0
        for message in chat_history:
            total_token_count += count_tokens(message.content)
        print(f"Total tokens in chat history: {total_token_count}")
        continue

    if query.lower() == 'h':
        for message in chat_history:
            print(message)
        continue

    response = agent_executor.invoke({"input": query, "chat_history": chat_history})
    print(response["output"])

    chat_history.extend([
        ("human", query),
        ("ai", response["output"])
    ])