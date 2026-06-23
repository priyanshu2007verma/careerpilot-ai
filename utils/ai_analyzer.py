from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_resume(resume_text):

    prompt = f"""
You are an expert ATS Resume Reviewer, Career Coach, and Hiring Manager.

Analyze the following resume and provide:

1. Resume Score (out of 100)
2. ATS Compatibility Score (out of 100)
3. Top 3 Strengths
4. Top 3 Weaknesses
5. Missing Skills or Keywords
6. 5 Actionable Suggestions
7. Final Verdict

Format the response professionally using clear headings.

Resume:

{resume_text}
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.4,
        max_tokens=1200

    )

    return response.choices[0].message.content