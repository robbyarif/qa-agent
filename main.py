import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Setup & Security
# Make sure you have a .env file with GEMINI_API_KEY=sk-...
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key or api_key == "your_key_here":
    print("Error: Please set your GEMINI_API_KEY in the .env file.")
    exit(1)

# Using OpenAI Python SDK with Gemini's OpenAI-compatible API endpoint
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 2. Mock Functions
def get_exchange_rate(currency_pair: str) -> str:
    """Mock function to get custom exchange rate."""
    print(f"[Mock] Getting exchange rate for {currency_pair}...")
    
    # Specific mock data required by the assignment
    rates = {
        "USD_TWD": "32.0",
        "JPY_TWD": "0.2",
        "EUR_USD": "1.2"
    }
    
    if currency_pair in rates:
        return json.dumps({"currency_pair": currency_pair, "rate": rates[currency_pair]})
    else:
        return json.dumps({"error": "Data not found"})

def get_stock_price(symbol: str) -> str:
    """Mock function to get custom stock price."""
    print(f"[Mock] Getting stock price for {symbol}...")
    
    # Specific mock data required by the assignment
    prices = {
        "AAPL": "260.00",
        "TSLA": "430.00",
        "NVDA": "190.00"
    }
    
    if symbol in prices:
        return json.dumps({"symbol": symbol, "price": prices[symbol]})
    else:
        return json.dumps({"error": "Data not found"})

# 3. Function Map (Dynamic execution without if-else chains)
available_functions = {
    "get_exchange_rate": get_exchange_rate,
    "get_stock_price": get_stock_price,
}

# 4. Tool Schemas with Strict Mode / Structured Outputs
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_exchange_rate",
            "description": "Get the exchange rate for a given currency pair.",
            "parameters": {
                "type": "object",
                "properties": {
                    "currency_pair": {
                        "type": "string", 
                        "description": "The currency pair to look up (e.g., USD_TWD, JPY_TWD, EUR_USD)"
                    }
                },
                "required": ["currency_pair"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get the current stock price for a given stock symbol.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string", 
                        "description": "The stock symbol to look up (e.g., AAPL, TSLA, NVDA)"
                    }
                },
                "required": ["symbol"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

def run_agent():
    # 5. System Prompt (Persona)
    messages = [
        {"role": "system", "content": "You are a helpful Financial Assistant. You can help the user check the exchange rates and stock prices by using your tools. Be concise but polite."}
    ]
    
    print("Financial Assistant Agent Started. Type 'exit' to quit.")

    # 6. Robust Agent Loop
    while True:
        try:
            user_input = input("User: ")
        except EOFError:
            break
            
        if user_input.lower() in ["exit", "quit"]:
            break
            
        messages.append({"role": "user", "content": user_input})

        try:
            # First API Call
            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            response_msg = response.choices[0].message
            tool_calls = response_msg.tool_calls

            if tool_calls:
                # IMPORTANT: Add the assistant's "thought" (tool call request) to history
                # This ensures the model knows what tools it just invoked
                messages.append(response_msg)
                
                # Handle Parallel Tool Calls
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    print(f"\n[Debug] Executing tool: {function_name} with arguments {function_args}")
                    
                    # Dynamic Dispatch using Function Map
                    function_to_call = available_functions.get(function_name)
                    
                    if function_to_call:
                        try:
                            # Safely pass arguments as **kwargs
                            tool_result = function_to_call(**function_args)
                        except Exception as e:
                            tool_result = json.dumps({"error": str(e)})
                    else:
                        tool_result = json.dumps({"error": "Function not found"})
                    
                    # Append RESULT to history for each tool called
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": tool_result,
                    })
                
                # Second API Call (Get final answer with context of tool results)
                final_response = client.chat.completions.create(
                    model="gemini-2.5-flash",
                    messages=messages
                )
                
                final_content = final_response.choices[0].message.content
                print(f"Agent: {final_content}")
                messages.append({"role": "assistant", "content": final_content})
                
            else:
                # No tool needed, normal text response
                print(f"Agent: {response_msg.content}")
                messages.append({"role": "assistant", "content": response_msg.content})
                
        except Exception as e:
            print(f"[Error] Failed to process response: {e}")
            # Do not append the failed assistant state so the user can just continue normally

if __name__ == "__main__":
    run_agent()
