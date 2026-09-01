from typing import TypedDict
from skill_gap import analyze_skill_gap

from langgraph.graph import StateGraph, START, END


# --------------------------------------------------
# 1. State
# --------------------------------------------------

class CareerState(TypedDict):

    question: str
    target_role: str
    result: str


# --------------------------------------------------
# 2. Skill Gap Node
# --------------------------------------------------

def skill_gap_node(state: CareerState):

    result = analyze_skill_gap(
        state["question"],
        state["target_role"]
    )

    return {
        "result": result
    }


# --------------------------------------------------
# 3. Resume Analysis Node
# --------------------------------------------------

def resume_analysis_node(state: CareerState):

    return {
        "result": "Resume Analysis selected."
    }


# --------------------------------------------------
# 4. Interview Preparation Node
# --------------------------------------------------

def interview_prep_node(state: CareerState):

    return {
        "result": "Interview Preparation selected."
    }


# --------------------------------------------------
# 5. Router
# --------------------------------------------------

def route_request(state: CareerState):

    question = state["question"].lower()

    if "skill" in question:

        return "skill_gap"

    elif "resume" in question:

        return "resume_analysis"

    elif "interview" in question:

        return "interview_prep"

    else:

        return "skill_gap"


# --------------------------------------------------
# 6. Create Graph
# --------------------------------------------------

graph_builder = StateGraph(CareerState)


# Add nodes

graph_builder.add_node(
    "skill_gap",
    skill_gap_node
)

graph_builder.add_node(
    "resume_analysis",
    resume_analysis_node
)

graph_builder.add_node(
    "interview_prep",
    interview_prep_node
)


# --------------------------------------------------
# 7. Conditional Routing
# --------------------------------------------------

graph_builder.add_conditional_edges(

    START,

    route_request,

    {
        "skill_gap": "skill_gap",
        "resume_analysis": "resume_analysis",
        "interview_prep": "interview_prep"
    }
)


# --------------------------------------------------
# 8. Connect Nodes to END
# --------------------------------------------------

graph_builder.add_edge(
    "skill_gap",
    END
)

graph_builder.add_edge(
    "resume_analysis",
    END
)

graph_builder.add_edge(
    "interview_prep",
    END
)


# --------------------------------------------------
# 9. Compile
# --------------------------------------------------

career_graph = graph_builder.compile()


# --------------------------------------------------
# 10. Test
# --------------------------------------------------

question = input(
    "What do you want help with? "
)

target_role = input(
    "What is your target role? "
)


result = career_graph.invoke({

    "question": question,

    "target_role": target_role,

    "result": ""
})


print("\nResult:")
print(result["result"])