from langgraph.graph import StateGraph, START, END

from .state_logic import WorkflowState, extraction_node, validation_node, confidence_node

def build_graph():
    graph = StateGraph(WorkflowState)

    graph.add_node("extract", extraction_node)
    graph.add_node("validate", validation_node)
    graph.add_node("confidence", confidence_node)

    graph.add_edge(START, "extract")
    graph.add_edge("extract", "validate")
    graph.add_edge("validate", "confidence")
    graph.add_edge("confidence", END)

    return graph.compile()