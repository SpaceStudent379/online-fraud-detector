# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import CustomUser,Transaction

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = (
            "username",
            "email",
            "balance",
            "bank_info",
        )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "balance",
            "bank_info",
        )


class RandomUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('user')
        )

# class BalanceUpdateForm(forms.ModelForm):
#    class Meta:
#       model = CustomUser
#       fields = ['balance']
class BalanceUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['balance']

    def save(self, commit=True):
        instance = super().save(commit=False)
        old_balance = instance.__class__.objects.get(pk=instance.pk).balance
        new_balance = instance.balance
        amount = new_balance - old_balance
        transaction_type = 'deposit' if amount > 0 else 'withdrawal'
        Transaction.objects.create(user=instance, transaction_type=transaction_type, amount=abs(amount))
        if commit:
            instance.save()
        return instance