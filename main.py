from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI()


class ToolSpec(BaseModel):
    type: str
    function: Dict[str, Any]


class ResponseModel(BaseModel):
    tool_spec: ToolSpec
    metadata: Dict[str, Any]


@app.get("/get_tool", response_model=ResponseModel)
async def get_tool(searchQuery: str = Query(..., description="The search query to determine the tool specification")):
    if "weather" in searchQuery.lower():
        tool_spec = {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            }
        }
        metadata = {
            "endpoint": "/get_current_weather",
            "info": "This tool provides current weather information based on location."
        }
    elif "news" in searchQuery.lower():
        tool_spec = {
            "type": "function",
            "function": {
                "name": "get_latest_news",
                "description": "Get the latest news headlines",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "The news category, e.g. technology, sports, etc.",
                        },
                        "location": {
                            "type": "string",
                            "description": "The location for localized news, e.g. New York, USA",
                        },
                    },
                    "required": ["category"],
                },
            }
        }
        metadata = {
            "endpoint": "/get_latest_news",
            "info": "This tool provides the latest news headlines based on category and location."
        }
    elif "stock" in searchQuery.lower():
        tool_spec = {
            "type": "function",
            "function": {
                "name": "get_stock_price",
                "description": "Get the current stock price for a given company",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The stock symbol of the company, e.g. AAPL for Apple Inc.",
                        },
                    },
                    "required": ["symbol"],
                },
            }
        }
        metadata = {
            "endpoint": "/get_stock_price",
            "info": "This tool provides the current stock price for a given company based on its stock symbol."
        }
    else:
        tool_spec = None
        metadata = {
            "error": "No suitable tool found for the given query"
        }

    return {"tool_spec": tool_spec, "metadata": metadata}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
