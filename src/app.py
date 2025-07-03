from langchain.callbacks import get_openai_callback

from src.agent import agent_executor

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

    print("App: Agent invoke start...")
    result = agent_executor.invoke({
        "input": query,
        "chat_history": chat_history,
    })
    print("App: Agent invoke end...")
    print("App: Agent output:")
    print(result["output"])