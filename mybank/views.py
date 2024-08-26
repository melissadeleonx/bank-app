# Standard Library
from io import BytesIO
import base64

# Third-Party Library
import pyotp
import qrcode
from googleapiclient.discovery import build

# Django Core Imports
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Django Auth
from django.contrib.auth import login as django_login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm


# MyBank File Imports
from .forms import UserRegistrationForm, UserLoginForm, DepositForm, WithdrawalForm, TOTPVerificationForm, PasswordResetRequestForm
from .models import User, UserProfile, Account, Transaction
from .google_auth import get_authorization_url, get_credentials_from_code
from .utils import verify_user_email

# Homepage and Blog Views
# TODO: Make a separate frontend homepage and connect it using django frameworks
def index(request):
    """Render the homepage, accessible by all users"""
    return render(request, "mybank/index.html")

# Authentication Views
# Registration: Handles user registration using the MyBank UserRegistrationForm and verification tokens or Sign-Up via Google OAuth2.
def register(request):
    """
    Handle user registration using UserRegistrationForm.
    Process registration forms, generates email verification tokens, 
    and sends a confirmation email to the user. It also provides the option to sign up via Google OAuth2.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # User is initially inactive until email is verified
            user.is_active = False
            # Once user is saved to database, user's profile and account are also created using signals
            user.save()


            # Generate email verification token and send a confirmation email to the user.
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))           
            verification_url = request.build_absolute_uri(
                reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
            )

            subject = 'Confirm Your Email Address'
            message = f'''
            Hi {user.username},

            Please click the link below to verify your email address and activate your account:
            {verification_url}

            Best regards,
            The MyBank Team
            '''
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            try:
                # TODO: Create a professional looking Email template instead of simple message
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, "Please check your email to confirm your registration.")
                return redirect(reverse('registration_confirmation'))
            except Exception as e:
                messages.error(request, f"Failed to send confirmation email: {e}")
                return redirect(reverse('register'))  

        else:
            # Handles registration form errors
            return render(request, "mybank/auth/register.html", {
                "form": form,
                "message": "Please correct the errors below."
            })
    else:
        form = UserRegistrationForm()

    # From google_auth.py, it generate Google OAuth2 authorization URL
    google_auth_url = get_authorization_url()

    context = {
        "form": form,
        "google_auth_url": google_auth_url
    }

    return render(request, "mybank/auth/register.html", context)

# Log In: Handles user login with UserLoginForm and integrates Two-Factor Authentication (2FA) flow.
def login_view(request):
    """
    Handle user login using UserLoginForm.
    Process login forms and manages Two-Factor Authentication (2FA).
    1. Validating user credentials.
    2. Checking if the user has completed 2FA setup.
    3. Redirecting to the 2FA setup or verification page as needed.
    4. Allowing access to the dashboard if 2FA is completed and verified.
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        # Step 1: Form validation
        if form.is_valid():
            user = form.cleaned_data.get('user')
            django_login(request, user)
            
            # Step 2: Check if user has completed Two-Factor Authentication setup
            if not user.is_2fa_setup_completed:
                return redirect(reverse('two_factor_setup'))
            
            # Step 2.1: Verify Two-Factor Authentication session status
            elif not request.session.get('is_2fa_verified', False):
                return redirect(reverse('ttop_verify'))
            
            else:
                # Step 3: Proceed to dashboard if 2FA setup is completed and verified
                return redirect(reverse('dashboard'))
        else:
            # Error handling
            return render(request, 'mybank/auth/login.html', {
                'form': form,
                'message': 'Please correct the errors below.'
            })
    else:
        form = UserLoginForm()

    # User can log in using Gmail and repeat the same Two-Factor Authentication flow
    google_auth_url = get_authorization_url()

    context = {
        'form': form,
        'google_auth_url': google_auth_url
    }

    return render(request, 'mybank/auth/login.html', context)

# LogOut
@login_required
def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, "We have confirmed that you have left your Dashboard Area.")
    return redirect(reverse("index"))

# Password-reset(forgot password?) related logic and templates
def password_reset_request(request):
    """
    Handle password reset requests by processing the PasswordResetRequestForm.
    1. Validates the email address submitted in the form.
    2. Checks if any users exist with that email address.
    3. Generates a password reset token and URL if the user exists.
    4. Sends an email with the password reset instructions to the user.
    5. Provides feedback to the user on the request status.
    """
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user_model = get_user_model()

            # Find users associated with the given email address
            users = user_model.objects.filter(email=email)
            if users.exists():
                for user in users:
                    # Generate a token and encode user ID for the password reset URL
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    reset_url = request.build_absolute_uri(
                        reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                    )
                    subject = "Password Reset Request"
                    # the message is in a Password reset email template
                    message = render_to_string('mybank/auth/password_reset_email.html', {
                        'user': user,
                        'reset_url': reset_url,
                    })
                    # Using SMTP and django send_mail, send the password reset email
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                messages.success(request, "We have emailed you instructions for resetting your password.")
                return redirect('password_reset_done')
            else:
                messages.error(request, "No user is associated with this email address.")
    else:
        form = PasswordResetRequestForm()

    return render(request, 'mybank/auth/password_reset_request.html', {'form': form})

def password_reset_done(request):
    """Render password reset done page."""
    return render(request, 'mybank/auth/password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    """
    Handle the password reset confirmation process.
    1. Validates the reset token and user ID.
    2. Use Django's SetPasswordForm to set a new password if the token is valid.
    3. Saves the new password and redirects to the login page upon success.
    4. Provides feedback if the token is invalid or expired.
    """   
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect('login')
        else:
            form = SetPasswordForm(user)

        return render(request, 'mybank/auth/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "The password reset link is no longer valid.")
        return redirect('password_reset_request')


# Email Verification
def verify_email(request, uidb64, token):
    """
    Verify the user's email using the provided token and uid.
    If successful, log in the user with limited access before 2fa setup is completed.
    """
    success, message = verify_user_email(uidb64, token)

    if success:
        user = get_object_or_404(get_user_model(), pk=force_bytes(urlsafe_base64_decode(uidb64)))
        django_login(request, user)  
        messages.success(request, message)
        return redirect(reverse('verification_success'))
    else:
        messages.error(request, message)
        return redirect(reverse('index'))

# Two-factor Authentication Set up
# TODO:
# 1. Create a 2FA reset functionality to allow users to reconfigure their 2FA settings if needed.
# 2. Implement rate limiting for OTP verification attempts to prevent abuse and brute-force attacks.
@login_required
def two_factor_setup(request):
    """ Handle the setup process for Two-Factor Authentication (2FA) for the newly registered user.
    1. Generate a Time-based One-Time Password (TOTP) key using the pyotp library, if one does not already exist for the user.
    2. Create a provisioning URI that is used to set up the TOTP authenticator app.
    3. Generate a QR code from the provisioning URI using the qrcode library. This QR code is scanned by the user's authenticator app.
    4. Convert the QR code image to a Base64-encoded string so it can be embedded directly in HTML.
    5. Handle OTP verification: When a POST request is made, verify the OTP submitted by the user. If the OTP is valid, mark 2FA setup as complete and redirect to the dashboard. If invalid, show an error message.
    """
    user = request.user

    # Step 1: Generate TOTP key if not already done
    if not user.totp_key:
        user.totp_key = pyotp.random_base32()
        user.save()

    # Step 2: Generate the TOTP provisioning URI and QR code.
    totp = pyotp.TOTP(user.totp_key)
    provisioning_uri = totp.provisioning_uri(name=user.email, issuer_name="MyBank")

    # Step 3: Generate the QR code from the provisioning URI and convert it to Base64
    qr = qrcode.make(provisioning_uri)
    qr_image = BytesIO()
    qr.save(qr_image, format='PNG')
    qr_image.seek(0)
    qr_code_image_base64 = base64.b64encode(qr_image.getvalue()).decode('utf-8')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        if totp.verify(otp):
            user.is_2fa_setup_completed = True
            user.save()
            messages.success(request, 'Two-Factor Authentication has been successfully set up.')
            return redirect('dashboard')
        else:
            messages.error(request, 'The code you entered is incorrect. Please try again.')

    context = {
        'provisioning_uri': provisioning_uri,
        'qr_code_image': qr_code_image_base64,
    }

    return render(request, 'mybank/auth/two_factor_setup.html', context)

# Two-Factor Authentication Verification
@login_required
def ttop_verify(request):
    """Handle the verification process for Two-Factor Authentication (2FA) using TOTP codes."""

    # Form is accessed only if 2fa set up is already completed
    if request.method == 'POST':
        form = TOTPVerificationForm(request.POST)
        if form.is_valid():
            user = request.user
            code = form.cleaned_data.get('code')
            totp = pyotp.TOTP(user.totp_key)

            
            if totp.verify(code):
                # Mark 2FA as verified for the current session.
                user.is_2fa_verified = True  
                user.save() 
                return redirect(reverse('dashboard'))
            else:
                form.add_error(None, 'Invalid TOTP code. Please try again.')
    else:
        form = TOTPVerificationForm()

    return render(request, 'mybank/auth/ttop_verify.html', {'form': form})

# Tried a few Django packages and uninstalled them, Google API provides the simplest setup instructions
# https://googleapis.github.io/google-api-python-client/docs/oauth.html
def oauth2callback(request):
    """
    Handles the OAuth2 callback from Google
    1. During development, tester email addresses are added to exchange the authorization code for OAuth2 credentials.
    2. Fetches user profile information from Google People API(not to be confused with Gmail API)
    3. Logs the user in or creates a new account if the user does not already exist.
    """
    code = request.GET.get('code')
    if not code:
        return HttpResponse('Error: No code provided', status=400)
    
    try:
        creds = get_credentials_from_code(code)
        
        # Fetch user profile information from Google People API
        service = build('people', 'v1', credentials=creds)
        profile = service.people().get(
            resourceName='people/me',
            personFields='emailAddresses,names'
        ).execute()

        email = profile.get('emailAddresses', [{}])[0].get('value')
        name = profile.get('names', [{}])[0].get('displayName')

        if not email:
            return HttpResponse('Error: No email address found in profile', status=400)

        # Check if user exists or create a new user
        user, created = User.objects.get_or_create(email=email, defaults={'username': name})
        user.is_verified = True

        if created:
            # New user created via Google OAuth
            user.set_unusable_password()
            user.save()

            # No need to create a new account as signals already do that after user is created

            # Send a confirmation email to newly signed up users only
            # TODO: Create a professional email template instead of just a simple message
            subject = 'Welcome to MyBank!'
            message = f'''
            Hi {user.username},

            Thank you for registering with MyBank. We are excited to have you onboard!

            Best regards,
            The MyBank Team
            '''
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, "Confirmation email sent successfully.")
            except Exception as e:
                messages.error(request, f"Failed to send confirmation email: {e}")
        
        # Log the user in after normal registration or Google registration
        django_login(request, user)

        # Same authentication steps, after logging in, check the 2FA status and redirect accordingly
        if not user.is_2fa_setup_completed:
            # Redirect to TOTP setup page if 2FA is not set up
            return redirect(reverse('two_factor_setup'))
        elif not request.session.get('is_2fa_verified', False):
            # Redirect to TOTP verification page if 2FA is set up but not verified for this session
            return redirect(reverse('ttop_verify'))

        # If 2FA is set up and verified, proceed to the dashboard
        return redirect(reverse('dashboard'))
    
    except Exception as e:
        return HttpResponse(f'Error during OAuth callback: {e}', status=500)

def google_login(request):
    """
    Redirects the user to Google's OAuth 2.0 authorization URL to initiate the login process.
    """
    auth_url = get_authorization_url()
    return redirect(auth_url)

# Confirmation Views
def registration_confirmation(request):
    """ User is redirected here after registration """
    return render(request, "mybank/confirmation/registration_confirmation.html")

@login_required
def verification_success(request):
    "User is redirected here after email verification"
    return render(request, 'mybank/confirmation/verification-success.html')



# Dashboard and Account Views

# TODO: 2fa_verified sessions should be enforced. Enhance dashboard with account summaries and recent transactions
@login_required
def dashboard(request):
    """Dashboard can only be viewed by the users if they have completed 2FA."""
    if not request.user.is_2fa_setup_completed:
        return redirect('two_factor_setup')
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        account = Account.objects.get(user=request.user)
        recent_transactions = Transaction.objects.filter(account=account).order_by('-date')[:5]
        account_balance = account.balance
        
    except UserProfile.DoesNotExist:
        user_profile = None
        recent_transactions = None
        account_balance = 0 

    except Account.DoesNotExist:
        account = None
        recent_transactions = None
        account_balance = 0 

    current_date = timezone.now().date()

    context = {
        'user_profile': user_profile,
        'account': account,
        'recent_transactions': recent_transactions,
        'current_date': current_date,
        'account_balance': account_balance,
    }
    
    return render(request, 'mybank/accounts/dashboard.html', context)

# TODO: Add email notifications for successful transactions
# TODO: Implement transaction approval feature if needed
@login_required
def deposit(request):
    """ Handle deposits into user accounts using forms.py (requires login and 2fa_verified session) """
    user = request.user

    if request.method == 'POST':
        form = DepositForm(request.POST, user=user)
        if form.is_valid():
            account_number = form.cleaned_data.get('account_number')
            amount = form.cleaned_data.get('amount')

            account = get_object_or_404(Account, account_number=account_number, user=user)

            try:
                account.deposit(amount)
                # Log the transaction
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type=Transaction.DEPOSIT,
                    description=f"Deposit of {amount} to account {account_number}."
                )
                messages.success(request, f"Deposited {amount} to account {account_number}.")
                return redirect('dashboard')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = DepositForm(user=user)

    account = None
    if user.accounts.count() == 1:
        account = user.accounts.first()

    context = {
        'form': form, 
        'account': account
    }

    return render(request, 'mybank/transactions/deposit.html', context)

# TODO: Add email notifications for successful transactions
# TODO: Implement transaction approval feature if needed
@login_required
def withdraw(request):
    """ Handle withdrawals using forms.py (requires login and 2fa_verified session)"""
    user = request.user

    if request.method == 'POST':
        form = WithdrawalForm(request.POST, user=user)
        if form.is_valid():
            account_number = form.cleaned_data.get('account_number')
            amount = form.cleaned_data.get('amount')

            account = get_object_or_404(Account, account_number=account_number, user=user)

            try:
                account.withdraw(amount)
                # Log the transaction
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type=Transaction.WITHDRAWAL,
                    description=f"Withdrawal of {amount} from account {account_number}."
                )
                messages.success(request, f"Withdrew {amount} from account {account_number}.")
                return redirect('dashboard')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = WithdrawalForm(user=user)

    account = None
    if user.accounts.count() == 1:
        account = user.accounts.first()

    context = {
        'form': form,
        'account': account
    }

    return render(request, 'mybank/transactions/withdrawal.html', context)

# TODO: Add filtering options for transaction history
# TODO: Add email notifications for significant transactions
@login_required
def transaction_history(request):
    """ Like Dashboard, transaction_history can only be displayed for logged-in and 2fa completed user"""

    if not request.user.is_2fa_setup_completed:
        return redirect('two_factor_setup')
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        account = Account.objects.get(user=request.user)
        recent_transactions = Transaction.objects.filter(account=account).order_by('-date')[:5]


    except UserProfile.DoesNotExist:
        user_profile = None
        recent_transactions = None

    except Account.DoesNotExist:
        account = None
        recent_transactions = None

    current_date = timezone.now().date()

    context = {
        'user_profile': user_profile,
        'account': account,
        'recent_transactions': recent_transactions,
        'current_date': current_date,
    }
    
    return render(request, 'mybank/transactions/transaction_history.html', context)

#TODO List
#TODO Error Handling and Performance Optimization
#TODO MVP Follow-up: 
# Address post-MVP issues, like restricting dashboard access. 
# Research on access code system as an alternative to email.
#TODO Security Enhancements: 
# Rate limiting to prevent brute-force attacks.
# Add security questions (old but gold)) to align with common practices in online banking.
# HTTPS across the platform for secure data transmission.
# Cookie compliance (GDPR etc.)
#TODO User Behavior and Alerts:
# Research more on way to implement user behavior analytics to monitor and understand user interactions.
# Set up SMS or email alerts for various activities
#TODO Core Functionalities:
# Transfer functionality
# Make Payment functionality to handle bill payments and other services.
# Qrcode to make payments in physical stores
# Account Overview chart
# Budget Tracker feature
#TODO User Experiece:
# Check on famous apps' marketing/user experience strategy 
# Professional Email Template
# Profile Management features
# Settings and customizations
#TODO Tests and Debugging
