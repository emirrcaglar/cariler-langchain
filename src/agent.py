from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.conversation.memory import ConversationBufferMemory

import pandas as pd

from src.vector_store import get_vectorstore
from src.my_tools import DataFrameAggregateTool, DataFrameInspectTool, DataFrameFilterTool, DataFrameAnalysisTool

from dotenv import load_dotenv
load_dotenv()

# --- Data and Tool Setup ---
file_path = "data/cari_hesap_hareketleri.csv"

# 1. Initialize Vector Store
embeddings = OpenAIEmbeddings()
vectorstore = get_vectorstore(file_path, embeddings)
df = pd.read_csv(file_path, encoding="utf-8")

# 3. Initialize LLM and Tools
llm = ChatOpenAI(
    model="o4-mini-2025-04-16",
    max_retries=3
    )

conversational_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# --- Agent Setup ---
prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a data-agent who works on financial data.
    You will work on the data with Pandas. You should first analyze the user prompt, extract parameters
    and use them in a data filter operation using Pandas query (_filter_data() function in DataFrameTransformTool). If that fails, only then you are going to use different tools.
    You have two types of tools:\n
    1. A vector search tool (similarity_search) for finding relevant information in a vector store.\n
    2. Pandas tools for inspecting a DataFrame.\n
    Decide which tool is best to answer the user's question.\n
    In your output, what tools you used, what was your instinct etc.
    Turkish is your main output language.
     """),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])


tools = [
    DataFrameAnalysisTool(df=df, vectorstore=vectorstore),
    DataFrameInspectTool(df=df),
    DataFrameFilterTool(df=df), 
    DataFrameAggregateTool(df=df), # type: ignore
    ]


agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools,
                                verbose=True, memory=conversational_memory)
