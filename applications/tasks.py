from celery import shared_task
from django.core.mail import send_mail
from .models import Application

# Always use @shared_task in reusable apps (not @app.task)
@shared_task(bind=True, max_retries=3)
#need to rewite this function logic
def send_application_email(self, data):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        send_mail(
            subject='Welcome!',
            message=f'Hi {user.first_name}, welcome aboard.',
            from_email='noreply@example.com',
            recipient_list=[user.email],
        )
    except Exception as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)

