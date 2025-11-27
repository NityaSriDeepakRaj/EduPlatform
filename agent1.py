import json
from groq import Groq

# ---------------------------
# 1) SYSTEM PROMPT (IMPORTANT)
# ---------------------------
SYSTEM_PROMPT = """
You are Agent 1: The Interpreter.

Your job is to convert a user's natural-language request into a structured JSON
that describes what animation should be generated.

STRICT RULES:
- Output ONLY a JSON. No explanations.
- Follow the exact schema.
- DO NOT generate nested objects or dictionaries inside "objects" or "actions".
- DO NOT generate attributes like color, length, direction, position, etc.
- "objects" must be a list of simple strings ONLY.
- "actions" must be simple strings ONLY.
- "details" must be a simple dictionary with minimal info (numbers only if required).
- Keep JSON short and high level.
- Infer only basic missing details; do NOT over-specify.
- scene_count must be 1–3.
- style must be one of: "simple", "diagram", "graph", "algorithm".

ALLOWED object names:
"circle", "triangle", "square", "vector_a", "vector_b", "resultant",
"arrow", "bars", "graph", "function", "line", "point"

ALLOWED actions:
"draw", "move", "grow", "highlight", "rotate", "swap"

SCHEMA:
{
  "concept": "",
  "goal": "",
  "objects": [],
  "actions": [],
  "details": {},
  "scene_count": 1,
  "style": "simple"
}
"""

# ---------------------------
# 2) Initialize Groq Client
# ---------------------------
#client = Groq(api_key="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")


# ---------------------------
# 3) Main Agent-1 Function
# ---------------------------
def agent1_interpret(user_text: str):
    prompt = SYSTEM_PROMPT + f"\nUser: {user_text}\nOutput JSON:"

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        temperature=0.1
    )

    raw_output = response.choices[0].message.content

    cleaned = (
        raw_output.strip()
        .replace("json", "")
        .replace("", "")
    )

    try:
        parsed = json.loads(cleaned)
        return parsed
    except Exception:
        print("\n[Agent-1 WARNING] Invalid JSON generated. Raw output:")
        print(raw_output)
        return {"error": "Invalid JSON", "raw": raw_output}


# ---------------------------
# 4) Quick Test
# ---------------------------
if __name__ == "main":
    test = "animate vector addition with two arrows"
    result = agent1_interpret(test)
    print(json.dumps(result, indent=2))