# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from.models import Transaction, CustomUser
from.forms import BalanceUpdateForm
from django.shortcuts import render,redirect

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def dashboard(request):
    user = request.user
    if user.is_winner and not user.winner_bonus_claimed:
    # if user.is_winner:
        winner_status = "Congratulations you are the winner!"
        user.balance += 100000
        user.winner_bonus_claimed = True
        Transaction.objects.create(user=user, transaction_type='deposit', amount=100000)
        user.save()
    else:
        winner_status = "You are not the winner."
    return render(request, 'dashboard.html', {'winner_status': winner_status})


@login_required
def update_balance(request):
    if request.method == 'POST':
       form = BalanceUpdateForm(request.POST, instance=request.user)
       if form.is_valid():
         form.save()
         return redirect('home')
    else:
       form = BalanceUpdateForm(instance=request.user)
    return render(request, 'account_update.html', {'form': form})

