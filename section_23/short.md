# Multimodal AI - Introduction

## Important Distinction

### ❌ Multi-Model (with "e")
- Multiple AI models working together
- Different concept entirely

### ✅ Multimodal (with "a")
- **Single AI model** that accepts **multiple types of input**
- Text, images, audio, video
- **This is what we're learning!**

---

## What is Multimodal AI?

**Multimodal AI** = AI systems that process and integrate information from multiple data types:
- 📝 Text
- 🖼️ Images
- 🎵 Audio
- 🎥 Video

---

## Example: Text-Only vs Multimodal

### GPT-3.5 Turbo (Text-Only)
```
Input:  Text only
Output: Text only
```

### GPT-4o-mini (Multimodal)
```
Input:  Text + Images
Output: Text
```

---

## Code Comparison

### Text-Only Input (Traditional)
```python
messages=[
    {
        "role": "user",
        "content": "What is in this image?"  # Just text
    }
]
```

### Multimodal Input (Image + Text)
```python
messages=[
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What is in this image?"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://example.com/image.jpg"
                }
            }
        ]
    }
]
```

---

## OpenAI Model Capabilities

| Model | Text Input | Image Input | Audio Input | Text Output |
|-------|-----------|-------------|-------------|-------------|
| GPT-3.5 Turbo | ✅ | ❌ | ❌ | ✅ |
| GPT-4o-mini | ✅ | ✅ | ❌ | ✅ |
| GPT-4o | ✅ | ✅ | ✅ | ✅ |

---

## Key Takeaway

**Multimodal = Multiple Input Types**

The model can "see" images, "hear" audio, and "read" text to generate responses!

**Next: Coding image analysis with GPT-4o!** 📸

# Coding a Multimodal Image Caption Agent

## Project Structure

```
image/
├── .env
└── main.py
```

---

## Complete Code: `main.py`

```python
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI()

# Make multimodal API call
response = client.chat.completions.create(
    model="gpt-4o",  # Must be multimodal model!
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Generate a caption for this image in about 50 words."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://images.pexels.com/photos/..."  # Your image URL
                    }
                }
            ]
        }
    ]
)

# Print the response
print(response.choices[0].message.content)
```

---

## Environment File: `.env`

```
OPENAI_API_KEY=your_api_key_here
```

---

## Run the Code

```bash
cd image
python main.py
```

---

## Example Output

```
"A cheerful young man proudly holds up a sticky note 
with the word 'code' written on it, emphasizing his 
passion for programming."
```

**The model "sees" the image and describes it!**

---

## Two Ways to Pass Images

### Option 1: Public URL
```python
{
    "type": "image_url",
    "image_url": {
        "url": "https://example.com/image.jpg"
    }
}
```

### Option 2: Base64 Encoded (Local Files)
```python
import base64

# Read and encode local image
with open("image.jpg", "rb") as f:
    base64_image = base64.b64encode(f.read()).decode()

{
    "type": "image_url",
    "image_url": {
        "url": f"data:image/jpeg;base64,{base64_image}"
    }
}
```

---

## Key Points

| Aspect | Detail |
|--------|--------|
| **Model** | Must support images (GPT-4o, GPT-4o-mini) |
| **Content** | Array of multiple types |
| **Image Source** | URL or Base64 encoded |
| **Response** | Text description/analysis |

---

## Content Array Structure

```python
content = [
    {"type": "text", "text": "Your prompt here"},
    {"type": "image_url", "image_url": {"url": "..."}},
    # Can add more images!
    {"type": "image_url", "image_url": {"url": "..."}}
]
```

---

## Summary

**Multimodal AI allows:**
- 📝 Text input
- 🖼️ Image input (URL or Base64)
- 🎵 Audio input (supported models)
- Combined analysis across modalities

**Next: Explore audio and more multimodal capabilities!** 🎉

