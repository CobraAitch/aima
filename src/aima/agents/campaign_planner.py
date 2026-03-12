from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_ollama import ChatOllama

class PlannerState(TypedDict):
    goal: str
    plan: str

def generate_plan(state: PlannerState) -> PlannerState:
    llm = ChatOllama(model="llama3.1:8b")
    response = llm.invoke(
        f"You are a marketing strategist. Create a campaign plan for: {state['goal']}. "
        f"Include target audience, channels, key messages, and timeline."
    )
    return {"goal": state["goal"], "plan": response.content}

graph = StateGraph(PlannerState)
graph.add_node("generate_plan", generate_plan)
graph.add_edge(START, "generate_plan")
graph.add_edge("generate_plan", END)

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({"goal": "Launch BMW M3 social media campaign", "plan": ""})
    print(result["plan"])

