from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from celery import shared_task
from django.utils.html import strip_tags


@shared_task
def send_email(subject:str, ctx:dict[str,any], template_path:str, recipient_list:list[str], attchament_list: list[list[str,str]] = None):
    ctx['site_domain'] = settings.SITE_DOMAIN
    email_from = settings.EMAIL_HOST_USER
    html_message = render_to_string(template_name=template_path,context=ctx)
    plain_message = strip_tags(html_message)
    message = EmailMultiAlternatives(
        subject= subject,
        body= plain_message,
        from_email= email_from,
        to = recipient_list,
    )
    # application/pdf
    message.attach_alternative(html_message,'text/html')
    if attchament_list:
        for attachament in attchament_list:
            message.attach(filename = attachament[0],content= attachament[1],mimetype = attachament[2] )
    message.send()