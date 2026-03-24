# jobs/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Jobs

@receiver(post_save, sender=Jobs)
def broadcast_new_job(sender, instance, created, **kwargs):
    if created:                                         # only on new job creation
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'latest_jobs',                              # group name
            {
                'type': 'new_job_posted',               # maps to consumer method
                'job': {
                    'id':         instance.id,
                    'title':      instance.title,
                    'company':    instance.company,
                    'location':   instance.location,
                    'salary':     str(instance.salary),
                    'job_type':   instance.job_type,
                    'created_at': str(instance.created_at),
                }
            }
        )