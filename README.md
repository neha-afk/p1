# AI-Based Personalized Career Content Generator

Generates a fully personalized career profile for a student using the **Groq API** (LLaMA 3.3 70B). Given a student's skills, academic interests and career goal, it produces:

- ✅ Professional Summary (resume / LinkedIn ready)
- ✅ Skill-Gap Report (what you have, what you're missing, priorities)
- ✅ Learning Recommendations (courses, projects, 4-week study plan)
- ✅ Interview Preparation (technical + HR questions with model answers)

All four sections are consistent with each other through **prompt chaining** — each step builds on the previous one using the same student profile.

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your Groq API key

**Windows (Command Prompt)**
```cmd
set GROQ_API_KEY=your_groq_api_key_here
```

**Windows (PowerShell)**
```powershell
$env:GROQ_API_KEY="your_groq_api_key_here"
```

**Mac / Linux**
```bash
export GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at: https://console.groq.com

---

## How to Run

```bash
python app.py
```

You will be prompted to enter:
- Your name
- Your skills (comma-separated)
- Your academic interests
- Your career goal

The report is printed to the terminal **and** saved as `<YourName>_career_profile.txt`.

---

## Sample Input

```
Your name: Priya
Your skills (comma-separated): Python, HTML, basic SQL
Your academic interests: Machine learning, statistics
Your career goal: Data Scientist
```

Expected output file: `Priya_career_profile.txt`

