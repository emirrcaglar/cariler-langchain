from dotenv import load_dotenv
import pandas as pd

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.conversation.memory import ConversationBufferMemory

from vector_store import get_vectorstore
from my_tools import DataFrameAggregateTool, DataFrameInspectTool, DataFrameTransformTool
load_dotenv()

# --- Data and Tool Setup ---
file_path = "data/cari_hesap_hareketleri.csv"

# 1. Initialize Vector Store
embeddings = OpenAIEmbeddings()
vectorstore = get_vectorstore(file_path, embeddings)
df = pd.read_csv(file_path)



# 3. Initialize LLM and Tools
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
    )

conversational_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

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

tools = [
    DataFrameTransformTool(df=df), 
    DataFrameAggregateTool(df=df), 
    DataFrameInspectTool(df=df)
    ]

# from langchain.agents import initialize_agent

# agent = initialize_agent(
#     agent='chat-conversational-react-description',    
#     tools=tools,
#     llm=llm,
#     verbose=True,
#     max_iterations=3,
#     early_stopping_method='generate',
#     memory=conversational_memory
# )

# agent("Tedarikcilerin toplam bakiyelerini hesapla")


agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- Main Application Loop ---
chat_history = []
while True:
    query = input(">>> ")
    
    if query.lower() == 'q':
        break

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