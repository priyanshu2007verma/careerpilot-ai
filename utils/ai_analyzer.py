from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_resume(resume_text):

    prompt = f"""
You are an expert ATS Resume Reviewer and Career Coach.

Analyze this resume and provide:

Resume Score (out of 100)

ATS Score (out of 100)

Top 3 Strengths

Top 3 Weaknesses

5 Suggestions

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

        temperature=0.3,
        max_tokens=1000

    )

    return response.choices[0].message.content