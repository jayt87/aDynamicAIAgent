from typing import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
from llm_models import llm5, llm_reasoning04mini
from prompts import *
load_dotenv()

#TODO: prevent infinite loops by checking the number of iterations or messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

config = {"configurable": {"thread_id": "1"}}
memory = MemorySaver()

def worker(state: State) -> dict:  
    prompt = [
        {"role": "system", "content": state["messages"][-1].content},
    ]
    response = llm_reasoning04mini.invoke(prompt)
    return {"messages": [ response ]}

# Supervisor: evaluates progress (no state change needed)
def supervisor(state: State) -> dict:
    prompt = [
        {"role": "system", "content": SUPERVISOR_PROMPT},
    ] + state["messages"]
    response = llm_reasoning04mini.invoke(prompt)
    return {"messages": [ response ]}

# Routing logic: keep looping or end
def route(state: State):
    decision = END if "END WORKER NOW" in state["messages"][-1].content else "worker"
    print(f"Decision made by supervisor: {decision}")
    return decision

# Build graph
builder = StateGraph(State)
builder.add_node("supervisor", supervisor)
builder.add_node("worker", worker)
# supervisor is the entry; it decides to continue to worker or end
builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", route, {"worker": "worker", END: END})
# after worker, go back to supervisor (loop)
builder.add_edge("worker", "supervisor")
graph = builder.compile(checkpointer=memory)

def stream_graph_updates(user_input: str):
    msgs = [ {"role": "user", "content": user_input} ]
    while True:
        for event in graph.stream({"messages": msgs}, config):
            for name, value in event.items():
                print(f"{name.title()}: ", value["messages"][-1].content)
                print("-" * 100)
                    
# Run
stream_graph_updates("azure openai, responses api , file input for base64 pdf payload doesn't seem to be working. The file upload and then analyze functionality seems to be working but base 64 not. Search for GitHub issues, Microsoft documentation and other web results to explain to me what is the current status .")