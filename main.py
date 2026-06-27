import sys
import json
import sqlite3
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

from src.state import AgentState
from src.nodes.data_extractor import data_extractor
from src.nodes.dependency_analyzer import dependency_analyzer
from src.nodes.market_researcher import market_researcher
from src.nodes.risk_evaluator import risk_evaluator

# Node to create an interrupt point for human intervention
def human_review_node(state: AgentState) -> dict:
    print("--- NODE: HUMAN REVIEW ---")
    return {}

def build_graph():
    workflow = StateGraph(AgentState)
    
    # 1. Define nodes
    workflow.add_node("data_extractor", data_extractor)
    workflow.add_node("dependency_analyzer", dependency_analyzer)
    workflow.add_node("market_researcher", market_researcher)
    workflow.add_node("risk_evaluator", risk_evaluator)
    workflow.add_node("human_review", human_review_node) 
    
    # 2. Define standard execution flow
    workflow.set_entry_point("data_extractor")
    workflow.add_edge("data_extractor", "dependency_analyzer")
    workflow.add_edge("dependency_analyzer", "market_researcher")
    workflow.add_edge("market_researcher", "risk_evaluator")
    
    # 3. Conditional routing after AI risk evaluation
    def route_after_evaluation(state: AgentState):
        if state.get("recommendation") in ["REJECT_OR_ESCALATE", "ESCALATE_FOR_MANUAL_REVIEW"]:
            return "human_review"
        return END

    workflow.add_conditional_edges("risk_evaluator", route_after_evaluation)
    workflow.add_edge("human_review", END)
    
    # 4. Integrate SQLite memory (Step 7) - FIXED INITIALIZATION
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    memory = SqliteSaver(conn)
    
    # 5. Compile graph with interrupt configuration (Step 8)
    return workflow.compile(
        checkpointer=memory,
        interrupt_before=["human_review"]
    )

if __name__ == "__main__":
    app_id = sys.argv[1] if len(sys.argv) > 1 else "FACT-2026-001"
    print(f"\nSTARTING RISK ASSESSMENT FOR: {app_id}")
    
    graph = build_graph()
    thread = {"configurable": {"thread_id": app_id}} 
    initial_state = {"application_id": app_id}

    # First run of the graph
    for event in graph.stream(initial_state, thread):
        for node_name, node_state in event.items():
            print(f"Completed Node: {node_name}")

    current_state = graph.get_state(thread)
    
    # Check if the system is paused for human review
    if current_state.next:
        print("\n" + "="*60)
        print("SYSTEM PAUSED: MANUAL CREDIT REVIEW REQUIRED")
        print("="*60)
        
        state_data = current_state.values
        print(f"Borrower:      {state_data.get('seller_name')}")
        print(f"Counterparty:  {state_data.get('buyer_name')}")
        print(f"AI Risk Level: {state_data.get('risk_level')}")
        print(f"Reasoning:     {state_data.get('risk_reasoning')}")
        print(f"AI Suggests:   {state_data.get('recommendation')}")
        print("-" * 60)
        
        # Await user input via terminal
        user_input = input("\nAction Required - APPROVE or REJECT? (Y/N): ").strip().upper()
        human_decision = "APPROVED_BY_HUMAN" if user_input == "Y" else "REJECTED_BY_HUMAN"
        
        print(f"\nUpdating state with decision: {human_decision}...")
        graph.update_state(thread, {"human_decision": human_decision})
        
        # Resume graph execution
        print("Resuming workflow...")
        for event in graph.stream(None, thread):
            for node_name, node_state in event.items():
                print(f"Completed Node: {node_name}")
                
    print("\nWORKFLOW COMPLETED. FINAL REPORT:")
    final_state = graph.get_state(thread).values
    
    report = {
        "application_id": final_state.get("application_id"),
        "seller_name": final_state.get("seller_name"),
        "dependency_ratio": final_state.get("dependency_ratio"),
        "ai_risk_level": final_state.get("risk_level"),
        "human_decision": final_state.get("human_decision", "AUTO_PROCESSED")
    }
    
    print(json.dumps(report, indent=4))