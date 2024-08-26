from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, Account
from django.contrib.auth import authenticate
import re


# TODO: Complete the Two-Factor Authentication after email verification
class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration using Django's built-in UserCreationForm.
    The User model already includes first name, last name, and password fields.
    
    Enhancements: Implemented the user creation using Google Oauth2. Implemented the verification procedure after registration. 
    """
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="First Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Last Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )


    email = forms.EmailField(
        required=True,
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )

    terms_agreement = forms.BooleanField(
        label="",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={
            'required': 'You must agree to the terms to register.'
        }
    )

    terms_message = """
    By creating an account, you agree to the <a href='/terms/' target='_blank' class='text-decoration-none'>Terms of Service</a>. 
    """


    def clean_password1(self):
        """
        Validate the password to ensure it meets complexity requirements:
        - At least 8 characters long
        - Includes uppercase and lowercase letters
        - Includes numbers
        - Includes special characters (@$!%*?&#)
        """
        password = self.cleaned_data.get('password1')
        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password) or not re.search(r'[@$!%*?&#]', password):
            raise ValidationError('Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.')
        return password


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            }),
        }
        labels = {
            'username': 'Username',
        }

# Form for user login and validating credentials
# TODO: Implement alternative authentication methods such as mobile SMS or Authenticator App.
# Consider integrating login options via Gmail or other email services.
class UserLoginForm(forms.Form):
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email or username'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    # Validate the provided credentials against the database
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError('Invalid login credentials')
        
        self.cleaned_data['user'] = user  # Store the authenticated user in cleaned_data
        return self.cleaned_data

# Verify TOTP code using their authenticator
class TOTPVerificationForm(forms.Form):
    code = forms.CharField(
        max_length=6, 
        label="",
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter TOTP code'}))

# Password Reset Form
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="",
        widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
        }))

# Simple form for handling deposits into user accounts
# TODO: Consider adding additional procedures or permission checks for making deposits.
class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter deposit amount'
        })
    )

    account_number = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    # Initialize the form with the user's accounts.
    # If only one account is found, set it as the default. If multiple accounts are found, provide a dropdown.
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            accounts = Account.objects.filter(user=user)
            
            if accounts.count() == 1:
                self.fields['account_number'].initial = accounts.first().account_number
                self.fields['account_number'].widget = forms.TextInput(attrs={
                    'class': 'form-control-plaintext',
                    'readonly': 'readonly'
                })
            elif accounts.count() > 1:
                self.fields['account_number'] = forms.ChoiceField(
                    choices=[(account.account_number, account.account_number) for account in accounts],
                    widget=forms.Select(attrs={
                        'class': 'form-control'
                    })
                )
            else:
                raise forms.ValidationError("User has no account associated.")

    # Validate the provided account number
    def clean_account_number(self):
        account_number = self.cleaned_data.get('account_number')
        if not Account.objects.filter(account_number=account_number).exists():
            raise forms.ValidationError("Account number does not exist.")
        return account_number
    
# Simple form for handling withdrawals from user accounts
# TODO: Consider adding additional procedures or permission checks for withdrawing funds.
class WithdrawalForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter withdrawal amount'
        })
    )

    account_number = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    # Initialize the form with the user's accounts.
    # If only one account is found, set it as the default. If multiple accounts are found, provide a dropdown.
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            accounts = Account.objects.filter(user=user)

            if accounts.count() == 1:
                self.fields['account_number'].initial = accounts.first().account_number
                self.fields['account_number'].widget = forms.TextInput(attrs={
                    'class': 'form-control-plaintext',
                    'readonly': 'readonly'
                })
            elif accounts.count() > 1:
                self.fields['account_number'] = forms.ChoiceField(
                    choices=[(account.account_number, account.account_number) for account in accounts],
                    widget=forms.Select(attrs={
                        'class': 'form-control'
                    })
                )
            else:
                raise forms.ValidationError("User has no account associated.")

    # Validate the provided account number and ensure sufficient funds for withdrawal
    def clean_account_number(self):
        account_number = self.cleaned_data.get('account_number')
        account = Account.objects.filter(account_number=account_number).first()
        if not account:
            raise forms.ValidationError("Account number does not exist.")
        if account and account.balance < self.cleaned_data.get('amount'):
            raise forms.ValidationError("Insufficient funds.")
        return account_number
