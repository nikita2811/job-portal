# applications/resume_parser.py
import re
import pdfplumber
import docx
import spacy

nlp = spacy.load('en_core_web_sm')

# ─── Extract Text ────────────────────────────────────────────

def extract_text_from_pdf(file_path):
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

def extract_text_from_docx(file_path):
    doc  = docx.Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    return ''

# Extract Name

def extract_name(text):
    doc = nlp(text[:500])                               
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text
    return ''

# Extract Email

def extract_email(text):
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match   = re.search(pattern, text)
    return match.group(0) if match else ''

# Extract Phone

def extract_phone(text):
    pattern = r'(\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'
    match   = re.search(pattern, text)
    return match.group(0) if match else ''

# Extract Skills

SKILLS_DB = [
    # programming languages
    'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go',
    # frameworks
    'django', 'flask', 'fastapi', 'react', 'vue', 'angular', 'node', 'express', 'spring',
    # databases
    'postgresql', 'mysql', 'mongodb', 'redis', 'sqlite', 'oracle',
    # tools
    'docker', 'kubernetes', 'git', 'aws', 'azure', 'gcp', 'linux', 'nginx',
    # concepts
    'rest api', 'graphql', 'microservices', 'ci/cd', 'agile', 'scrum',
]

def extract_skills(text):
    text_lower = text.lower()
    return [skill for skill in SKILLS_DB if skill in text_lower]

# Extract Experience

def extract_experience(text):
    experience = []
    # match patterns like "2019 - 2022" or "Jan 2020 - Present"
    pattern    = r'(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?\s?\d{4})\s*[-–]\s*(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?\s?\d{4}|Present)'
    matches    = re.finditer(pattern, text, re.IGNORECASE)

    for match in matches:
        # get surrounding context (job title, company)
        start   = max(0, match.start() - 100)
        end     = min(len(text), match.end() + 100)
        context = text[start:end].strip()
        experience.append({
            'duration': match.group(0),
            'context':  context,
        })
    return experience

# Extract Education 

def extract_education(text):
    education = []
    degrees   = ['bachelor', 'master', 'phd', 'b.tech', 'm.tech', 'bsc', 'msc', 'mba', 'b.e', 'm.e']
    lines     = text.lower().split('\n')

    for line in lines:
        if any(degree in line for degree in degrees):
            education.append(line.strip())

    return education



def parse_resume(file_path):
    text = extract_text(file_path)
    return {
        'raw_text':   text,
        'name':       extract_name(text),
        'email':      extract_email(text),
        'phone':      extract_phone(text),
        'skills':     extract_skills(text),
        'experience': extract_experience(text),
        'education':  extract_education(text),
    }