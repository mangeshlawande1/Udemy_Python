# What is Prompting?

## The Problem:
Without instructions, LLM answers **anything** - science, jokes, math, coding, etc. It's uncontrolled and unpredictable.

## The Solution: System Prompts
A **system prompt** = Special instructions that control the chatbot's behavior

---

## Example Code:

### ❌ Without System Prompt (Uncontrolled):
```python
messages = [
    {"role": "user", "content": "Who are you?"}
]
# LLM can answer anything!
```

### ✅ With System Prompt (Controlled):
```python
messages = [
    {
        "role": "system", 
        "content": "You are an expert in maths and only answer maths related questions."
    },
    {"role": "user", "content": "Can you code a Python program?"}
]

# Response: "Sorry, I can only answer math questions"
```

### ✅ Stricter System Prompt:
```python
{
    "role": "system",
    "content": "You are a math expert. If query is not related to maths, just say sorry and do not answer."
}
```

---

## Test Results:

| Question | Response |
|----------|----------|
| "Code Python program" | ❌ "Sorry, I only answer math questions" |
| "Solve (a+b)²" | ✅ *Provides solution* |

---

## Why It Matters:
- **Sets context** and boundaries
- **Controls** what LLM can/cannot do
- **Critical for building reliable AI agents**

**Next:** Learn different types of prompting techniques to improve accuracy!


=======================================

# Zero-Shot Prompting

## Definition:
**Directly giving instructions to the model WITHOUT any examples.**

---

## Code Example:

```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_KEY", base_url="GEMINI_URL")

# Zero-shot prompt - Direct instructions, no examples
system_prompt = """
You should only and only answer coding related questions.
Do not answer anything else.
Your name is Alexa.
If user asks something other than coding, just say sorry.
"""

response = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Can you tell me a joke?"}
    ]
)

print(response.choices[0].message.content)
```

---

## Test Results:

| User Question | Response |
|---------------|----------|
| "Tell me a joke" | ❌ "Sorry" |
| "Translate 'hello' to Hindi" | ❌ "Sorry" |
| "Write Python code to translate" | ✅ *Provides code* |

---

## Key Points:
- ✅ **Direct instructions** - No examples needed
- ✅ **Simple and clear** - Just tell what to do
- ✅ **Works well** for straightforward tasks
- 🎯 Model follows rules based purely on written instructions

**Next:** Few-shot prompting (giving examples to improve performance)

============================================

# Few-Shot Prompting

## Definition:
**Providing examples along with instructions to improve accuracy and control output format.**

---

## Part 1: Basic Few-Shot Prompting

```python
system_prompt = """
You should only answer coding related questions.
Your name is Alexa.

EXAMPLES:

Question: Can you explain A + B whole square?
Answer: Sorry, I can only help with coding related questions.

Question: Write a code in Python for adding two numbers.
Answer: 
def add(a, b):
    return a + b

Question: What is the capital of France?
Answer: Sorry, I can only help with coding related questions.
"""
```

### Results:
- "Explain A+B whole square" → ❌ "Sorry, coding questions only"
- "Write Python code to add" → ✅ Provides code

---

## Part 2: **Structuring Output with Few-Shot** (Advanced)

### Problem:
Output is unstructured markdown - hard to parse programmatically.

### Solution:
Use few-shot to enforce **JSON format**:

```python
system_prompt = """
You are a coding assistant.

RULE 1: Strictly follow output in JSON format.

OUTPUT FORMAT:
{
    "code": "string or null",
    "is_coding_question": boolean
}

EXAMPLES:

Question: Can you explain A + B whole square?
Answer: {"code": null, "is_coding_question": false}

Question: Write code to add two numbers in Python
Answer: {
    "code": "def add(a, b):\n    return a + b",
    "is_coding_question": true
}
"""
```

### Results:

| Question | Output |
|----------|--------|
| "Explain A+B²" | `{"code": null, "is_coding_question": false}` |
| "Add N numbers in JS" | `{"code": "function add(arr) {...}", "is_coding_question": true}` |

---

## Key Benefits:

✅ **50x better accuracy** with 50-60 examples  
✅ **Structured output** (JSON, XML, etc.)  
✅ **Easier parsing** - use `response.code` directly  
✅ **Most commonly used** in real-world applications

**Tip:** Examples can grow over time to improve quality!


==============================================


# Chain of Thought (CoT) Prompting

## What is CoT?
**Making the LLM "think" step-by-step before answering** - like how humans solve problems.

### Used in:
- DeepSeek models
- OpenAI O3 models
- Any AI that needs to "reason"

---

## How It Works:

### System Prompt Structure:

```python
system_prompt = """
You are an expert AI assistant in resolving user queries using chain of thought.

You work on START → THINK → PLAN → OUTPUT steps.

RULES:
1. Strictly follow the given JSON output format
2. Only run one step at a time
3. Sequence: START (user input) → PLAN (multiple times) → OUTPUT (final answer)

OUTPUT JSON FORMAT:
{
    "step": "start" | "plan" | "output",
    "content": "string"
}

EXAMPLE:
Question: Can you solve 2 + 3 * 5 / 10?

Answer Step 1: {"step": "plan", "content": "User is interested in math problem"}
Answer Step 2: {"step": "plan", "content": "Should solve using BODMAS method"}
Answer Step 3: {"step": "plan", "content": "First multiply: 3 * 5 = 15"}
Answer Step 4: {"step": "plan", "content": "New equation: 2 + 15 / 10"}
Answer Step 5: {"step": "plan", "content": "Divide: 15 / 10 = 1.5"}
Answer Step 6: {"step": "plan", "content": "New equation: 2 + 1.5"}
Answer Step 7: {"step": "plan", "content": "Add: 2 + 1.5 = 3.5"}
Answer Step 8: {"step": "plan", "content": "Solved! Answer is 3.5"}
Answer Step 9: {"step": "output", "content": "3.5"}
"""
```

---

## Code Example:

```python
import json
from openai import OpenAI

client = OpenAI(...)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Write code to add N numbers in JavaScript"}
]

# First call
response = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=messages,
    response_format={"type": "json_object"}  # Force JSON output
)

# Response 1: {"step": "start", "content": "User wants JS code to add N numbers"}

# Add assistant's response to history
messages.append({"role": "assistant", "content": response.choices[0].message.content})

# Call again - it continues thinking
# Response 2: {"step": "plan", "content": "Need to define function accepting arbitrary arguments"}
# Response 3: {"step": "plan", "content": "Will use rest parameter ..."}
# ...
# Final: {"step": "output", "content": "function add(...nums) { return nums.reduce(...) }"}
```

---

## Multi-Step Thinking Process:

```
User: "Write code to add N numbers in JS"

Step 1 (start): "User wants JS code to add N numbers"
Step 2 (plan): "Need function with arbitrary arguments"
Step 3 (plan): "Will use rest parameter syntax"
Step 4 (plan): "Use reduce() to sum array"
Step 5 (output): 
    function add(...numbers) {
        return numbers.reduce((sum, num) => sum + num, 0);
    }
```

---

## Key Points:

✅ **Increases accuracy** - AI thinks before acting  
✅ **Transparent reasoning** - See the thought process  
✅ **Better for complex tasks** - Math, coding, logic  
✅ **Requires multiple API calls** - Each thinking step is separate  

## Challenge:
Currently **manually appending** each response to message history.

**Next video:** Automate the thinking loop!
=======================================

# Automating Chain of Thought (CoT)

## Problem:
Previously, we **manually** added each response to message history. Now let's **automate** it!

---

## Automated CoT Code:

```python
import json
from openai import OpenAI

client = OpenAI()  # Reads API key from environment

# System prompt with CoT instructions (same as before)
system_prompt = """
You are an expert AI assistant using chain of thought.
Work on START → PLAN → OUTPUT steps.
...
"""

# Initialize message history
message_history = [
    {"role": "system", "content": system_prompt}
]

# Get user input
user_query = input("🧑 Type something: ")
message_history.append({"role": "user", "content": user_query})

# Automated thinking loop
while True:
    # Call LLM
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=message_history,
        response_format={"type": "json_object"}
    )
    
    # Get raw result
    raw_result = response.choices[0].message.content
    
    # Parse JSON
    parsed_result = json.loads(raw_result)
    
    # Add to history
    message_history.append({
        "role": "assistant",
        "content": raw_result
    })
    
    # Handle different steps
    step = parsed_result.get("step")
    content = parsed_result.get("content")
    
    if step == "start":
        print(f"🔥 {content}")
        continue
    
    elif step == "plan":
        print(f"🧠 {content}")  # Show thinking process
        continue
    
    elif step == "output":
        print(f"🤖 {content}")  # Final answer
        break  # Exit loop
```

---

## Example Output:

**User Input:**
```
Can you solve 2 + 3 / 10 * 6 * 4 / 1 - 50?
```

**Automated Thinking:**
```
🔥 User wants to solve mathematical expression
🧠 Expression is: 2 + 3 / 10 * 6 * 4 / 1 - 50
🧠 Apply BODMAS: First division 3/10 = 0.3
🧠 Next multiplication: 0.3 * 6 = 1.8
🧠 Continue multiplication: 1.8 * 4 = 7.2
🧠 Division: 7.2 / 1 = 7.2
🧠 Addition: 2 + 7.2 = 9.2
🧠 Subtraction: 9.2 - 50 = -40.8
🤖 -40.8
```

---

## Code Example 2:

**User Input:**
```
Write JavaScript code to add N arguments as fast as possible with caching
```

**Output:**
```
🔥 Need to write efficient JS function with caching
🧠 Use rest parameter to accept N arguments
🧠 Implement memoization for caching
🧠 Use Map for O(1) lookup
🤖 
function add(...nums) {
    const cache = new Map();
    const key = nums.join(',');
    if (cache.has(key)) return cache.get(key);
    const sum = nums.reduce((a, b) => a + b, 0);
    cache.set(key, sum);
    return sum;
}
```

---

## How It Works:

1. **Initialize:** Start with system prompt
2. **User input:** Add to message history
3. **Loop:** Call LLM repeatedly
4. **Append:** Add each response to history
5. **Display:** 
   - 🔥 = Start
   - 🧠 = Thinking/Planning
   - 🤖 = Final output
6. **Break:** Stop when step = "output"

---

## Key Points:

✅ **Fully automated** - No manual message adding  
✅ **Continuous thinking** - LLM plans multiple steps  
✅ **Transparent** - See the reasoning process  
✅ **Better accuracy** - Thinks before answering  
✅ **Works with any complex task** - Math, coding, logic  

**Note:** Works best with **GPT-4** or similar models. Gemini may have JSON parsing issues.


===================================================

# Persona-Based Prompting

## What is it?
**Making AI mimic someone's personality, tone, and speaking style** by providing detailed background and examples.

---

## Code Example:

```python
from openai import OpenAI

client = OpenAI()

# Persona-based system prompt
system_prompt = """
You are an AI assistant named Piyush Garg.

BACKGROUND:
- 25 years old
- Tech enthusiast
- Principal Engineer
- Main tech stack: JavaScript and Python
- Currently learning GenAI

SPEAKING STYLE EXAMPLES:

Example 1:
User: "Hey"
You: "Hey, what's up! How can I assist you today?"

Example 2:
User: "What do you think about React?"
You: "React is awesome! I've been using it for years. The component model just makes sense, you know?"

Example 3:
User: "Can you help with Python?"
You: "Of course! Python is my jam. What do you need help with?"

[Add 50-100 more examples showing tone, vocabulary, humor, etc.]
"""

# Chat with persona
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Who are you?"}
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages
)

print(response.choices[0].message.content)
# Output: "Hey! I'm Piyush Garg, your personal AI assistant..."
```

---

## How to Build a Good Persona:

### 1. **Background Information:**
```
- Age, profession, location
- Interests, hobbies
- Education, experience
- Current projects
```

### 2. **Examples (Most Important!):**
Get 100-150 examples from:
- 💬 WhatsApp/chat history
- 🐦 Twitter/LinkedIn comments
- 📝 Emails, blog posts
- 🎤 Interview transcripts

### 3. **Speaking Patterns:**
```
- Vocabulary choices
- Sentence structure
- Humor style
- Common phrases
- Emojis used
- Tone (formal/casual)
```

---

## Real Example - Creating Girlfriend/Boyfriend Clone:

```python
system_prompt = """
You are Sarah, my girlfriend.

BACKGROUND:
- 24 years old, graphic designer
- Loves coffee, hates mornings
- Calls me "babe" often
- Uses lots of emojis

EXAMPLES:

User: "Good morning!"
You: "Ugh morning already? ☕😴 Need coffee first babe"

User: "How was work?"
You: "Omg so exhausting! Client changed everything AGAIN 🙄 How was yours? 💕"

User: "Miss you"
You: "Aww miss you too babe! 🥺❤️ Can't wait to see you"

[100+ more examples...]
"""
```

---

## Test Results:

| Question | Response |
|----------|----------|
| "Who are you?" | "Hey! I'm Piyush Garg, your personal AI assistant..." |
| "What's up?" | "What's up! How can I assist you today?" |
| Generic greeting | Responds in persona's typical style |

---

## Challenge Assignment:

**Create your best friend's persona:**

1. ✅ Gather chat history (WhatsApp, Discord, etc.)
2. ✅ Write detailed background
3. ✅ Add 100-150 conversation examples
4. ✅ Include their:
   - Common phrases
   - Emojis/slang
   - Topics they talk about
   - Humor style
5. ✅ Test and refine

---

## Key Success Factors:

📊 **Quality > Quantity in examples**
- Show variety of situations
- Include emotional responses
- Capture unique phrases

🎯 **The more examples, the better accuracy**
- 10 examples = Basic mimicry
- 50 examples = Good resemblance  
- 100+ examples = Convincing clone

💡 **Update over time**
- Add new examples as you chat
- Refine based on what sounds "off"

---

## Important Notes:

⚠️ **Privacy:** Only use chat data you have permission to use  
⚠️ **Ethics:** Don't impersonate real people maliciously  
✅ **Use cases:** Customer support bots, personal assistants, educational tools

**Bottom line:** Persona prompting is all about **detailed background + tons of examples!**



