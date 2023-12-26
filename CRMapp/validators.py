from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^\+9715\d{8}$', message="Phone number must be entered in the format: '+9715Xxxxxxxx'.")

url_validator = RegexValidator(regex=r'^https?://\S+$', message="Invalid URL format")