from .models import Jobs


def get_latest_jobs_qs(user=None):
    jobs = Jobs.objects.order_by('-created_at')

    # if user is passed and has preferences apply filters
    if user and hasattr(user, 'profile'):
        pref = user.profile

        # filter only if profile field is set
        if pref.title:
            jobs = jobs.filter(title__icontains=pref.title)

        if pref.location:
            jobs = jobs.filter(location__icontains=pref.location)

        if pref.salary:
            jobs = jobs.filter(salary__gte=pref.salary)

        if pref.job_type:
            jobs = jobs.filter(job_type__icontains=pref.job_type)
        
        if pref.experience:
            jobs = jobs.filter(experience__icontains=pref.experience)

    return list(
        jobs[:10].values(
            'id', 'title', 'company', 'location',
            'salary', 'job_type', 'created_at'
        )
    )