from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied, ValidationError

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser to include additional fields:
    - is_verified: Indicates if the user has verified their email address.
    - totp_key: Stores the TOTP secret key used for Two-Factor Authentication (2FA).
    - is_2fa_setup_completed: Indicates if the user has completed the 2FA setup and if True, users will have complete access to their accounts and make transactions.
    """
    is_verified = models.BooleanField(default=False, help_text=_("Indicates if the user has verified their email address."))
    totp_key = models.CharField(max_length=32, blank=True, null=True, help_text=_("TOTP secret key for 2FA."))
    is_2fa_setup_completed = models.BooleanField(default=False, help_text=_("Indicates if the user has completed 2FA setup."))

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    """
    User profile model storing additional details about the user:
    - phone_number: The user's phone number.
    - address: The user's address.

    This profile is created via signals when a new user registers.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def can_access_profile(self):
        """
        Check if the user can access or modify their profile.
        """
        return self.user.is_verified and self.user.is_2fa_verified

class Account(models.Model):
    """
    Simplified model representing a user's account:
    - account_number: Unique identifier for the account.
    - account_type: Type of account (e.g., Savings or Checking).
    - balance: Current balance of the account.
    - status: Current status of the account (e.g., Active or Closed).
    """
    SAVINGS = 'savings'
    CHECKING = 'checking'
    ACCOUNT_TYPE_CHOICES = [
        (SAVINGS, 'Savings'),
        (CHECKING, 'Checking'),
    ]

    ACTIVE = 'active'
    CLOSED = 'closed'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES) 
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_type.capitalize()} - {self.account_number}"

    def deposit(self, amount):
        """Method to handle deposits."""
        if amount <= 0:
            raise ValidationError("Deposit amount must be positive.")
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        """Method to handle withdrawals."""
        if amount <= 0:
            raise ValidationError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValidationError("Insufficient funds.")
        self.balance -= amount
        self.save()

    def transfer(self, target_account, amount):
        """Method to transfer funds from this account to another account."""
        if amount <= 0:
            raise ValidationError("Transfer amount must be positive.")
        if self.status != self.ACTIVE or target_account.status != self.ACTIVE:
            raise ValidationError("Both accounts must be active to perform a transfer.")
        if amount > self.balance:
            raise ValidationError("Insufficient funds.")

        # Withdraw from this account and deposit into the target account
        self.withdraw(amount)
        target_account.deposit(amount)

        # Create transaction records for both accounts
        Transaction.objects.create(account=self, amount=amount, transaction_type=Transaction.WITHDRAWAL, description=f'Transfer to {target_account.account_number}')
        Transaction.objects.create(account=target_account, amount=amount, transaction_type=Transaction.DEPOSIT, description=f'Transfer from {self.account_number}')

class Transaction(models.Model):
    """
    Model representing a financial transaction within an account:
    - account: The account associated with the transaction.
    - amount: The amount involved in the transaction.
    - transaction_type: The type of transaction (Deposit, Withdrawal or Transfer).
    - description: Additional information about the transaction.
    - date: The date and time when the transaction occurred.
    """
    DEPOSIT = 'Deposit'
    WITHDRAWAL = 'Withdrawal'
    TRANSFER = 'Transfer'

    TRANSACTION_TYPE_CHOICES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
        (TRANSFER, 'Transfer'),

    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.date}"
    
    @classmethod
    def log_transfer(cls, from_account, to_account, amount):
        """Logs the transfer between two accounts as two transactions."""
        cls.objects.create(
            account=from_account,
            amount=amount,
            transaction_type=cls.TRANSFER,
            description=f"Transfer to {to_account.account_number}"
        )
        cls.objects.create(
            account=to_account,
            amount=amount,
            transaction_type=cls.TRANSFER,
            description=f"Transfer from {from_account.account_number}"
        )