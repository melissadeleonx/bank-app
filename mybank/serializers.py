# bank/serializers.py
# #TODO in order to use django RESTapi and customers can do CRUD within the dashboard

from rest_framework import serializers
from .models import Account, Transaction

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id', 
            'user', 
            'account_number', 
            'account_type', 
            'balance', 
            'created_at', 
            'updated_at', 
            'status', 
            'interest_rate'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'balance']

    def validate_deposit(self, value):
        # Deposit amount should be positive
        if value <= 0:
            raise serializers.ValidationError("Deposit amount must be positive.")
        return value

    def validate_withdraw(self, value):
        # Withdrawal should not be more than the balance
        if value <= 0:
            raise serializers.ValidationError("Withdrawal amount must be positive.")
        if value > self.instance.balance:
            raise serializers.ValidationError("Insufficient funds.")
        return value
    
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'amount', 'transaction_type', 'description', 'date']
        read_only_fields = ['date'] 

    def validate(self, data):
        # Add custom validation if needed
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        return data