from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, Account, Transaction

# Dedicated admin configuration for each models to search, filter and manage records easily
class UserAdmin(BaseUserAdmin):
    model = User

    # Fields for displaying the User model
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_verified', 'is_2fa_setup_completed')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login', 'totp_key') 
    ordering = ('-date_joined',)
    filter_horizontal = ()

    # Fields to include in the User detail view
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('2FA and Verification', {'fields': ('is_verified', 'is_2fa_setup_completed', 'totp_key')}),
    )

    # Fields to be included in the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

class AccountAdmin(admin.ModelAdmin):
    # Fields displaying the Account model
    list_display = ('user', 'account_number', 'account_type', 'balance', 'status', 'created_at', 'updated_at')
    search_fields = ('account_number', 'user__username')
    list_filter = ('account_type', 'status', 'created_at')

class TransactionAdmin(admin.ModelAdmin):
    # Fields displaying the Transaction model
    list_display = ('account', 'transaction_type', 'amount', 'date', 'description')
    search_fields = ('account__account_number', 'transaction_type', 'amount')
    list_filter = ('transaction_type', 'date', 'account__account_type')
    ordering = ('-date',)

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
