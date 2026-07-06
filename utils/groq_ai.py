from dotenv import load_dotenv 
load_dotenv()
from groq import Groq
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_ingredients_with_ai(ingredients, score):
    prompt = f"""
You are a professional nutritionist.

Ingredients:
{ingredients}

Overall Health Score: {score}/10

Please provide:
1. A short summary.
2. Healthy ingredients.
3. Harmful ingredients.
4. Who should avoid this product.
5. Final recommendation.

Keep the answer under 150 words.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
import json

def extract_ingredients_with_ai(ocr_text):

    prompt = f"""
You are a food ingredient extraction expert.

Extract ONLY the ingredient names from the OCR text.

Rules:
- Return ONLY valid JSON.
- Do NOT explain anything.
- Remove percentages.
- Remove headings like INGREDIENTS.
- Keep INS numbers.
- Keep complete ingredient names.
- Ignore manufacturing information.

Example:

Input:
Ingredients:
Refined Wheat Flour (80%), Palm Oil,
Iodized Salt, INS 621, INS 451

Output:

[
"REFINED WHEAT FLOUR",
"PALM OIL",
"IODIZED SALT",
"INS 621",
"INS 451"
]

OCR TEXT:

{ocr_text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip()

    try:
        return json.loads(result)
    except:
        return []
def analyze_ingredients_with_ai(ingredients):

    import json

    prompt = f"""
You are a professional food scientist.

Analyze every ingredient below.

Ingredients:
{ingredients}

Return ONLY valid JSON.

Format:

[
  {{
    "name":"SUGAR",
    "category":"Sweetener",
    "purpose":"Sweetener",
    "description":"Provides sweetness.",
    "health_score":4,
    "risk_level":"Medium",
    "benefits":"Quick energy.",
    "side_effects":"High intake increases risk of obesity and diabetes.",
    "recommendation":"Consume in moderation."
  }}
]

Do NOT write markdown.
Do NOT explain.
Return ONLY JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()

    return json.loads(content)
def analyze_with_ai(ingredients, score):

    prompt = f"""
You are a professional nutritionist.

Ingredients:
{ingredients}

Overall Health Score: {score}/10

Please provide:
1. A short summary.
2. Healthy ingredients.
3. Harmful ingredients.
4. Who should avoid this product.
5. Final recommendation.

Keep the answer under 150 words.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content