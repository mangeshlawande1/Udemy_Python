# Prompt Styles (Bonus Section)

## What are Prompt Styles?
**Different formats/syntax for sending instructions to LLMs** - not what you say, but HOW you structure it.

---

## 1️⃣ ChatML (Chat Markup Language) ⭐

### Used by: OpenAI, Gemini, Claude
### Format: Array of objects with `role` + `content`

```python
messages = [
    {
        "role": "system",      # System prompt
        "content": "You are an AI expert in mathematics"
    },
    {
        "role": "user",        # User input
        "content": "What is 2+2?"
    },
    {
        "role": "assistant",   # Assistant's previous response
        "content": "4"
    }
]
```

**This is what we've been using!** 99% of the time, you'll use ChatML.

---

## 2️⃣ Alpaca Prompting

### Used by: Meta Llama, Alpaca models
### Format: Plain text with special headers

```
### Instruction:
You are an AI expert in mathematics.

### Input:
What is 2+2?

### Response:
```

**Structure:**
- `### Instruction:` = System prompt
- `### Input:` = User query  
- `### Response:` = (Left empty - LLM fills this)

**Example with CoT:**
```
### Instruction:
You are an AI expert assistant resolving user queries using chain of thought.
Your task is to think step-by-step.

### Input:
Write a code to add N numbers in JavaScript

### Response:
```

---

## 3️⃣ Instruct Prompting (Llama 2 Style)

### Used by: Llama 2, some open-source models
### Format: Special tokens with angle brackets

```
<s>[INST] <<SYS>>
You are an AI expert in mathematics.
<</SYS>>

What is 2+2? [/INST]
```

**Structure:**
- `<s>` = Beginning of text
- `[INST]` = Instruction wrapper
- `<<SYS>>` = System prompt
- `[/INST]` = End instruction (model responds here)

---

## Comparison Table:

| Style | Syntax | Used By | Popularity |
|-------|--------|---------|------------|
| **ChatML** | JSON objects | OpenAI, Gemini, Claude | ⭐⭐⭐⭐⭐ (99%) |
| **Alpaca** | Plain text headers | Meta Llama, Alpaca | ⭐⭐⭐ |
| **Instruct** | Special tokens | Llama 2 | ⭐⭐ |

---

## Converting Between Styles:

**Original (ChatML):**
```python
[
    {"role": "system", "content": "You are helpful"},
    {"role": "user", "content": "Hi"}
]
```

**→ Alpaca:**
```
### Instruction:
You are helpful

### Input:
Hi

### Response:
```

**→ Instruct:**
```
<s>[INST] <<SYS>>
You are helpful
<</SYS>>

Hi [/INST]
```

---

## Key Takeaways:

✅ **ChatML is the industry standard** - stick with it  
✅ **Different models need different formats**  
✅ **Most APIs (OpenAI, Gemini) handle formatting for you**  
✅ **Only matters when using raw/open-source models**  

## What We'll Use Going Forward:

```python
# ChatML - The one true format we'll use
messages = [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
]
```

**This section = bonus knowledge.** You don't need to memorize other formats unless working with specific open-source models!

