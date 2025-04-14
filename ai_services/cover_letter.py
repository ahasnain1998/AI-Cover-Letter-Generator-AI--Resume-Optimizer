

import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()
API_KEY = os.getenv("HF_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

headers = {"Authorization": f"Bearer {API_KEY}"}

def generate_cover_letter(resume_text, job_description, tone='professional', max_retries=3):
    if not API_KEY:
        return "Error: API key not found. Please set HF_API_KEY in your .env file."

    prompt = f"""
    ### Instructions:
    Write a {tone}, ATS-friendly cover letter (150-200 words) aligning the resume to the job description below. Start with "Dear Hiring Manager," and end with "Sincerely, [Your Name]".

    ### Resume:
    {resume_text}

    ### Job Description:
    {job_description}

    ### Begin Cover Letter:
    """

    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=30)
            response.raise_for_status()
            result = response.json()

            if isinstance(result, list) and "generated_text" in result[0]:
                generated_text = result[0]["generated_text"]
                cover_letter = generated_text.split("### Begin Cover Letter:")[-1].strip()
                if not cover_letter.endswith("[Your Name]"):
                    cover_letter += "\n\nSincerely,\n[Your Name]"
                return cover_letter

            return "Error: Unexpected API response format."
        except requests.exceptions.RequestException as e:
            time.sleep(5)
    return "Error: Failed to connect to API after retries."







