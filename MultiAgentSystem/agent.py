from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

class AgentState(TypedDict):
    topic: str
    research_data: List[str]
    blog_post: str
    
def researcher_node(state: AgentState):
    topic = state['topic']
    print(f"Researcher is looking up: {topic}...")
    
    search = DuckDuckGoSearchRun()
    
    try:
        results = search.run(f"key facts and latest news about {topic}")
    except Exception as e:
        results = f"Could not find data: {e}"
        
    print("Research complete")
    
    return {"research_data": state.get("research_data",[])+[results]}

def writer_node(state: AgentState):
    print("Writer is drafting the post...")
    
    topic = state["topic"]
    data = state["research_data"][-1] if state["research_data"] else ""
    llm = ChatOllama(model="llama3", temperature=0.7)
    
    prompt = ChatPromptTemplate.from_template(
        """You are a tech blog writer.
        Write a short, engaging blgo post about "{topic}"
        based ONLY on the following research data: {data}
        Return just the blog post content."""
    )
    
    chain = prompt | llm
    response = chain.invoke({"topic": topic, "data": data})
    print("Writing complete")
    return {"blog_post": response.content}

workflow = StateGraph(AgentState)

workflow.add_node("Researcher", researcher_node)
workflow.add_node("Writer", writer_node)

workflow.set_entry_point("Researcher")
workflow.add_edge("Researcher","Writer")
workflow.add_edge("Writer",END)

app = workflow.compile()