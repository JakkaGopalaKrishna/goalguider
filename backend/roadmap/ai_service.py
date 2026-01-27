from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_roadmap_with_ai(current_status, career_goal):
    prompt = f"""
You are a career guidance system.

Generate a personalized career roadmap in STRICT JSON format.

Rules:
- Output ONLY valid JSON
- No markdown
- No explanations
- Steps must be in logical order

Input:
Current Status: {current_status}
Career Goal: {career_goal}

JSON format:
{{
  "steps": [
    {{
      "step_number": 1,
      "title": "Step title",
      "description": "What to do in this step",
      "duration": "Time period"
    }}
  ]
}}
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )
    print(response.text)
    return response.text
