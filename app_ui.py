import os
import streamlit as st
from groq import Groq
from fpdf import FPDF

# --- Page config ---
st.set_page_config(page_title="Career Content Generator", page_icon="🎯", layout="centered")
st.title("🎯 AI-Based Personalized Career Content Generator")
st.caption("Powered by Groq AI · Fill the form below to generate your personalized career profile")

# --- Check for API key; show error in UI instead of crashing ---
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("⚠️ GROQ_API_KEY is not set. Set it in your terminal and restart with `streamlit run app_ui.py`.")
    st.stop()

client = Groq(api_key=api_key)

# --- Helper: send one prompt to Groq and return the reply ---
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

# --- PDF builder: creates a nicely formatted PDF and returns bytes ---
def build_pdf(name, summary, skill_gap, learning, interview):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title block
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "AI-Based Personalized Career Profile", ln=True, align="C")
    pdf.set_font("Helvetica", "I", 12)
    pdf.cell(0, 8, f"Student: {name}", ln=True, align="C")
    pdf.ln(6)

    # Helper to write a section with a bold heading and body text
    def section(heading, body):
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_fill_color(230, 240, 255)
        pdf.cell(0, 9, heading, ln=True, fill=True)
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 10)
        # Encode to latin-1 safely (replace unsupported chars) for built-in fonts
        safe_body = body.encode("latin-1", errors="replace").decode("latin-1")
        pdf.multi_cell(0, 6, safe_body)
        pdf.ln(5)

    section("PROFESSIONAL SUMMARY", summary)
    section("SKILL-GAP REPORT", skill_gap)
    section("LEARNING RECOMMENDATIONS", learning)
    section("INTERVIEW PREPARATION", interview)

    return bytes(pdf.output())

# --- Input form ---
with st.form("career_form"):
    st.subheader("📋 Enter Your Details")
    name      = st.text_input("Full Name",                      placeholder="e.g. Priya")
    skills    = st.text_input("Skills (comma-separated)",       placeholder="e.g. Python, HTML, basic SQL")
    interests = st.text_input("Academic Interests",             placeholder="e.g. Machine learning, statistics")
    goal      = st.text_input("Career Goal",                    placeholder="e.g. Data Scientist")
    submitted = st.form_submit_button("✨ Generate My Career Profile")

# --- On form submit ---
if submitted:
    # Validate inputs
    if not all([name, skills, interests, goal]):
        st.warning("⚠️ Please fill in all four fields before generating.")
        st.stop()

    # Build the shared profile string passed to every prompt
    profile = (
        f"Student Name: {name}\n"
        f"Skills: {skills}\n"
        f"Academic Interests: {interests}\n"
        f"Career Goal: {goal}"
    )

    # Run all 4 chained prompts with a progress bar
    progress = st.progress(0, text="Starting generation...")

    progress.progress(10, text="Step 1/4 — Writing Professional Summary...")
    summary = ask(
        f"{profile}\n\n"
        "Write a 3-4 line first-person professional summary suitable for a resume "
        "or LinkedIn profile. Mention the career goal explicitly."
    )

    progress.progress(35, text="Step 2/4 — Building Skill-Gap Report...")
    skill_gap = ask(
        f"{profile}\n\nProfessional Summary:\n{summary}\n\n"
        "Produce a Skill-Gap Report with three clearly labelled sections:\n"
        "1. Skills Already Owned that are relevant to the career goal.\n"
        "2. Missing Skills needed to reach the career goal.\n"
        "3. Priority (High / Medium / Low) for each missing skill, with a one-line reason."
    )

    progress.progress(60, text="Step 3/4 — Creating Learning Recommendations...")
    learning = ask(
        f"{profile}\n\nSkill-Gap Report:\n{skill_gap}\n\n"
        "Based ONLY on the missing skills above, provide:\n"
        "- 3 free or low-cost online courses (name + platform).\n"
        "- 2 beginner-friendly project ideas that practise those skills.\n"
        "- A simple 4-week study plan."
    )

    progress.progress(85, text="Step 4/4 — Preparing Interview Material...")
    interview = ask(
        f"{profile}\n\nSkill-Gap Report:\n{skill_gap}\n\n"
        "Provide interview preparation material:\n"
        "- 5 technical interview questions with short model answers.\n"
        "- 3 HR / behavioural questions with tips on how to answer them.\n"
        "- 1 question specifically about the student's weakest/lowest-priority skill, "
        "with advice on how to answer it honestly and confidently."
    )

    progress.progress(100, text="Done!")
    progress.empty()

    # --- Display the four sections ---
    st.success(f"✅ Career profile for **{name}** is ready!")

    with st.expander("📝 Professional Summary", expanded=True):
        st.write(summary)

    with st.expander("🔍 Skill-Gap Report", expanded=True):
        st.write(skill_gap)

    with st.expander("📚 Learning Recommendations", expanded=True):
        st.write(learning)

    with st.expander("🎤 Interview Preparation", expanded=True):
        st.write(interview)

    st.divider()

    # --- Build plain-text report for TXT download ---
    txt_report = (
        f"AI-BASED PERSONALIZED CAREER PROFILE\n"
        f"Student: {name}\n"
        f"{'='*60}\n\n"
        f"PROFESSIONAL SUMMARY\n{'-'*40}\n{summary}\n\n"
        f"SKILL-GAP REPORT\n{'-'*40}\n{skill_gap}\n\n"
        f"LEARNING RECOMMENDATIONS\n{'-'*40}\n{learning}\n\n"
        f"INTERVIEW PREPARATION\n{'-'*40}\n{interview}\n"
    )

    # --- Build PDF bytes ---
    pdf_bytes = build_pdf(name, summary, skill_gap, learning, interview)

    # --- Download buttons side by side ---
    st.subheader("⬇️ Download Your Report")
    col1, col2 = st.columns(2)
    safe_name = name.replace(" ", "_")

    with col1:
        st.download_button(
            label="📄 Download as TXT",
            data=txt_report,
            file_name=f"{safe_name}_career_profile.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            label="📕 Download as PDF",
            data=pdf_bytes,
            file_name=f"{safe_name}_career_profile.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

