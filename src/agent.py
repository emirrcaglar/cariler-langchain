from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.conversation.memory import ConversationBufferMemory

import pandas as pd

from src.Tools.analyze import DataFrameAnalysisTool
from src.Tools.filter import DataFrameFilterTool
from src.Tools.inspect import DataFrameInspectTool
from src.Tools.aggregate import DataFrameAggregateTool
from src.Tools.output import ReportGeneratorTool
from src.Tools.currency import CurrencyTool

from src.vector_store import get_vectorstore
from src.constants import DATA_FILE_PATH, AI_MODEL

from dotenv import load_dotenv
load_dotenv()

# --- Data and Tool Setup ---
file_path = DATA_FILE_PATH

# 1. Initialize Vector Store
embeddings = OpenAIEmbeddings()
vectorstore = get_vectorstore(file_path, embeddings)
df = pd.read_csv(file_path, encoding="utf-8")
print("Agent: DataFrame head after loading CSV:")
print(df.head())

# 3. Initialize LLM and Tools
llm = ChatOpenAI(
    model=AI_MODEL,
    max_retries=3,
    streaming=False,
    )

conversational_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# --- Agent Setup ---
prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a data-agent who works on financial data.
    Generate a comprehensive markdown report summarizing your findings, including a data sample
    and recommendations.
    Use iterative refinement. Start small, build the data after understanding the smaller parts.
    Always inspect unique values before filtering.
    You MUST handle all grouping / filtering operations before doing any conversions, printing, currency ops. etc.
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
    ReportGeneratorTool(df=df),
    CurrencyTool(df=df)
    ]


agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(
                            agent=agent, 
                            tools=tools,
                            verbose=True, 
                            memory=conversational_memory,
                            )
