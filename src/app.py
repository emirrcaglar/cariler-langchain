from src.agent import agent_executor
from src.utils import count_tokens

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
    chat_history.append(result["output"])

    print("App: Agent invoke end...")
    print("App: Agent output:")
    print(result["output"])

    token_count, history = count_tokens(chat_history + [query])
    print(f"\n\nApproximate tokens in chat: {token_count}")  

    print(f"\n\nChat history: {history}")
