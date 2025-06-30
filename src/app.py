from workflow import workflow

chain = workflow.compile()

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

    result = chain.invoke({
        "input": query,
        "chat_history": chat_history,
        "agent_outcome": None,
        "intermediate_steps": []
    })
