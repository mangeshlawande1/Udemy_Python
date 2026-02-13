# Prompt Engineering & Logic: A Complete Guide

Let me break down these powerful techniques in a way that's easy to understand and apply.

---

## What is Prompt Engineering?

**Prompt Engineering** = The art and science of communicating with AI to get the best possible results.

```
┌─────────────────────────────────────────────────────────┐
│                    Think of it like:                    │
│                                                         │
│  Bad Prompt  = Mumbling unclear instructions            │
│  Good Prompt = Clear, detailed, specific guidance       │
└─────────────────────────────────────────────────────────┘
```

---

## 1. Chain-of-Thought (CoT) Prompting

### What is CoT?

Instead of asking the AI to jump straight to an answer, you ask it to **think step-by-step** — just like showing your work in math class.

### Visual Comparison

```
WITHOUT CoT (Direct Answer)
┌──────────────────────────────────────┐
│ Q: "What is 23 × 17?"                │
│                                      │
│ A: "391"                             │
│    ↑ Could be right or wrong         │
│    ↑ No way to verify the logic      │
└──────────────────────────────────────┘

WITH CoT (Step-by-Step)
┌──────────────────────────────────────┐
│ Q: "What is 23 × 17? Let's think     │
│     step by step."                   │
│                                      │
│ A: "Let me break this down:          │
│    Step 1: 23 × 10 = 230             │
│    Step 2: 23 × 7 = 161              │
│    Step 3: 230 + 161 = 391           │
│    Answer: 391"                      │
│    ↑ Shows reasoning                 │
│    ↑ Can spot errors in logic        │
└──────────────────────────────────────┘
```

---

### CoT Techniques

#### **1. Zero-Shot CoT (Simplest)**

Just add "Let's think step by step" to your prompt!

```
❌ BAD:
"Is 97 a prime number?"

✅ GOOD:
"Is 97 a prime number? Let's think step by step."

RESPONSE:
"Let me check:
Step 1: Check if divisible by 2 → 97 is odd, so no
Step 2: Check if divisible by 3 → 9+7=16, not divisible by 3
Step 3: Check if divisible by 5 → Doesn't end in 0 or 5
Step 4: Check if divisible by 7 → 97÷7=13.8... no
Step 5: Check up to √97 ≈ 9.8
Step 6: No divisors found
Answer: Yes, 97 is prime."
```

#### **2. Few-Shot CoT (With Examples)**

Show the AI examples of the thinking process you want.

```
PROMPT:
"Solve these word problems:

Example 1:
Q: Roger has 5 tennis balls. He buys 2 more cans of 
   tennis balls. Each can has 3 balls. How many does he have?
A: Let me think step-by-step:
   - Started with: 5 balls
   - Bought: 2 cans × 3 balls = 6 balls
   - Total: 5 + 6 = 11 balls
   Answer: 11 balls

Example 2:
Q: The cafeteria had 23 apples. If they used 20 to make 
   lunch and bought 6 more, how many do they have?
A: Let me think step-by-step:
   - Started with: 23 apples
   - Used: -20 apples
   - Remaining: 23 - 20 = 3 apples
   - Bought: +6 apples
   - Total: 3 + 6 = 9 apples
   Answer: 9 apples

Now solve this:
Q: Sarah has 12 cookies. She gives 5 to her friend and 
   bakes 8 more. How many cookies does Sarah have?"

RESPONSE:
"A: Let me think step-by-step:
   - Started with: 12 cookies
   - Gave away: -5 cookies
   - Remaining: 12 - 5 = 7 cookies
   - Baked: +8 cookies
   - Total: 7 + 8 = 15 cookies
   Answer: 15 cookies"
```

#### **3. Structured CoT (With Framework)**

Provide a specific reasoning framework.

```
PROMPT:
"Analyze this business decision using this framework:

1. SITUATION: What's the current state?
2. OPTIONS: What are the choices?
3. PROS/CONS: Evaluate each option
4. RECOMMENDATION: What should we do?
5. REASONING: Why?

Decision: Should we expand to a new city or improve 
existing stores?

Think through this step-by-step."

RESPONSE:
"1. SITUATION:
   - Current: 5 stores in City A, revenue plateauing
   - Resources: $500K budget, 2-year timeline

2. OPTIONS:
   A) Expand to City B (3 new stores)
   B) Renovate existing 5 stores

3. PROS/CONS:
   Option A:
   ✓ New market access
   ✓ Revenue diversification
   ✗ Higher risk
   ✗ Split management focus
   
   Option B:
   ✓ Strengthen existing market
   ✓ Lower risk
   ✗ Limited growth potential
   ✗ Still dependent on one city

4. RECOMMENDATION: Option A (Expand)

5. REASONING:
   - Plateau suggests market saturation in City A
   - Diversification reduces risk long-term
   - $500K is sufficient for cautious expansion
   - Can test market with 1-2 stores initially"
```

---

### Complex CoT Patterns

#### **Tree of Thought (ToT)**

Explore multiple reasoning paths simultaneously.

```
PROMPT:
"Solve this puzzle by exploring different approaches:

Puzzle: You have a 3-liter jug and a 5-liter jug. 
How do you measure exactly 4 liters?

Explore 3 different solution paths."

RESPONSE:
"Path 1: Fill 5L, pour into 3L
- 5L jug: 5 liters
- Pour to 3L: 5L jug now has 2 liters
- Empty 3L, pour 2L into it
- Fill 5L again
- Pour from 5L to fill 3L (needs 1L)
- Result: 5L jug has 4 liters ✓

Path 2: Fill 3L repeatedly
- Fill 3L, pour into 5L (5L has 3)
- Fill 3L again, pour into 5L (5L has 5, 3L has 1)
- Empty 5L, pour 1L from 3L
- Fill 3L, pour into 5L
- Result: 5L jug has 4 liters ✓

Path 3: Work backwards
- Target: 4L in 5L jug
- 4 = 5 - 1, so need to remove 1L
- How to get 1L? 3 - 2 = 1
- How to get 2L? Fill 5L, pour out 3L
[continues reasoning...]

Best path: Path 1 (fewest steps)"
```

---

## 2. Role-Based Instructions

### What Are Roles?

Assigning the AI a specific **persona, expertise, or perspective** to guide its responses.

### Basic Structure

```
┌────────────────────────────────────────────────────────┐
│  "You are a [ROLE] with [EXPERTISE].                  │
│   Your task is to [OBJECTIVE].                        │
│   You should [BEHAVIOR/STYLE]."                       │
└────────────────────────────────────────────────────────┘
```

---

### Role Examples by Use Case

#### **Example 1: Technical Expert**

```
❌ GENERIC PROMPT:
"Explain neural networks"

✅ ROLE-BASED PROMPT:
"You are a senior machine learning engineer with 10 years 
of experience teaching beginners. Explain neural networks 
to someone who understands basic programming but has no 
AI background. Use analogies and simple diagrams."

RESULT: More accessible, tailored explanation
```

#### **Example 2: Critical Analyst**

```
PROMPT:
"You are a skeptical financial analyst who questions 
assumptions and looks for risks. Review this investment 
proposal and identify potential red flags:

[Investment proposal text]

Be thorough and critical in your analysis."

RESPONSE:
"⚠️ RED FLAGS IDENTIFIED:

1. Revenue Projections:
   - Claims 300% growth in Year 2
   - No clear explanation of customer acquisition strategy
   - Industry average is 50-70%
   - RISK: Unrealistic expectations

2. Market Analysis:
   - States 'huge market potential' without data
   - No competitive analysis provided
   - RISK: Market may be saturated

[continues with detailed critical analysis...]"
```

#### **Example 3: Creative Professional**

```
PROMPT:
"You are an award-winning children's book author known 
for imaginative storytelling and teaching moral lessons. 
Write a short story about honesty for 6-8 year olds. 
Use simple words, vivid imagery, and a memorable lesson."

RESPONSE:
"THE MAGIC PAINTBRUSH

Once upon a time, in a village painted with rainbows, 
lived a young fox named Finn..."
[Story follows in appropriate style and language]
```

---

### Advanced Role Techniques

#### **1. Multi-Role Framework**

```
PROMPT:
"Analyze this product idea from three perspectives:

👔 ROLE 1: Cautious CEO
Focus on: Risk, costs, timeline

🎨 ROLE 2: Creative Designer  
Focus on: User experience, innovation

💰 ROLE 3: Sales Director
Focus on: Market fit, revenue potential

Product: AI-powered meal planning app with grocery 
delivery integration"

RESPONSE:
"👔 CEO PERSPECTIVE:
Risks:
- High development cost ($200K-500K)
- Crowded market (MyFitnessPal, Yummly)
- Grocery API dependencies...

🎨 DESIGNER PERSPECTIVE:
Opportunities:
- Personalization is key differentiator
- Voice interface for hands-free cooking
- AR features to visualize portions...

💰 SALES PERSPECTIVE:
Market Analysis:
- $10B meal kit market growing 15% annually
- Premium subscription model: $9.99/month
- B2B opportunity with gyms/wellness..."
```

#### **2. Dynamic Role Adaptation**

```
PROMPT:
"You are a tutor who adapts their teaching style based on 
the student's responses. Start by explaining photosynthesis. 
If I seem confused, simplify. If I ask advanced questions, 
go deeper."

[Conversation evolves based on student's level]

Student: "I don't get it"
Tutor: [Simplifies to elementary level]

Student: "What about the Calvin cycle?"
Tutor: [Shifts to advanced biochemistry]
```

---

## 3. Combining CoT + Roles

### The Power Combo

```
PROMPT:
"You are a detective investigating a crime scene. 
Use chain-of-thought reasoning to analyze this evidence.

Evidence:
- Window broken from outside
- No valuables taken
- Fresh footprints leading to garden
- Dog didn't bark

Think through this step-by-step like a detective would."

RESPONSE:
"🔍 DETECTIVE ANALYSIS:

Step 1 - Scene Assessment:
The broken window suggests forced entry, but let's not 
jump to conclusions. I'll examine each piece of evidence.

Step 2 - The Window:
- Broken from OUTSIDE
- Glass shards inside the room
- Initial thought: Burglary
- But wait... why no valuables taken?

Step 3 - Missing Valuables:
- TV, jewelry untouched
- This is unusual for burglary
- Alternative theory: Someone wanted IN, not valuables

Step 4 - The Footprints:
- LEAD TO garden (not away from house)
- Suggests someone went TO garden AFTER entering
- Possible hiding something? Meeting someone?

Step 5 - The Silent Dog:
⚠️ CRITICAL CLUE
- Dogs bark at strangers
- Dog didn't bark
- Conclusion: The intruder was KNOWN to the dog

THEORY: This wasn't a burglary. Someone the dog knew 
broke in (or staged a break-in) to access the garden. 
Possible scenarios:
1. Family member locked out
2. Someone hiding something in garden
3. Staged break-in to cover something else

Next steps: Interview household members, search garden, 
check who had access to the property."
```

---

## Practical Prompt Engineering Patterns

### Pattern 1: The "Expert Persona" Template

```
You are [SPECIFIC ROLE] with expertise in [DOMAIN].

Your characteristics:
- [TRAIT 1]
- [TRAIT 2]
- [TRAIT 3]

Your task: [CLEAR OBJECTIVE]

Approach: [METHODOLOGY]

Constraints:
- [LIMITATION 1]
- [LIMITATION 2]

Output format: [STRUCTURE]
```

**Example Application:**

```
You are a pediatric nutritionist with 15 years of experience.

Your characteristics:
- Evidence-based recommendations
- Sensitive to cultural food preferences
- Practical, budget-conscious advice

Your task: Create a one-week meal plan for a picky 
3-year-old who refuses vegetables.

Approach: Use "food chaining" and creative presentation 
techniques. Think step-by-step about nutritional needs, 
then design meals that hide or transform vegetables.

Constraints:
- Budget: $50/week
- No specialty stores
- 30-minute max prep time per meal

Output format: Day-by-day meal plan with prep tips
```

---

### Pattern 2: The "Reasoning Chain" Template

```
Let's solve this step-by-step:

1. UNDERSTAND: What is being asked?
2. GATHER: What information do we have?
3. ANALYZE: What patterns or relationships exist?
4. EXPLORE: What are possible approaches?
5. SOLVE: Execute the best approach
6. VERIFY: Does this make sense?
```

**Example Application:**

```
PROBLEM: "Our website traffic dropped 40% last month. 
What happened?"

Let's solve this step-by-step:

1. UNDERSTAND:
   - Need to identify cause of 40% traffic drop
   - Timeframe: Last month
   - Metric: Website traffic

2. GATHER:
   - What changed last month?
   - Check: Content, SEO, technical issues, seasonality
   - Need: Analytics data, update logs, industry trends

3. ANALYZE:
   [AI would continue with systematic analysis...]
```

---

### Pattern 3: The "Multi-Perspective" Template

```
Analyze [TOPIC] from these angles:

🔍 Analytical: What does the data say?
❤️ Emotional: How do people feel?
⚖️ Ethical: What's right/wrong?
💼 Practical: What's realistic?
🔮 Future: What are long-term effects?
```

---

## Common Prompt Engineering Mistakes

```
┌────────────────────────────────────────────────────────┐
│                ❌ MISTAKES vs ✅ FIXES                 │
├────────────────────────────────────────────────────────┤
│                                                        │
│ ❌ "Tell me about marketing"                           │
│ ✅ "You are a B2B SaaS marketing expert. Explain       │
│    the 3 most effective lead generation strategies     │
│    for enterprise software in 2024. Use data and       │
│    examples."                                          │
│                                                        │
│ ❌ "Is this a good idea?"                              │
│ ✅ "Evaluate this idea using: 1) Market viability,     │
│    2) Technical feasibility, 3) Financial projections. │
│    Think step-by-step."                                │
│                                                        │
│ ❌ "Make it better"                                    │
│ ✅ "You are an editor. Improve this for clarity and    │
│    engagement. Focus on: removing jargon, adding       │
│    examples, shortening sentences."                    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## Quick Reference: Prompt Engineering Toolkit

```
┌─────────────────────────────────────────────────────────┐
│              PROMPT ENGINEERING CHEAT SHEET             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 🧠 FOR COMPLEX REASONING:                               │
│    → Add "Let's think step-by-step"                     │
│    → Show examples of desired reasoning                 │
│    → Ask for verification of logic                      │
│                                                         │
│ 🎭 FOR BETTER RESPONSES:                                │
│    → Assign specific expert role                        │
│    → Define expertise level                             │
│    → Specify output style/format                        │
│                                                         │
│ 🎯 FOR ACCURACY:                                        │
│    → Be specific about what you want                    │
│    → Provide constraints and requirements               │
│    → Ask for sources or reasoning                       │
│                                                         │
│ 🔧 FOR STRUCTURED OUTPUT:                               │
│    → Specify exact format needed                        │
│    → Use frameworks (SWOT, 5W1H, etc.)                  │
│    → Number steps or sections                           │
│                                                         │
│ ⚡ POWER PHRASES:                                       │
│    • "Explain like I'm [age/profession]"                │
│    • "Show your work"                                   │
│    • "What assumptions are you making?"                 │
│    • "Consider alternative viewpoints"                  │
│    • "Verify this conclusion"                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

Would you like me to dive deeper into **specific prompting techniques** (like few-shot learning, prompt chaining, or constitutional AI), or explore **advanced applications** for your particular use case?