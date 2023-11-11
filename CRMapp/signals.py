from django.db.models.signals import pre_save , post_save
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .models import *


@receiver(post_save, sender=UserProfile)
def check_user_position(sender, instance, **kwargs):
    if instance.isMaint:
        instance.isManager = False
        instance.isMangerMaint = False
        instance.isEmp = False
        instance.user.is_superuser = False
        instance.user.is_staff = False
    elif instance.isManager:
        instance.isMaint = False
        instance.isMangerMaint = False
        instance.isEmp = False
        instance.user.is_superuser = True
        instance.user.is_staff = True
    elif instance.isMangerMaint:
        instance.isMaint = False
        instance.isManager = False
        instance.isEmp = False
        instance.user.is_superuser = True
        instance.user.is_staff = True
    elif instance.isEmp:
        instance.isMaint = False
        instance.isManager = False
        instance.isMangerMaint = False
        instance.user.is_superuser = True
        instance.user.is_staff = True
    instance.save()


@receiver(pre_save, sender=Client)
def check_client_exists(sender, instance, **kwargs):

    existing_client = Client.objects.filter(name__icontains=instance.name).first() or Client.objects.filter(mobile_phone=instance.mobile_phone).first()
    if existing_client and existing_client != instance:
        
        raise Exception("Client with this name already exists")

@receiver(pre_save, sender=Interest)
def check_interest_exists(sender, instance, **kwargs):
    existing_interest = Interest.objects.filter(client=instance.client, company_name=instance.company_name).first()
    if existing_interest and existing_interest != instance:
        
        raise Exception("Client with this interest already exists")


@receiver(pre_save, sender=Phase)
def check_duplicate_phase(sender, instance, **kwargs):
    if instance.isActive:
       
        Phase.objects.filter(contract=instance.contract, isActive=True).exclude(id=instance.id).update(isActive=False)

    existing_phase = Phase.objects.filter(
        contract=instance.contract, 
        Name=instance.Name,
    ).exclude(id=instance.id)  
    
    
    if existing_phase.exists():
        raise Exception("contract with this phase already exist")

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
 