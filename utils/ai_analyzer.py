from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_resume(resume_text):

    prompt = f"""
You are an expert ATS Resume Reviewer.

Analyze the resume.

Return ONLY valid JSON.

Example:

{{
    "resume_score": 78,
    "ats_score": 82,
    "strengths": [
        "Strong technical skills",
        "Good project portfolio",
        "Leadership experience"
    ],
    "weaknesses": [
        "Limited work experience",
        "Missing certifications",
        "Lack of quantified achievements"
    ],
    "suggestions": [
        "Add project metrics",
        "Improve summary section",
        "Add certifications",
        "Include GitHub achievements",
        "Add more ATS keywords"
    ]
}}

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

        temperature=0.1

    )

    result = response.choices[0].message.content

    result = result.replace(
        "```json",
        ""
    )

    result = result.replace(
        "```",
        ""
    )

    result = result.strip()

    print(result)

    return json.loads(result)