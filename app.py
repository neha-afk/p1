import os
import sys
from groq import Groq

# --- Setup: load API key from environment, never hardcode it ---
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    print("ERROR: GROQ_API_KEY environment variable is not set.")
    print("Set it with:  set GROQ_API_KEY=your_key_here  (Windows)")
    print("          or  export GROQ_API_KEY=your_key_here  (Mac/Linux)")
    sys.exit(1)

client = Groq(api_key=api_key)

# --- Helper: send one prompt to Groq and return the reply as a string ---
def ask(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        temperature=0.4,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a career counsellor for students. "
                    "Be specific, concise and consistent. "
                    "Use only the facts given about the student."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()

# --- Step 1: Collect student details from the user ---
print("=== AI-Based Personalized Career Content Generator ===\n")
name      = input("Your name: ").strip()
skills    = input("Your skills (comma-separated): ").strip()
interests = input("Your academic interests: ").strip()
goal      = input("Your career goal: ").strip()

# --- Step 2: Build a shared profile string used in every prompt ---
profile = (
    f"Student Name: {name}\n"
    f"Skills: {skills}\n"
    f"Academic Interests: {interests}\n"
    f"Career Goal: {goal}"
)

print("\nGenerating your personalized career profile — please wait...\n")

# --- Step 3a: Prompt 1 — Professional Summary ---
# Asks the model for a 3-4 line first-person summary for a resume/LinkedIn
summary = ask(
    f"{profile}\n\n"
    "Write a 3-4 line first-person professional summary suitable for a resume "
    "or LinkedIn profile. Mention the career goal explicitly."
)

# --- Step 3b: Prompt 2 — Skill-Gap Report ---
# Reuses profile + summary so the model stays consistent with what was just said
skill_gap = ask(
    f"{profile}\n\nProfessional Summary:\n{summary}\n\n"
    "Produce a Skill-Gap Report with three clearly labelled sections:\n"
    "1. Skills Already Owned that are relevant to the career goal.\n"
    "2. Missing Skills needed to reach the career goal.\n"
    "3. Priority (High / Medium / Low) for each missing skill, with a one-line reason."
)

# --- Step 3c: Prompt 3 — Learning Recommendations ---
# Builds on the skill-gap report; only recommends resources for missing skills
learning = ask(
    f"{profile}\n\nSkill-Gap Report:\n{skill_gap}\n\n"
    "Based ONLY on the missing skills above, provide:\n"
    "- 3 free or low-cost online courses (name + platform).\n"
    "- 2 beginner-friendly project ideas that practise those skills.\n"
    "- A simple 4-week study plan."
)

# --- Step 3d: Prompt 4 — Interview Preparation ---
# Uses profile + skill-gap to tailor questions to this student's exact strengths/gaps
interview = ask(
    f"{profile}\n\nSkill-Gap Report:\n{skill_gap}\n\n"
    "Provide interview preparation material:\n"
    "- 5 technical interview questions with short model answers.\n"
    "- 3 HR / behavioural questions with tips on how to answer them.\n"
    "- 1 question specifically about the student's weakest/lowest-priority skill, "
    "with advice on how to answer it honestly and confidently."
)

# --- Step 4: Combine all outputs into one final report ---
report = f"""
{'='*60}
  AI-BASED PERSONALIZED CAREER PROFILE
  Student: {name}
{'='*60}

PROFESSIONAL SUMMARY
{'-'*40}
{summary}

SKILL-GAP REPORT
{'-'*40}
{skill_gap}

LEARNING RECOMMENDATIONS
{'-'*40}
{learning}

INTERVIEW PREPARATION
{'-'*40}
{interview}

{'='*60}
"""

# --- Print the report to the terminal ---
print(report)

# --- Save the report to a text file named after the student ---
filename = f"{name.replace(' ', '_')}_career_profile.txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write(report)

print(f"Report saved to: {filename}")

