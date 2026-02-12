I'll create a comprehensive summary of this Agent SDK introduction.

# Summary: Introduction to OpenAI Agent SDK

## What is OpenAI Agent SDK?

**Official Definition:**
> "A lightweight, easy-to-use package that enables building AI agent apps with very few abstractions. It's a production-ready upgrade from previous Agent experiments."

---

## Core Primitives

The Agent SDK has 4 main primitives:

1. **Agents** - The AI entities
2. **Handoffs** - Transfer between agents
3. **Guardrails** - Safety controls
4. **Sessions** - Conversation management

---

## What is an Agent?

### Traditional Definition

```
Agent = LLM + Custom Instructions + Tools + Management
```

**Components:**
- **LLM** (OpenAI, Gemini, Claude, etc.)
- **Custom Instructions** (System prompts)
- **Tools** (Functions agent can call)
- **Guardrails** (Input/output validation)
- **History Management** (Conversation context)

---

## Before Agent SDK: Manual Implementation

### Old Way (From Previous Lessons)

```python
# Manual agent implementation
messages = []  # History management
system_prompt = "You are a helpful assistant..."  # Instructions

while True:  # Manual orchestration loop
    # Make LLM call
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    
    # Check if tool call
    if response.choices[0].message.tool_calls:
        # Manually handle tool call
        tool_result = execute_tool(...)
        messages.append(...)  # Manually update history
        continue  # Loop again
    
    # Check if final output
    if response.choices[0].finish_reason == "stop":
        break  # Exit loop
    
    # Handle other cases...
```

**Problems:**
- Manual loop management
- Manual tool call handling
- Manual history tracking
- Complex orchestration logic
- Hard to maintain

---

## With Agent SDK: Simplified Implementation

### Installation

```bash
pip install openai-agents-sdk
```

### Update requirements.txt

```bash
pip freeze > requirements.txt
```

---

### Hello World Agent

```python
# hello.py
from dotenv import load_dotenv
from agents import Agent, Runner

# Load environment variables
load_dotenv()

# Define agent
hello_agent = Agent(
    name="hello-world-agent",
    instructions="""
    You are an agent which greets the user and helps them 
    answer using emojis and in a funny manner.
    """
)

# Run agent
result = Runner.run_sync(
    agent=hello_agent,
    input="Hi! My name is Piyush"
)

# Print output
print(result.final_output)
```

**Output:**
```
Hey Piyush! 👋 Welcome to the fun zone! 🎉 
Flash your best smile 'cause you're about to have a blast! 😄✨
```

---

## Key Differences: Old vs New

### Manual Implementation vs Agent SDK

| Aspect | Manual (Old) | Agent SDK (New) |
|--------|--------------|-----------------|
| **Loop management** | `while True:` loop | `Runner.run_sync()` |
| **Tool calling** | Manual detection & execution | Automatic |
| **History** | Manual `messages` array | Automatic |
| **Orchestration** | Complex if/else logic | Abstracted |
| **Code length** | 100+ lines | ~10 lines |
| **Maintainability** | Hard | Easy |

---

## How Agent SDK Works Under the Hood

### What `Runner.run_sync()` Does

```python
# Simplified internal logic (what SDK does for you)
def run_sync(agent, input):
    messages = []  # Initialize history
    
    while True:  # Orchestration loop
        # 1. Make LLM call
        response = llm_call(agent.instructions, messages, input)
        
        # 2. Check response type
        if is_tool_call(response):
            # Execute tool automatically
            result = execute_tool(response)
            messages.append(result)
            continue  # Loop again
        
        elif is_planning(response):
            # Handle planning
            messages.append(response)
            continue  # Loop again
        
        elif is_final_output(response):
            # Return final answer
            return response  # Exit loop
        
        # Handle other cases...
```

**Everything abstracted!**

---

## Agent Structure

### Basic Agent Components

```python
from agents import Agent

agent = Agent(
    name="agent-name",           # Identifier
    instructions="...",          # System prompt
    tools=[...],                 # Optional: Functions
    guardrails=[...],            # Optional: Safety
    # More options...
)
```

---

### Agent with Tools (Preview)

```python
from agents import Agent

def get_weather(location: str) -> str:
    """Get current weather for location"""
    # Implementation
    return f"Weather in {location}: Sunny, 25°C"

weather_agent = Agent(
    name="weather-agent",
    instructions="Help users with weather information",
    tools=[get_weather]  # Attach tools
)

# Tools automatically called when needed!
result = Runner.run_sync(
    agent=weather_agent,
    input="What's the weather in London?"
)
```

**SDK handles:**
- Tool detection
- Tool execution
- Result integration
- Looping until done

---

## Setup for This Section

### File Structure

```
agent_sdk/
├── .env                 # API keys
├── hello.py             # First agent
└── requirements.txt     # Dependencies
```

### Environment Setup

```bash
# .env file
OPENAI_API_KEY=sk-...
```

### Code Template

```python
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

# Your agent code here
```

---

## Running the Agent

```bash
# Activate environment
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

# Run agent
python agent_sdk/hello.py
```

---

## Key Concepts

### 1. Agent Definition

```python
agent = Agent(
    name="my-agent",
    instructions="Your custom prompt"
)
```

**What it is:**
- A configuration object
- Defines agent behavior
- Doesn't run anything yet

---

### 2. Runner Execution

```python
result = Runner.run_sync(
    agent=agent,
    input="User message"
)
```

**What it does:**
- Executes the agent
- Handles all orchestration
- Returns final output

---

### 3. Result Object

```python
result = Runner.run_sync(...)

# Access final output
print(result.final_output)

# Can also access:
# - result.messages (conversation history)
# - result.tool_calls (tools used)
# - result.iterations (loop count)
```

---

## Abstraction Benefits

### What SDK Handles Automatically

✅ **Conversation History**
- Automatically tracks messages
- Maintains context

✅ **Tool Calling**
- Detects when tools needed
- Executes tools
- Integrates results

✅ **Orchestration Loop**
- Runs until completion
- Handles all states
- No manual loop needed

✅ **Error Handling**
- Retries on failures
- Graceful degradation

✅ **Streaming** (optional)
- Real-time outputs
- Token-by-token

---

## What's Coming Next

### Topics to Cover

1. **Tools** - Function calling
2. **Streaming** - Real-time responses
3. **MCP (Model Context Protocol)** - Advanced context
4. **Handoffs** - Multi-agent systems
5. **Guardrails** - Safety & validation
6. **Sessions** - Persistent conversations

---

## Simple vs Complex Agents

### Simple Agent (Hello World)

```python
Agent(
    name="greeter",
    instructions="Greet users warmly"
)
# Just responds to input
```

### Complex Agent (Weather)

```python
Agent(
    name="weather-assistant",
    instructions="Help with weather queries",
    tools=[get_weather, get_forecast],
    guardrails=[validate_location],
)
# Can call tools, validate inputs, etc.
```

**Same SDK, scales easily!**

---

## Why Use Agent SDK?

### Advantages

| Benefit | Impact |
|---------|--------|
| **Less code** | 90% reduction |
| **Production-ready** | Built-in best practices |
| **Maintainable** | Clear structure |
| **Scalable** | Easy to add features |
| **Abstractions** | Focus on logic, not plumbing |

### When to Use

✅ Building production agents  
✅ Need tool calling  
✅ Multi-agent systems  
✅ Complex workflows  
✅ Maintainable codebase  

---

## Quick Reference

### Basic Agent Template

```python
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

# Define
agent = Agent(
    name="my-agent",
    instructions="Custom instructions"
)

# Run
result = Runner.run_sync(
    agent=agent,
    input="User input"
)

# Output
print(result.final_output)
```

---

## Key Takeaways

1. **Agent SDK simplifies** agent development dramatically
2. **Abstracts complexity** - loops, tools, history automatic
3. **Production-ready** - built by OpenAI for real apps
4. **Scales easily** - simple to complex agents
5. **Coming features** - tools, streaming, MCP, handoffs

**Next: Adding tools to agents** 🛠️

---

## Comparison Example

### Manual (50+ lines)
```python
messages = []
while True:
    response = client.chat.completions.create(...)
    if tool_calls:
        for tool in tool_calls:
            result = execute_tool(...)
            messages.append(...)
        continue
    elif ...:
        # more logic
    break
```

### Agent SDK (5 lines)
```python
agent = Agent(name="...", instructions="...")
result = Runner.run_sync(agent=agent, input="...")
print(result.final_output)
```

**90% less code, same functionality!** 🚀


I'll create a comprehensive summary of working with tools in the Agent SDK.

# Summary: Agent SDK - Working with Tools

## Three Types of Tools

The OpenAI Agent SDK supports three types of tools:

| Type | Description | Provider |
|------|-------------|----------|
| **Hosted Tools** | Pre-built by OpenAI | OpenAI |
| **Function Calls** | Custom Python functions | You |
| **Agent as Tool** | Use another agent | You |

---

## 1. Hosted Tools (Built by OpenAI)

### What Are Hosted Tools?

**Pre-built tools provided by OpenAI** that you can use out-of-the-box:

- ✅ **Web Search Tool** - Search the internet
- ✅ **File Search Tool** - Search through files
- ✅ **Code Interpreter** - Execute Python code
- ✅ **Computer Tool** - Computer use/automation
- ✅ **Image Generation** - Create images
- ✅ **Local Shell Tool** - Run shell commands

**Note:** This list grows over time as OpenAI adds more tools

---

## Web Search Tool Example

### Code Implementation

```python
# agent_with_tool.py
from dotenv import load_dotenv
from agents import Agent, Runner
from agents import WebSearchTool  # Import hosted tool

load_dotenv()

# Define agent with web search capability
agent = Agent(
    name="web-search-agent",
    instructions="""
    You are an agent that can search the web 
    to answer user questions accurately.
    """,
    tools=[WebSearchTool]  # Add tool here
)

# Run agent
result = Runner.run_sync(
    agent=agent,
    input="What is on piyushgarg.dev website?"
)

print(result.final_output)
```

---

### Example 1: Website Search

**Input:**
```python
input="What is on piyushgarg.dev website?"
```

**Output:**
```
Hey there, tech adventurer! Want to peek into the mystical 
world of piyushgarg.dev? 

This website belongs to Piyush Garg. Here's what you'll find:

📚 Introduction - Learn about Piyush
🎓 Courses - Educational content
🎥 Video Content - Tutorials and guides
🔗 Links - Social media and resources

The website showcases Piyush's work in tech education!
```

**What happened:**
1. Agent received query
2. Detected need for web search
3. **Automatically called WebSearchTool**
4. Got website content
5. Formatted response

---

### Example 2: Weather Information

**Input:**
```python
input="Can you please fetch weather information for Patiala, pin code 147001?"
```

**Output:**
```
Weather Information for Patiala (147001):

🌡️ Current Temperature: 18°C
☁️ Condition: Partly Cloudy
💨 Wind: 12 km/h
💧 Humidity: 65%

Historical Data:
- Yesterday: 20°C, Sunny
- Last Week Average: 17°C
```

**What happened:**
1. Agent parsed location request
2. Used WebSearchTool to find weather
3. Retrieved current and historical data
4. Formatted user-friendly response

---

### Without Web Search Tool

**Same code, but tool commented out:**

```python
agent = Agent(
    name="limited-agent",
    instructions="Help users with information",
    # tools=[WebSearchTool]  # Commented out!
)

result = Runner.run_sync(
    agent=agent,
    input="Fetch weather for Patiala"
)
```

**Output:**
```
Hey there! My weather powers only work in places I can see 👀

To get weather for Patiala, you'll need to:
1. Open Google
2. Search "weather Patiala"
3. Check the results manually

Sorry, I can't fetch real-time data without my web search tool! 🔍
```

**Key difference:** Agent knows its limitations without tools

---

## How Hosted Tools Work

### Internal Process (Abstracted)

```
User Input
    ↓
Agent analyzes query
    ↓
Detects need for web search
    ↓
Calls WebSearchTool (automatic)
    ↓
Gets results from web
    ↓
Integrates results
    ↓
Formats response
    ↓
Returns to user
```

**All orchestration handled by SDK!**

---

## Available Hosted Tools

### 1. Web Search Tool

```python
from agents import WebSearchTool

agent = Agent(
    name="searcher",
    tools=[WebSearchTool]
)
```

**Use cases:**
- Real-time information
- Current events
- Website content
- Research queries

---

### 2. File Search Tool

```python
from agents import FileSearchTool

agent = Agent(
    name="file-searcher",
    tools=[FileSearchTool]
)
```

**Use cases:**
- Search through documents
- Find specific content
- Document analysis

---

### 3. Code Interpreter

```python
from agents import CodeInterpreterTool

agent = Agent(
    name="code-runner",
    tools=[CodeInterpreterTool]
)
```

**Use cases:**
- Execute Python code
- Data analysis
- Calculations
- File processing

---

### 4. Computer Tool

```python
from agents import ComputerTool

agent = Agent(
    name="computer-user",
    tools=[ComputerTool]
)
```

**Use cases:**
- Automate tasks
- GUI interactions
- System operations

---

### 5. Image Generation

```python
from agents import ImageGenerationTool

agent = Agent(
    name="artist",
    tools=[ImageGenerationTool]
)
```

**Use cases:**
- Create images
- Visual content
- Design assistance

---

### 6. Local Shell Tool

```python
from agents import LocalShellTool

agent = Agent(
    name="shell-runner",
    tools=[LocalShellTool]
)
```

**Use cases:**
- Run shell commands
- System administration
- File operations

⚠️ **Security warning:** Be careful with shell access!

---

## Multiple Tools Example

### Agent with Multiple Capabilities

```python
from agents import (
    Agent, 
    Runner,
    WebSearchTool,
    CodeInterpreterTool,
    FileSearchTool
)

multi_tool_agent = Agent(
    name="super-agent",
    instructions="You can search web, run code, and search files",
    tools=[
        WebSearchTool,
        CodeInterpreterTool,
        FileSearchTool
    ]
)

# Agent automatically chooses right tool!
result = Runner.run_sync(
    agent=multi_tool_agent,
    input="Search web for Python tutorials, then create a summary file"
)
```

**Agent decides which tool to use based on task!**

---

## Tool Selection Logic

### How Agent Chooses Tools

```
User: "What's the weather in Paris?"
    ↓
Agent analyzes: Need real-time data
    ↓
Available tools:
- WebSearchTool ✓ (can get real-time data)
- CodeInterpreterTool ✗ (not relevant)
    ↓
Agent selects: WebSearchTool
    ↓
Executes search
    ↓
Returns result
```

**Automatic tool selection!**

---

## Tool Configuration

### Basic Usage

```python
# Simple - use default settings
tools=[WebSearchTool]
```

### Advanced Configuration (if supported)

```python
# Some tools accept parameters
tools=[
    WebSearchTool(
        max_results=5,
        region="US"
    )
]
```

**Check individual tool documentation for options**

---

## Error Handling

### When Tool Fails

```python
agent = Agent(
    name="resilient-agent",
    instructions="""
    If a tool fails, try to help the user anyway
    by explaining what went wrong.
    """,
    tools=[WebSearchTool]
)
```

**SDK handles failures gracefully:**
- Retries if appropriate
- Returns error to agent
- Agent can explain to user

---

## Testing Tools

### Run the Example

```bash
# Create file
# agent_sdk/agent_with_tool.py

# Run
python agent_sdk/agent_with_tool.py
```

### Expected Behavior

**With tool:**
```
Input: "What is on piyushgarg.dev?"
Output: [Detailed website information]
```

**Without tool:**
```
Input: "What is on piyushgarg.dev?"
Output: [Explanation that it can't access web]
```

---

## Best Practices

### 1. Choose Relevant Tools

```python
# ✅ Good - tools match agent purpose
weather_agent = Agent(
    name="weather",
    tools=[WebSearchTool]  # Needs real-time data
)

# ❌ Bad - unnecessary tools
greeter_agent = Agent(
    name="greeter",
    tools=[CodeInterpreterTool]  # Doesn't need code execution
)
```

---

### 2. Clear Instructions

```python
agent = Agent(
    name="research-assistant",
    instructions="""
    Use WebSearchTool to find current information.
    Always cite sources when using web search.
    """,
    tools=[WebSearchTool]
)
```

---

### 3. Tool Limitations

```python
agent = Agent(
    name="informed-agent",
    instructions="""
    You have access to web search for real-time info.
    If search fails, explain you can't access that data.
    """,
    tools=[WebSearchTool]
)
```

---

## Hosted Tool Benefits

| Benefit | Description |
|---------|-------------|
| **No implementation** | Pre-built by OpenAI |
| **Maintained** | Updates automatic |
| **Optimized** | Performance tuned |
| **Secure** | Security built-in |
| **Easy to use** | Just add to tools array |

---

## Comparison: With vs Without Tools

### Without Tools (Limited)

```python
agent = Agent(
    name="basic-agent",
    instructions="Answer questions"
    # No tools
)

# Can only use training data
# Can't access real-time info
# Can't perform actions
```

### With Tools (Powerful)

```python
agent = Agent(
    name="powered-agent",
    instructions="Answer questions using available tools",
    tools=[
        WebSearchTool,
        CodeInterpreterTool
    ]
)

# Can search web
# Can run code
# Can access real-time data
```

---

## Complete Working Example

```python
from dotenv import load_dotenv
from agents import Agent, Runner, WebSearchTool

load_dotenv()

# Create agent with web search
agent = Agent(
    name="web-researcher",
    instructions="""
    You are a research assistant that can search the web.
    Always provide accurate, up-to-date information.
    Cite sources when possible.
    """,
    tools=[WebSearchTool]
)

# Example queries
queries = [
    "What is on piyushgarg.dev?",
    "Current weather in London",
    "Latest Python version"
]

for query in queries:
    print(f"\nQuery: {query}")
    result = Runner.run_sync(agent=agent, input=query)
    print(f"Response: {result.final_output}\n")
    print("-" * 50)
```

---

## Key Takeaways

1. **Hosted tools** = Pre-built by OpenAI
2. **Just add to array** = `tools=[WebSearchTool]`
3. **Automatic execution** = SDK handles calling
4. **Multiple tools** = Agent chooses appropriate one
5. **Growing list** = More tools added over time
6. **No code needed** = Ready to use

---

## Next Topics

Coming up:
1. **Function calling** - Custom Python tools
2. **Agent as tool** - Multi-agent systems
3. **Tool parameters** - Advanced configuration

**Next: Creating custom function tools!** 🛠️

---

## Quick Reference

```python
# Import tools
from agents import (
    WebSearchTool,
    FileSearchTool,
    CodeInterpreterTool,
    ComputerTool,
    ImageGenerationTool,
    LocalShellTool
)

# Add to agent
agent = Agent(
    name="my-agent",
    instructions="...",
    tools=[WebSearchTool]  # Or any other tool
)

# Run (tools used automatically)
result = Runner.run_sync(agent=agent, input="...")
```

**That's it! Tools work automatically!** 🚀


# Summary: Function Tools in Agent SDK

## What Are Function Tools?

**Custom Python functions that agents can use as tools**

- You write the code
- Agent SDK handles orchestration
- Full control over functionality

---

## Creating a Function Tool

### Basic Structure

```python
from agents import function_tool

@function_tool  # Decorator makes it a tool
def my_custom_tool(parameter: str) -> str:
    """
    Description of what this tool does.
    
    Args:
        parameter: What this parameter is for.
    """
    # Your custom logic here
    return result
```

**Three requirements:**
1. `@function_tool` decorator
2. Type hints (parameters and return)
3. Docstring (for agent context)

---

## Weather Tool Example

### Complete Implementation

```python
from dotenv import load_dotenv
import requests
from agents import Agent, Runner, WebSearchTool, function_tool

load_dotenv()

# Custom function tool
@function_tool
def get_weather(city: str) -> str:
    """
    Fetch the weather for the given city name.
    
    Args:
        city: The city name to fetch the weather for.
    """
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"Weather in {city}: {response.text}"
    return f"Could not fetch weather for {city}"


# Agent with custom tool
agent = Agent(
    name="weather-agent",
    instructions="Help users with weather information using your tools",
    tools=[get_weather]  # Just pass reference, don't call!
)

# Run
result = Runner.run_sync(
    agent=agent,
    input="What is the weather in Patiala?"
)

print(result.final_output)
```

---

## Output Example

**Input:**
```
What is the weather in Patiala?
```

**Output:**
```
🌡️ The temperature is toasty 27°C in Patiala!
Perfect weather for rocking those shades 😎
```

---

## Key Points

### 1. Decorator Required

```python
from agents import function_tool

@function_tool  # This is mandatory!
def my_tool():
    pass
```

---

### 2. Docstring is Critical

```python
@function_tool
def get_weather(city: str) -> str:
    """
    Fetch the weather for the given city name.  # Description
    
    Args:
        city: The city name to fetch the weather for.  # Parameter docs
    """
```

**Why?** Agent uses docstring to understand:
- What the tool does
- When to use it
- What parameters mean

---

### 3. Pass Reference, Don't Call

```python
# ✅ Correct - pass reference
tools=[get_weather]

# ❌ Wrong - don't call it!
tools=[get_weather()]  # This causes error!
```

---

### 4. Type Hints Required

```python
# ✅ Good - has type hints
def get_weather(city: str) -> str:
    pass

# ❌ Bad - no type hints
def get_weather(city):
    pass
```

---

## Mixing Tool Types

### Hosted + Function Tools Together

```python
from agents import Agent, WebSearchTool, function_tool

@function_tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    # implementation
    pass

# Agent with multiple tool types
agent = Agent(
    name="multi-tool-agent",
    instructions="Use available tools to help users",
    tools=[
        WebSearchTool,      # Hosted tool
        get_weather         # Function tool
    ]
)
```

**Agent chooses appropriate tool automatically!**

---

## Multiple Function Tools

```python
@function_tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    pass

@function_tool
def calculate_distance(city1: str, city2: str) -> str:
    """Calculate distance between two cities."""
    pass

@function_tool
def get_time(timezone: str) -> str:
    """Get current time in timezone."""
    pass

# Agent with many tools
agent = Agent(
    name="travel-assistant",
    instructions="Help with travel planning",
    tools=[
        get_weather,
        calculate_distance,
        get_time
    ]
)
```

---

## Function Tool vs Hosted Tool

### Verification Test

```python
# With hosted WebSearchTool
agent1 = Agent(
    name="web-agent",
    tools=[WebSearchTool, get_weather]
)

# Without hosted tool - only function
agent2 = Agent(
    name="function-only-agent",
    tools=[get_weather]  # Only custom tool
)

# Both can get weather!
# Agent2 proves get_weather function is being called
```

---

## Error: Calling Instead of Referencing

### Common Mistake

```python
# ❌ Error: Cannot call tool
tools=[get_weather()]  # Adding () calls the function

# ✅ Correct: Pass reference
tools=[get_weather]  # No parentheses
```

**Error message:**
```
TypeError: tools must be tool references, not results
```

---

## Docstring Formats

### Simple Format

```python
@function_tool
def my_tool(param: str) -> str:
    """Short description of what tool does."""
    pass
```

### Detailed Format (Recommended)

```python
@function_tool
def my_tool(param: str, option: int) -> str:
    """
    Detailed description of the tool functionality.
    
    Args:
        param: Description of param.
        option: Description of option.
    
    Returns:
        Description of what is returned.
    """
    pass
```

---

## Name Override (Optional)

```python
@function_tool(name_override="custom_tool_name")
def internal_name(city: str) -> str:
    """Tool description."""
    pass
```

**When to use:**
- Function name is not descriptive
- Want different display name
- Avoiding name conflicts

---

## Complete Working Example

```python
from dotenv import load_dotenv
import requests
from agents import Agent, Runner, function_tool

load_dotenv()

# Define custom tools
@function_tool
def get_weather(city: str) -> str:
    """
    Fetch current weather for a city.
    
    Args:
        city: The city name to fetch weather for.
    """
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    return f"Weather in {city}: {response.text}"


@function_tool  
def convert_temperature(temp: float, from_unit: str, to_unit: str) -> str:
    """
    Convert temperature between units.
    
    Args:
        temp: Temperature value to convert.
        from_unit: Original unit (celsius/fahrenheit).
        to_unit: Target unit (celsius/fahrenheit).
    """
    if from_unit.lower() == "celsius" and to_unit.lower() == "fahrenheit":
        result = (temp * 9/5) + 32
    elif from_unit.lower() == "fahrenheit" and to_unit.lower() == "celsius":
        result = (temp - 32) * 5/9
    else:
        return "Invalid units"
    return f"{temp}° {from_unit} = {result:.1f}° {to_unit}"


# Create agent with custom tools
agent = Agent(
    name="weather-assistant",
    instructions="""
    You are a helpful weather assistant.
    Use get_weather to fetch current conditions.
    Use convert_temperature for unit conversions.
    """,
    tools=[get_weather, convert_temperature]
)

# Test queries
queries = [
    "What's the weather in London?",
    "Convert 25 celsius to fahrenheit"
]

for query in queries:
    result = Runner.run_sync(agent=agent, input=query)
    print(f"Q: {query}")
    print(f"A: {result.final_output}\n")
```

---

## Function Tool Requirements

| Requirement | Purpose |
|-------------|---------|
| `@function_tool` decorator | Marks as tool |
| Type hints | Agent knows parameter types |
| Docstring | Agent understands usage |
| Return value | Agent gets result |

---

## Key Takeaways

1. **`@function_tool`** decorator converts function to tool
2. **Docstring required** for agent context
3. **Type hints required** for proper calling
4. **Pass reference** not call (`get_weather` not `get_weather()`)
5. **Combine tools** - hosted + function work together
6. **Agent chooses** which tool to use automatically

---

## Quick Template

```python
from agents import function_tool

@function_tool
def tool_name(param1: str, param2: int) -> str:
    """
    What this tool does.
    
    Args:
        param1: Description of param1.
        param2: Description of param2.
    """
    # Your logic
    return result

# Add to agent
agent = Agent(
    name="...",
    tools=[tool_name]  # No parentheses!
)
```

**Next: Agent as a Tool (multi-agent systems)** 🤖➡️🤖

# Summary: Agent as a Tool in Agent SDK

## Concept: What is Agent as Tool?

**Using one agent as a tool for another agent**

```
User → Main Agent → Sub-Agent (as tool) → Result back to Main Agent → User
```

---

## Visual Example

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION AGENT                       │
│           "You are a translation agent..."                   │
│                                                              │
│   Tools:                                                     │
│   ┌─────────────────┐    ┌─────────────────┐                │
│   │  Spanish Agent  │    │  French Agent   │                │
│   │  (as tool)      │    │  (as tool)      │                │
│   │                 │    │                 │                │
│   │  Translates to  │    │  Translates to  │                │
│   │  Spanish        │    │  French         │                │
│   └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
           ↑
           │
        User: "Say hello in Spanish"
           │
           ↓
    Uses Spanish Agent tool → Returns translation
```

---

## Real-World Example: Physics + Math

```
┌─────────────────────────────────────────────────────────────┐
│                    PHYSICS AGENT                             │
│           Expert in physics concepts                         │
│                                                              │
│   Tools:                                                     │
│   ├── calculate_gravity()                                   │
│   ├── calculate_velocity()                                  │
│   └── MATH AGENT (as tool)  ←── For solving equations       │
│                                                              │
│       ┌─────────────────────────────────────────┐           │
│       │           MATH AGENT                     │           │
│       │   Tools: add(), subtract(), multiply()  │           │
│       └─────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────┘

User: "Solve this equation: 2x + 5 = 15"
  ↓
Physics Agent: "I'm not expert in math, let me use Math Agent"
  ↓
Math Agent: Uses its tools → Returns "x = 5"
  ↓
Physics Agent: Returns result to user
```

---

## Code Implementation

### Step 1: Create Sub-Agents

```python
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

# Spanish translation agent
spanish_agent = Agent(
    name="translate_to_spanish",
    instructions="You translate the user's message to Spanish"
)

# French translation agent  
french_agent = Agent(
    name="translate_to_french",
    instructions="You translate the user's message to French"
)
```

---

### Step 2: Create Orchestrator with Agents as Tools

```python
# Main orchestrator agent
orchestrator_agent = Agent(
    name="orchestrator",
    instructions="""
    You are a translation agent.
    You can use tools given to you to translate.
    If user asks for multiple translations, 
    you can call the relevant tools.
    """,
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translates text to Spanish"
        ),
        french_agent.as_tool(
            tool_name="translate_to_french", 
            tool_description="Translates text to French"
        )
    ]
)
```

---

### Step 3: Run the Agent

```python
# Run orchestrator
result = Runner.run_sync(
    agent=orchestrator_agent,
    input="Say hello, how are you? in Spanish"
)

print(result.final_output)
```

---

## Complete Code Example

```python
# agent_tool.py
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

# Sub-agent 1: Spanish translator
spanish_agent = Agent(
    name="translate_to_spanish",
    instructions="You translate the user's message to Spanish"
)

# Sub-agent 2: French translator
french_agent = Agent(
    name="translate_to_french",
    instructions="You translate the user's message to French"
)

# Main orchestrator agent
orchestrator_agent = Agent(
    name="orchestrator",
    instructions="""
    You are a translation agent.
    You can use tools given to you to translate.
    If user asks for multiple translations, 
    you can call the relevant tools.
    """,
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translates text to Spanish"
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translates text to French"
        )
    ]
)

# Run it
result = Runner.run_sync(
    agent=orchestrator_agent,
    input="Say hello, how are you? in Spanish"
)

print(result.final_output)

# View tool calls made
print(result.raw_responses)
```

---

## Output Examples

### Spanish Translation

**Input:**
```
Say hello, how are you? in Spanish
```

**Output:**
```
¡Hola! ¿Cómo estás?
```

**Tool Call Made:**
```python
{
    "function": "translate_to_spanish",
    "input": "hello, how are you?",
    "output": "¡Hola! ¿Cómo estás?"
}
```

---

### French Translation

**Input:**
```
Say hello, how are you? in French
```

**Output:**
```
Bonjour! Comment allez-vous?
```

**Tool Call Made:**
```python
{
    "function": "translate_to_french",
    "input": "hello, how are you?",
    "output": "Bonjour! Comment allez-vous?"
}
```

---

## The `.as_tool()` Method

### Syntax

```python
agent.as_tool(
    tool_name="name_for_tool",
    tool_description="What this tool does"
)
```

### Parameters

| Parameter | Purpose |
|-----------|---------|
| `tool_name` | Name used by orchestrator to call |
| `tool_description` | Helps orchestrator know when to use |

---

## Viewing Tool Calls

### Access Raw Responses

```python
result = Runner.run_sync(
    agent=orchestrator_agent,
    input="Translate to Spanish"
)

# See what tools were called
print(result.raw_responses)
```

### Raw Response Structure

```python
{
    "function_call": "translate_to_spanish",
    "call_id": "abc123",
    "input": "hello, how are you?",
    "output": "¡Hola! ¿Cómo estás?"
}
```

---

## Use Cases

### 1. Translation System

```python
orchestrator → spanish_agent (translate)
             → french_agent (translate)
             → german_agent (translate)
```

### 2. Customer Support

```python
support_agent → technical_agent (tech questions)
              → billing_agent (payment issues)
              → sales_agent (product info)
```

### 3. Education

```python
tutor_agent → math_agent (calculations)
            → physics_agent (physics concepts)
            → chemistry_agent (chemical formulas)
```

### 4. Research

```python
research_agent → data_agent (data analysis)
               → search_agent (web search)
               → summary_agent (summarization)
```

---

## How It Works Internally

```
1. User sends query to Orchestrator
         ↓
2. Orchestrator analyzes query
         ↓
3. Decides which sub-agent tool to use
         ↓
4. Calls sub-agent as tool
         ↓
5. Sub-agent processes and returns result
         ↓
6. Orchestrator receives result
         ↓
7. Orchestrator formats response
         ↓
8. Returns to user
```

---

## Multiple Translations Example

```python
# User asks for multiple translations
result = Runner.run_sync(
    agent=orchestrator_agent,
    input="Translate 'Good morning' to both Spanish and French"
)

# Orchestrator will call BOTH agents
# Tool calls:
# 1. translate_to_spanish("Good morning") → "Buenos días"
# 2. translate_to_french("Good morning") → "Bonjour"

# Final output includes both translations
```

---

## Key Points

### 1. Creating Sub-Agents

```python
sub_agent = Agent(
    name="sub_agent_name",
    instructions="What this agent does"
)
```

### 2. Converting to Tool

```python
sub_agent.as_tool(
    tool_name="tool_identifier",
    tool_description="When to use this tool"
)
```

### 3. Adding to Main Agent

```python
main_agent = Agent(
    name="orchestrator",
    instructions="...",
    tools=[
        sub_agent1.as_tool(...),
        sub_agent2.as_tool(...)
    ]
)
```

---

## Combining All Tool Types

```python
from agents import Agent, WebSearchTool, function_tool

@function_tool
def custom_function():
    """Custom logic"""
    pass

# Sub-agent
helper_agent = Agent(name="helper", instructions="...")

# Main agent with ALL tool types
main_agent = Agent(
    name="super_agent",
    instructions="Use available tools",
    tools=[
        WebSearchTool,                          # Hosted tool
        custom_function,                         # Function tool
        helper_agent.as_tool(                   # Agent as tool
            tool_name="helper",
            tool_description="For specific tasks"
        )
    ]
)
```

---

## Benefits of Agent as Tool

| Benefit | Description |
|---------|-------------|
| **Modularity** | Each agent handles specific domain |
| **Reusability** | Same agent usable by multiple orchestrators |
| **Scalability** | Add new specialist agents easily |
| **Separation** | Clean separation of concerns |
| **Maintenance** | Update one agent without affecting others |

---

## Quick Template

```python
from agents import Agent, Runner

# 1. Create specialist agents
agent_a = Agent(name="agent_a", instructions="Specializes in A")
agent_b = Agent(name="agent_b", instructions="Specializes in B")

# 2. Create orchestrator with agents as tools
orchestrator = Agent(
    name="orchestrator",
    instructions="Route queries to appropriate specialists",
    tools=[
        agent_a.as_tool(
            tool_name="handle_a",
            tool_description="Use for A-related queries"
        ),
        agent_b.as_tool(
            tool_name="handle_b", 
            tool_description="Use for B-related queries"
        )
    ]
)

# 3. Run
result = Runner.run_sync(
    agent=orchestrator,
    input="User query here"
)

print(result.final_output)
```

---

## Key Takeaways

1. **Agent can be tool** for another agent
2. **`.as_tool()`** method converts agent to tool
3. **Orchestrator** decides which sub-agent to use
4. **Modular design** - specialized agents for specific tasks
5. **Combine** with hosted tools and function tools
6. **View calls** via `result.raw_responses`

**Next: Handoffs between agents** 🤝



