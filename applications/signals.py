# applications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application, ParsedResume
from .resume_parser import parse_resume
from .match_socre import calculate_match_score

@receiver(post_save, sender=Application)
def parse_resume_on_apply(sender, instance, created, **kwargs):
    if created:
        # parse resume
        parsed = parse_resume(instance.resume.path)

        # save parsed data
        ParsedResume.objects.create(
            application = instance,
            name        = parsed['name'],
            email       = parsed['email'],
            phone       = parsed['phone'],
            skills      = parsed['skills'],
            experience  = parsed['experience'],
            education   = parsed['education'],
            raw_text    = parsed['raw_text'],
        )

        # calculate and save match score
        score            = calculate_match_score(parsed, instance.job)
        instance.match_score = score
        instance.save()