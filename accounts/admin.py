# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
import random
from.models import Transaction
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [ "email", "username","balance", "is_staff", "is_winner", ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("balance", "is_winner", "bank_info", )}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("balance", "is_winner", "bank_info",)}),)
    actions = ['generate_winner']

    def generate_winner(self, request, queryset):
        users = queryset.filter(is_staff=False)
        winner = random.choice(users)
        winner.is_winner = True
        winner.save()
        self.message_user(request, f"Winner generated: {winner.username}")

    generate_winner.short_description = "Generate Winner"


admin.site.register(CustomUser, CustomUserAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'amount', 'timestamp']
    list_filter = ['transaction_type']
    search_fields = ['user__username', 'amount']


admin.site.register(Transaction, TransactionAdmin)
