from openai import OpenAI
import requests
from pydantic import BaseModel
from typing import Dict, Any

client = OpenAI()


supa_search = {
    "type": "function",
    "function": {
            "name": "supa_search",
            "description": "Get the optimal tool to use.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A description of the user's intent, e.g. 'weather in Boston today'",
                    },
                },
                "required": ["query"],
            },
    }
}


def supa_search(query):
    # Use supa_search to find the optimal tool
    res = requests.get(f"http://localhost:8000/get_tool?searchQuery={query}")
    return res.json()["tool_spec"]


def find_and_execute_tool(user_query):
    # Create the messages for the supa_search
    messages = [
        {"role": "user", "content": user_query}
    ]

    optimal_tool = supa_search(user_query)

    # Execute the optimal tool
    optimal_params = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=[optimal_tool],
        tool_choice={"type": "function", "function": {
            "name": optimal_tool["function"]["name"]}}
    )

    return optimal_params


if __name__ == "__main__":
    user_query = "What are sports news today for san francisco?"
    print(find_and_execute_tool(user_query))
