from typing import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from llm_models import llm5, llm5mini
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
    response = llm5.invoke(prompt)
    return {"messages": [ response ]}

# Supervisor: evaluates progress (no state change needed)
def supervisor(state: State) -> dict:
    prompt = [
        {"role": "system", "content": SUPERVISOR_PROMPT},
    ] + state["messages"]
    response = llm5.invoke(prompt)
    return {"messages": [ response ]}

# Routing logic: keep looping or end
def route(state: State):
    if "PLAN GENERATED" in state["messages"][-1].content or type(state["messages"][-1]) is HumanMessage:
        decision = "supervisor"
    elif "END WORKER NOW" in state["messages"][-1].content:
        decision = END
    elif len(state["messages"]) > 90: #TODO: this is a temporary fix to prevent infinite loops, must be done in the graph.
        decision = END
    else:
        decision = "worker"
    return decision

# Build graph
builder = StateGraph(State)
builder.add_node("supervisor", supervisor)
builder.add_node("worker", worker)
# supervisor is the entry; it decides to continue to worker or end
builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", route, {"supervisor": "supervisor", "worker": "worker", END: END})
# after worker, go back to supervisor (loop)
builder.add_edge("worker", "supervisor")
graph = builder.compile(checkpointer=memory)

def stream_graph_updates(user_input: str):
    msgs = [ {"role": "user", "content": user_input} ]
    for event in graph.stream({"messages": msgs}, config):
        for name, value in event.items():
            print(f"Node name: {name.title()}: ", value["messages"][-1].content)
            print("-" * 100)                    
# Run
stream_graph_updates("in azure openai, responses api , file input for base64 pdf payload doesn't seem to be working. The file upload and then analyze functionality seems to be working but base 64 not. What is the current status of this issue?.")