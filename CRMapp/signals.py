from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .models import *



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "token={}".format( reset_password_token.key)
        }
    
    # @NOTE: Add validation to the function, catch errors when something wrong happens (try, catch)
    email_html_message = render_to_string('user_reset_password.html', context)
    # email_plaintext_message = render_to_string('user_reset_password.txt', context)    
    email_plaintext_message = "token={}".format( reset_password_token.key)

    msg = EmailMultiAlternatives(
    # title:
    ("Password Reset for {title}".format(title="Some website title")),
    # message:
    email_plaintext_message,
    # from:
    settings.EMAIL_HOST_USER,
    # to:
    [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
 