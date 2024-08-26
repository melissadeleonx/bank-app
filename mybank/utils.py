# Utility functions for email and auth verification, and user activation
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str 
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

# Verifies user email using uid and token, and activates the user if valid
def verify_user_email(uidb64, token):
    try:
        # user ID decoded from base64
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_verified = True 
        user.save()
        
        # Send verification success email
        subject = 'Thank You for Verifying Your Email'
        message = f'''
        Hi {user.username},

        Thank you for verifying your email address with MyBank. Your account is now active and you can complete your profile.

        Best regards,
        The MyBank Team
        '''
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            return True, "Your email has been verified. You can now log in."
        except Exception as e:
            return False, f"Failed to send thank-you email: {e}"
    else:
        return False, "The confirmation link is invalid or has expired."
    

