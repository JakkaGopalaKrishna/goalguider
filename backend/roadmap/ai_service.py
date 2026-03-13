# import google.generativeai as genai
# from django.conf import settings

# # client = genai.Client(api_key=settings.GEMINI_API_KEY)

# genai.configure(api_key=settings.GEMINI_API_KEY)
# model = genai.GenerativeModel("gemini-flash-latest")

# def generate_roadmap_with_ai(current_status, career_goal):
#     prompt = f"""
# You are a career guidance system.

# Generate a personalized career roadmap in STRICT JSON format.

# Rules:
# - Output ONLY valid JSON
# - No markdown
# - No explanations
# - Steps must be in logical order

# Input:
# Current Status: {current_status}
# Career Goal: {career_goal}

# JSON format:
# {{
#   "steps": [
#     {{
#       "step_number": 1,
#       "title": "Step title",
#       "description": "What to do in this step",
#       "duration": "Time period"
#     }}
#   ]
# }}
# """

#     # response = client.models.generate_content(
#     #     model="gemini-flash-latest",
#     #     contents=prompt
#     # )
#     response = model.generate_content(prompt)
#     print(response.text)
#     return response.text

# ----old version with prompt1----

# import google.generativeai as genai
# from django.conf import settings

# genai.configure(api_key=settings.GEMINI_API_KEY)
# model = genai.GenerativeModel("gemini-flash-latest")


# def generate_roadmap_with_ai(current_status, career_goal):
#     prompt = f"""
# You are an expert career mentor, curriculum designer, and industry professional.

# Your task is to generate a personalized career roadmap AND detailed daily tasks.

# STRICT RULES:
# - Output ONLY valid JSON
# - Do NOT include markdown
# - Do NOT include explanations
# - Do NOT include extra text
# - Steps must be in logical learning order
# - Each step MUST contain at least 10 to 12 tasks
# - Tasks must be small, specific, and actionable
# - Each task should be completable in 30–90 minutes
# - Avoid generic phrases like:
#   "understand basics", "read documentation", "watch a tutorial"
# - Tasks must feel practical and real-world
# - Do NOT repeat task patterns across different steps

# USER INPUT:
# Current Status: {current_status}
# Career Goal: {career_goal}

# OUTPUT JSON FORMAT (STRICT):

# {{
#   "steps": [
#     {{
#       "step_number": 1,
#       "title": "Step title",
#       "description": "Clear description of what this step covers",
#       "duration": "Estimated time period",
#       "tasks": [
#         "Task 1",
#         "Task 2",
#         "Task 3",
#         "... minimum 10 tasks total"
#       ]
#     }}
#   ]
# }}
# """

#     response = model.generate_content(prompt)
#     return response.text



# ----new version with prompt2----
import google.generativeai as genai
from django.conf import settings
import re

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-flash-latest")


def extract_json(text):
    """
    Safely extract JSON from Gemini output.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None


def generate_roadmap_with_ai(current_status, career_goal):
    prompt = f"""
You are an expert career mentor, curriculum architect, and industry professional.

Your responsibility is to generate a clear, realistic, and motivating career roadmap that helps a user progress from their current level to their target role.

USER CONTEXT:
Current Status: {current_status}
Target Role / Career Goal: {career_goal}

TASK:
Generate a detailed learning roadmap to help the user move from their current status to their target role.

IMPORTANT REQUIREMENTS:

ROADMAP STRUCTURE:
- Generate between 10 and 14 roadmap steps
- Each step should represent a focused, achievable milestone
- Steps must be in a logical progression order
- Steps should not be overly broad or vague
- Each step must feel like real progress to the user

FOR EACH ROADMAP STEP:
- Include:
  - step_number
  - title
  - description (clear, concise, practical)
  - duration (realistic time estimate)
  - tasks (minimum 10–12)

TASK GENERATION RULES:
- Tasks must be small, specific, and actionable
- Each task should be completable in 30–90 minutes
- Tasks should feel like real work, not syllabus headings
- Avoid generic phrases such as:
  - "understand basics"
  - "read documentation"
  - "watch a tutorial"
- Tasks must gradually increase in difficulty within the step
- Tasks must be directly related to the step topic
- Do NOT repeat the same task pattern across different steps

LEVEL AWARENESS:
- Adapt task depth and complexity based on the user's current status
- If user is intermediate or advanced, avoid beginner-level tasks

OUTPUT RULES:
- Output ONLY valid JSON
- No markdown
- No explanations
- No extra text

OUTPUT FORMAT (STRICT JSON):

{{
  "steps": [
    {{
      "step_number": 1,
      "title": "Step title",
      "description": "What this step focuses on",
      "duration": "Estimated duration",
      "tasks": [
        "Task 1",
        "Task 2",
        "Task 3"
      ]
    }}
  ]
}}
"""

    response = model.generate_content(prompt)

    raw_text = response.text.strip()
    json_text = extract_json(raw_text)

    if not json_text:
        raise ValueError("AI response did not contain valid JSON")

    return json_text
