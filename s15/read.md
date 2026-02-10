# 🔑 **OpenAI API Setup - Quick Guide**

---

## 📋 **Step-by-Step Setup**

### **1️⃣ Create Account**

```
Visit: https://platform.openai.com

✓ Sign up with Google (or email)
✓ Click "Dashboard" after login
```

---

### **2️⃣ Add Credits ($5 minimum)**

```
Dashboard → Settings → Billing → Add Credits

⚠️ Important:
- NOT free to use
- Minimum: $5
- $5 is enough for entire course!
- Instructor used only few cents from $5
```

**How to add:**
1. Go to Settings
2. Click "Billing"
3. Click "Add Credits"
4. Enter $5 (minimum)
5. Link your card
6. Complete payment

---

### **3️⃣ Create API Key**

```
Dashboard → API Keys → Create New Secret Key

Steps:
1. Click "Create new secret key"
2. Name it (e.g., "Test API Key")
3. Copy the key immediately
4. Store it safely (you can't see it again!)
```

**Example API key format:**
```
sk-proj-abc123...xyz789
```

---

## 🛠️ **Optional Features (FYI)**

| Feature | What It Does |
|---------|-------------|
| **Playground** | Test prompts in browser |
| **Usage** | Monitor spending & token usage |
| **Chat Prompts** | Save/manage prompt templates |

---

## 💰 **Cost Breakdown**

```
✓ $5 minimum deposit
✓ Pay-per-use (very cheap)
✓ Track usage in Dashboard

Example costs:
- 1000 tokens (GPT-4): ~$0.03
- 1000 tokens (GPT-3.5): ~$0.002
```

---

## 🔐 **Security Tips**

```python
# ✅ DO: Use environment variables
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ❌ DON'T: Hardcode in code
api_key = "sk-proj-abc123..."  # Never do this!
```

**After copying key:**
1. Store in `.env` file
2. Add `.env` to `.gitignore`
3. Revoke key if accidentally exposed

---

## 📝 **Quick Checklist**

```
✅ Created OpenAI account
✅ Added $5 credit
✅ Created API key
✅ Copied and saved key securely
✅ Ready to code!
```

---

## 🚀 **Next: Use in Python**

```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

**That's it! You're ready to build AI agents!** 🎯



=====================================

# 🐍 **OpenAI API with Python - Step-by-Step**

---

## 📦 **1. Installation**

```bash
# Install OpenAI package
pip install openai

# Install python-dotenv (for .env file)
pip install python-dotenv

# Save dependencies
pip freeze > requirements.txt
```

---

## 🔑 **2. Create .env File**

Create a file named `.env` in your project root:

```env
OPENAI_API_KEY=sk-proj-your-api-key-here
```

⚠️ **Important:** 
- Exact variable name: `OPENAI_API_KEY`
- Never commit this file to Git!

---

## 📝 **3. Create main.py**

```python
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create OpenAI client (automatically reads OPENAI_API_KEY)
client = OpenAI()

# Make API call
response = client.chat.completions.create(
    model="gpt-4o",  # or "gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"
    messages=[
        {
            "role": "user",
            "content": "Hey, I am Piyush. Nice to meet you!"
        }
    ]
)

# Print response
print(response.choices[0].message.content)
```

---

## 🚀 **4. Run the Code**

```bash
python main.py
```

**Output:**
```
Nice to meet you, Piyush! How can I assist you today?
```

---

## 📂 **Project Structure**

```
hello_world/
├── .env                    # API key (DO NOT COMMIT!)
├── main.py                 # Your code
├── requirements.txt        # Dependencies
└── .gitignore             # Add .env here!
```

**.gitignore:**
```
.env
__pycache__/
*.pyc
```

---

## 🎯 **Available Models**

| Model | Use Case | Cost |
|-------|----------|------|
| `gpt-4o` | Best quality | $$ |
| `gpt-4o-mini` | Fast & cheap | $ |
| `gpt-4` | Previous flagship | $$$ |
| `gpt-3.5-turbo` | Fastest, cheapest | $ |

---

## 🔧 **Common Issues & Fixes**

### ❌ **Error: "API key must be set"**

**Problem:** `.env` file not loaded

**Solution:**
```python
from dotenv import load_dotenv
load_dotenv()  # Add this BEFORE creating client!
```

---

### ❌ **Error: "Module 'dotenv' not found"**

**Problem:** python-dotenv not installed

**Solution:**
```bash
pip install python-dotenv
```

---

## 💡 **Enhanced Example with Conversation**

```python
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# Multiple messages (conversation)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Python?"},
        {"role": "assistant", "content": "Python is a programming language."},
        {"role": "user", "content": "What can I build with it?"}
    ]
)

print(response.choices[0].message.content)
```

---

## 📊 **Understanding the Response**

```python
response = client.chat.completions.create(...)

# Full response object structure:
response.choices[0].message.content  # ← AI's text response
response.choices[0].message.role     # "assistant"
response.model                        # "gpt-4o"
response.usage.prompt_tokens         # Input tokens used
response.usage.completion_tokens     # Output tokens used
response.usage.total_tokens          # Total tokens
```

---

## 🎓 **Complete Working Code**

```python
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Verify API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file!")

# Create client
client = OpenAI(api_key=api_key)

# Make request
try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Hey there!"
            }
        ]
    )
    
    # Print response
    print(response.choices[0].message.content)
    
    # Print token usage
    print(f"\nTokens used: {response.usage.total_tokens}")
    
except Exception as e:
    print(f"Error: {e}")
```

---

## ✅ **Quick Checklist**

```
✅ Installed openai package
✅ Installed python-dotenv package
✅ Created .env file with OPENAI_API_KEY
✅ Added .env to .gitignore
✅ Loaded .env with load_dotenv()
✅ Created OpenAI client
✅ Made successful API call
```

---

## 🚀 **You're Ready!**

Now you can:
- Make API calls to OpenAI
- Build chatbots
- Create AI agents
- Integrate LLMs into your apps

**Next:** Learn about streaming, function calling, and agents! 🎯




# Using Gemini API (Free Alternative to OpenAI)

## Key Points:

**Why Gemini?**
- OpenAI API costs money (charges per token)
- Gemini API is **currently free** to use

## Setup Steps:

1. **Get API Key:**
   - Go to `aistudio.google.com`
   - Click "Get API key"
   - Create new API key (no billing required)

2. **Install Package:**
   ```bash
   pip install google-generativeai
   ```

3. **Basic Code:**
   ```python
   from google import genai
   
   # Create client with API key
   client = genai.Client(api_key="YOUR_API_KEY")
   
   # Generate content
   response = client.models.generate_content(
       model="gemini-pro",  # specify model
       contents="Explain how AI works in few words"
   )
   
   # Print response
   print(response.text)
   ```

**Result:** Works similar to OpenAI but completely free (for now)!


-====================================

# Using Gemini with OpenAI SDK

## Problem:
- Gemini has different syntax/code style than OpenAI
- Hard to follow OpenAI tutorials if using Gemini

## Solution: 
**Use Gemini through OpenAI's library!**

## How It Works:

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_GEMINI_API_KEY",  # Use Gemini key
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # Redirect to Google
)

response = client.chat.completions.create(
    model="gemini-1.5-flash",  # Use Gemini model (not GPT)
    messages=[{"role": "user", "content": "Who are you?"}]
)

print(response.choices[0].message.content)
# Output: "I'm a language model trained by Google"
```

## Key Changes:
1. ✅ Same OpenAI code structure
2. 🔑 Use Gemini API key
3. 🔗 Change `base_url` to Google's endpoint
4. 🤖 Change model name to Gemini models

## Benefits:
- Follow OpenAI tutorials while using **free** Gemini
- Same code syntax
- 99% compatibility

**Note:** Gemini is free now, but may become paid later. Minor issues (1%) may occur.