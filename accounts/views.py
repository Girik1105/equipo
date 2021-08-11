from django.shortcuts import render, redirect

from . import models, forms

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from allauth.account.views import SignupView

class AccountSignupView(SignupView):
    def form_valid(self, form):
        if form.is_valid():
            form.save(self.request)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(self.request, user)
            return redirect('edit-user-profile')

account_signup_view = AccountSignupView.as_view()

# Create your views here.
@login_required
def profile_edit_view(request):
    profile = request.user.profile
    form = forms.profile_form(instance=profile)

    if request.method == 'POST':
        form = forms.profile_form(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('dashboard:index')

    context = {'form': form}
    return render(request, 'landing/accounts/profile_edit.html', context)