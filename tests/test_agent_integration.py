# End-to-end integration test for the research assistant
# Requires OpenAI API access and live PubMed connectivity

from src.agent import graph


def test_pubmed_and_calculator():
    config = {
        "configurable": {
            "thread_id": "integration_test"
        }
    }

    query = (
        "Search PubMed for 'Fully Automated Deep Learning Model "
        "to Detect Clinically Significant Prostate Cancer at MRI'. "
        "Find the external test AUC values for the model and radiologists. "
        "Use the calculator to calculate the difference in percentage points."
    )

    response = graph.invoke(
        {"messages": [("user", query)]},
        config=config
    )

    # Extract names of tools actually called
    tools_used = [
        call["name"]
        for msg in response["messages"]
        for call in getattr(msg, "tool_calls", [])
    ]

    # Verify both tools were selected
    assert "pubmed_search" in tools_used
    assert "calculator" in tools_used

    # Verify the agent produced a final answer
    assert response["messages"][-1].content

    print("Integration test passed!")