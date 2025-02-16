import os
from dotenv import load_dotenv
import openai
from typing import Annotated
from typing_extensions import TypedDict
from django.core.management.base import BaseCommand
# For typed messages rather than dict-based
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# LangGraph imports
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import requests
from datetime import datetime

# Set the prediction endpoint URL (adjust if needed)
URL = "https://1398-68-65-164-53.ngrok-free.app/predict"

load_dotenv()

# Initialize the OpenAI client using the API key from environment
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai(messages):
    """
    messages: List of dicts like { 'role': 'system'|'user'|'assistant', 'content': <string> }
    Returns the string content of the model's reply.
    """
    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-4", etc.
        messages=messages,
        temperature=0.0
    )
    return response.choices[0].message.content

class MyState(TypedDict):
    # Store typed messages from the beginning
    messages: Annotated[list, add_messages]
    # New keys for the three data inputs:
    ds_data: dict
    mobile_data: dict
    os_data: dict
    os_answer: str
    mobile_answer: str
    application_answer: str
    final_answer: str

graph_builder = StateGraph(MyState)

def orchestrator_initial(state: MyState) -> dict:
    """
    The initial orchestrator call: acknowledge the user's request.
    """
    if state["messages"]:
        user_input = state["messages"][-1].content
    else:
        user_input = "No user input"

    prompt = (
        "You are the Orchestrator. The user said:\n\n"
        f"{user_input}\n\n"
        "Acknowledge the request. Next, we will gather Distributed Systems, Mobile Systems, and "
        "Operating Systems perspectives before providing a final answer."
    )
    ai_response = call_openai(
        [
            {"role": "system", "content": prompt}
        ]
    )
    return {"messages": [AIMessage(content=ai_response)]}

def os_llm(state: MyState) -> dict:
    """
    Distributed Systems perspective.
    """
    if state["messages"]:
        user_input = state["messages"][0].content
    else:
        user_input = "No user input"

    ds_data = state["ds_data"]
    function_output = requests.post(URL, json=ds_data)
    print(function_output.content)

    prompt = (
        "You are a Distributed Systems expert. Based on the following function output (which "
        "states the probability of an error occurring in Distributed Systems, where 0 means no error "
        "and 1 means there is an error) and the user's query, tell the user whether the problem "
        "comes from Distributed Systems along with the probability.\n\n"
        f"{function_output.content}\n\n"
        "User question:\n"
        f"{user_input}\n\n"
        "Answer:"
    )
    ai_response = call_openai(
        [
            {"role": "system", "content": prompt}
        ]
    )
    return {"os_answer": ai_response}

def mobile_llm(state: MyState) -> dict:
    """
    Mobile Systems perspective.
    """
    if state["messages"]:
        user_input = state["messages"][0].content
    else:
        user_input = "No user input"

    mobile_data = state["mobile_data"]
    function_output = requests.post(URL, json=mobile_data)
    print(function_output.content)

    prompt = (
        "You are a Mobile Systems expert. Based on the following function output (which "
        "states the probability of an error occurring in Mobile Systems, where 0 means no error "
        "and 1 means there is an error) and the user's query, tell the user whether the problem "
        "comes from Mobile Systems along with the probability.\n\n"
        f"{function_output.content}\n\n"
        "User question:\n"
        f"{user_input}\n\n"
        "Answer:"
    )
    ai_response = call_openai(
        [
            {"role": "system", "content": prompt}
        ]
    )
    return {"mobile_answer": ai_response}

def application_llm(state: MyState) -> dict:
    """
    Operating Systems perspective.
    """
    if state["messages"]:
        user_input = state["messages"][0].content
    else:
        user_input = "No user input"

    os_data = state["os_data"]
    function_output = requests.post(URL, json=os_data)
    print(function_output.content)

    prompt = (
        "You are an Operating Systems expert. Based on the following function output (which "
        "states the probability of an error occurring in Operating Systems, where 0 means no error "
        "and 1 means there is an error) and the user's query, tell the user whether the problem "
        "comes from Operating Systems along with the probability.\n\n"
        f"{function_output.content}\n\n"
        "User question:\n"
        f"{user_input}\n\n"
        "Answer:"
    )
    ai_response = call_openai(
        [
            {"role": "system", "content": prompt}
        ]
    )
    return {"application_answer": ai_response}

def orchestrator_combine(state: MyState) -> dict:
    """
    Final orchestrator call: combine the three expert answers.
    """
    os_ans = state.get("os_answer", "")
    mobile_ans = state.get("mobile_answer", "")
    app_ans = state.get("application_answer", "")

    prompt = (
        "You have the following three expert answers:\n\n"
        f"Distributed Systems perspective:\n{os_ans}\n\n"
        f"Mobile Systems perspective:\n{mobile_ans}\n\n"
        f"Operating Systems perspective:\n{app_ans}\n\n"
        "Combine them into a single, concise answer for the user."
    )
    ai_response = call_openai(
        [
            {"role": "system", "content": prompt}
        ]
    )
    return {"final_answer": ai_response}

# Add nodes and edges to the graph.
graph_builder.add_node("orchestrator_initial", orchestrator_initial)
graph_builder.add_node("os_llm", os_llm)
graph_builder.add_node("mobile_llm", mobile_llm)
graph_builder.add_node("application_llm", application_llm)
graph_builder.add_node("orchestrator_combine", orchestrator_combine)

# Define a linear flow for the graph:
graph_builder.add_edge(START, "orchestrator_initial")
graph_builder.add_edge("orchestrator_initial", "os_llm")
graph_builder.add_edge("os_llm", "mobile_llm")
graph_builder.add_edge("mobile_llm", "application_llm")
graph_builder.add_edge("application_llm", "orchestrator_combine")
graph_builder.add_edge("orchestrator_combine", END)

graph = graph_builder.compile()

class Command(BaseCommand):
    help = "Runs the LangGraph orchestrator to process a user query with multiple LLM perspectives and stores the output in a Markdown report."

    def handle(self, *args, **options):
        # Create a list to capture output lines.
        output_lines = []

        def write_line(msg):
            """Helper function to write a message and store it."""
            # Write to the standard output.
            self.stdout.write(msg)
            # Append the message with a newline.
            output_lines.append(msg + "\n")

        from langchain.schema import HumanMessage  # Import HumanMessage locally if needed
        user_query = "My Mac shows a strange error for 3 days. What could be causing it?"
        initial_state = {
            "messages": [HumanMessage(content=user_query)],
            "ds_data": {"features": [21, 0, 0, 203, 0, 3, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 1, 3, 0, 0, 3, 0, 0, 0]},
            "mobile_data": {"features": [25, 1, 0, 190, 1, 2, 0, 1, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 0, 1, 2, 0, 0, 0]},
            "os_data": {"features": [20, 0, 1, 210, 0, 3, 0, 0, 1, 3, 0, 3, 0, 1, 0, 0, 0, 0, 0, 0, 1, 3, 1, 3, 0, 0, 3, 0, 1, 0]},
            "os_answer": "",
            "mobile_answer": "",
            "application_answer": "",
            "final_answer": "",
        }

        write_line("Running orchestrator graph...")

        # Stream events from the graph.
        for idx, event in enumerate(graph.stream(initial_state)):
            write_line(f"\n## Event {idx}")
            write_line(f"State keys: {list(event.keys())}")
            # Iterate over event contents safely.
            for key, value in event.items():
                if isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        if isinstance(subvalue, list):
                            subvalue_str = "\n".join(str(item) for item in subvalue)
                        else:
                            subvalue_str = str(subvalue)
                        write_line(f"{key} -> {subkey}: {subvalue_str}")
                elif isinstance(value, list):
                    value_str = "\n".join(str(item) for item in value)
                    write_line(f"{key}: {value_str}")
                else:
                    write_line(f"{key}: {value}")

        write_line("Orchestration completed.")

        # Determine the report folder and filename.
        report_dir = os.path.join(os.getcwd(), "agentic_historical_reports")
        os.makedirs(report_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"report_{timestamp}.md"
        report_path = os.path.join(report_dir, report_filename)

        # Write the collected output to the Markdown file.
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("## Orchestrator Report\n\n")
            f.writelines(output_lines)

        write_line(f"Report saved to: {report_path}")
        self.stdout.write(self.style.SUCCESS("Orchestration completed and report saved."))