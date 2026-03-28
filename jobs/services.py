from .models import Jobs


def get_latest_jobs_qs(user=None,page=1, page_size=10):
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
        total       = jobs.count()
        total_pages = (total + page_size - 1) // page_size   # ceil division
        start       = (page - 1) * page_size
        end         = start + page_size

    
    return {
        'jobs': list(
            jobs[start:end].values(
                'id', 'title', 'company', 'location',
                'salary', 'job_type', 'created_at'
            )
        ),
      'pagination': {
            'total':       total,
            'page':        page,
            'page_size':   page_size,
            'total_pages': total_pages,
            'has_next':    page < total_pages,
            'has_prev':    page > 1,
        }
    }