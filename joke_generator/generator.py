from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class JokeState(TypedDict):
    topic: str
    keypoints: str
    joke: str
    openai_api_key: str  # Ensure API key is always present in state

def create_keypoints(state: JokeState) -> JokeState:
    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        openai_api_key=state["openai_api_key"]
    )
    state["keypoints"] = model.invoke(
        f"Generate 3 to 5 key points for a joke about '{state['topic']}'. Make them creative, concise, and relevant to the topic."
    ).content
    return state

def create_joke(state: JokeState) -> JokeState:
    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        openai_api_key=state["openai_api_key"]
    )
    state["joke"] = model.invoke(
        f"Write a short, original joke (max 60 words) about '{state['topic']}'. Incorporate these key points: {state['keypoints']}. Make it witty and without hurting anyone's feelings."
    ).content
    return state

graph = StateGraph(JokeState)
graph.add_node("create_keypoints", create_keypoints)
graph.add_node("create_joke", create_joke)

graph.add_edge(START, "create_keypoints")
graph.add_edge("create_keypoints", "create_joke")
graph.add_edge("create_joke", END)

JokeWorkflow = graph.compile()

def run_joke_workflow(topic: str, openai_api_key: str) -> JokeState:
    return JokeWorkflow.invoke({"topic": topic, "openai_api_key": openai_api_key})
