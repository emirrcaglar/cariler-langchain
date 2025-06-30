from dotenv import load_dotenv
import pandas as pd

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.conversation.memory import ConversationBufferMemory

from vector_store import get_vectorstore
from my_tools import DataFrameAggregateTool, DataFrameInspectTool, DataFrameTransformTool, DataFrameAnalysisTool
load_dotenv()

# --- Data and Tool Setup ---
file_path = "data/cari_hesap_hareketleri.csv"

# 1. Initialize Vector Store
embeddings = OpenAIEmbeddings()
vectorstore = get_vectorstore(file_path, embeddings)
df = pd.read_csv(file_path)
df.columns = [col.upper().strip() for col in df.columns]



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
    ("system", """You are a helpful assistant. You work on financial data.
     You have two types of tools:\n
     1. Pandas tools (select_columns, get_column_names, group_by, get_head etc.) for inspecting a DataFrame.\n
     2. A vector search tool (similarity_search) for finding relevant information in a vector store.\n
     Decide which tool is best to answer the user's question.
     Always use uppercase column names when referring to DataFrame columns.
     Always use backtiks (`) around column names in queries.
     Turkish is your main output language."""),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

tools = [
    DataFrameTransformTool(df=df), 
    DataFrameAggregateTool(df=df), # type: ignore
    DataFrameInspectTool(df=df),
    DataFrameAnalysisTool(df=df, vectorstore=vectorstore)
    ]

agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools,
                                verbose=True, memory=conversational_memory)

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