# applications/match_score.py

def calculate_match_score(parsed_resume, job):
    score        = 0
    total_checks = 0

    # skills match
    job_skills    = list(job.skills.values_list('name', flat=True))
    resume_skills = [s.lower() for s in parsed_resume.get('skills', [])]

    if job_skills:
        matched  = [s for s in job_skills if s.lower() in resume_skills]
        score   += (len(matched) / len(job_skills)) * 60    # skills = 60% weight
        total_checks += 60

    # location match 
    if job.location.lower() in parsed_resume.get('raw_text', '').lower():
        score += 20                                          # location = 20% weight
    total_checks += 20

    # experience match
    if parsed_resume.get('experience'):
        score += 20                                          # has experience = 20% weight
    total_checks += 20

    return round((score / total_checks) * 100, 2) if total_checks else 0