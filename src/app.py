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

    result = agent_executor.invoke({
        "input": query,
        "chat_history": chat_history,
    })

    print(result["output"])
