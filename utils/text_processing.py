import spacy

nlp = spacy.load("en_core_web_sm")

def analyze_match(resume_text, job_description):
    resume_doc = nlp(resume_text)
    job_doc = nlp(job_description)

    resume_keywords = {token.text.lower() for token in resume_doc if token.is_alpha}
    job_keywords = {token.text.lower() for token in job_doc if token.is_alpha}

    match_score = len(resume_keywords & job_keywords) / len(job_keywords) * 100

    return match_score, resume_keywords & job_keywords
