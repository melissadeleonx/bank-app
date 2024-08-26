from django.urls import path
from . import views

# url paths according to their purpose
urlpatterns = [
    # Homepage
    path('', views.index, name='index'),

    # User Authentication
    path('register/', views.register, name='register'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('verification-success/', views.verification_success, name='verification_success'),

    path('two-factor-setup/', views.two_factor_setup, name='two_factor_setup'),
    path('ttop-verify/', views.ttop_verify, name='ttop_verify'),


    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('google-login/', views.google_login, name='google_login'),

    path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),

    

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Account Management
    # path('account/', views.account_overview, name='account_overview'),
    # path('profile/', views.profile, name='profile'),
    # path('settings/', views.settings, name='settings'),

    # Banking Transactions
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    # path('transfer/', views.transfer, name='transfer'),
    path('transactions/', views.transaction_history, name='transaction_history'),

    # Bill Payments
    # path('pay-bills/', views.pay_bills, name='pay_bills'),

    # Support
    # path('support/', views.support, name='support'),

    # Confirmation Pages
    path('registration-confirmation/', views.registration_confirmation, name='registration_confirmation'),


] 