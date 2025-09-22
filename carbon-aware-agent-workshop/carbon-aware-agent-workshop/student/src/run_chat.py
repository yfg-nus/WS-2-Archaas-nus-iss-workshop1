
from typing import List, Any, Dict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from config import OPENAI_MODEL, USE_LLM
from tools_agent import (
    get_profile_tool, list_regions_tool, update_prefs_tool,
    parse_time_tool, get_region_forecast_tool, best_slot_in_window_tool, recommend_best_tool
)

SYSTEM = (
    "You are a single-agent carbon-aware scheduler.\n"
    "- Goal: recommend the best (region, start time) around the user's desired time within allowed shift.\n"
    "- If the start time isn't specified, ask for it and accept natural language times (e.g., 'tomorrow 10am').\n"
    "- Use tools to parse time, read/update preferences, inspect forecasts, and recommend.\n"
    "- When the user expresses preference changes (e.g., 'I prefer regions SG, EU_WEST' or 'remember shift 90 minutes'),\n"
    "  call update_prefs to persist them.\n"
    "- Keep responses concise; when recommending, include region, ISO time, intensity, and shift minutes."
)

# Prepare LLM bound with tools
TOOLS = [
    get_profile_tool, list_regions_tool, update_prefs_tool,
    parse_time_tool, get_region_forecast_tool, best_slot_in_window_tool, recommend_best_tool
]

def build_app():
    if not USE_LLM:
        raise SystemExit("OPENAI_API_KEY missing. Add it to .env to run the chat agent.")
    llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0).bind_tools(TOOLS)

    graph = StateGraph(MessagesState)

    def assistant(state: MessagesState):
        # Ensure a single system message anchors behavior
        msgs = state["messages"]
        if not msgs or not isinstance(msgs[0], SystemMessage):
            msgs = [SystemMessage(content=SYSTEM)] + msgs
        resp = llm.invoke(msgs)
        return {"messages": [resp]}

    tool_node = ToolNode(TOOLS)

    graph.add_node("assistant", assistant)
    graph.add_node("tools", tool_node)

    graph.set_entry_point("assistant")
    graph.add_conditional_edges("assistant", tools_condition)  # -> "tools" when tool_calls present, else END
    graph.add_edge("tools", "assistant")
    graph.add_edge("assistant", END)

    return graph.compile()

def chat():
    app = build_app()
    print("Agent ready. Try: 'I want to schedule a job', 'tomorrow 10am', 'I prefer regions SG, EU_WEST', 'remember allowed shift 90 minutes'.")
    state: Dict[str, Any] = {"messages": [SystemMessage(content=SYSTEM)]}
    while True:
        try:
            user = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye")
            break
        if not user:
            continue
        if user.lower() in {"exit", "quit"}:
            print("Bye")
            break
        state["messages"].append(HumanMessage(content=user))
        # Run graph until it reaches END (no more tool calls)
        result = app.invoke(state)
        # Extract last AI message for display
        last_ai = None
        for m in result["messages"][::-1]:
            if isinstance(m, AIMessage) and m.content:
                last_ai = m
                break
        if last_ai:
            print(f"\nAgent: {last_ai.content}")
        state = result  # continue conversation with updated state

if __name__ == "__main__":
    chat()
