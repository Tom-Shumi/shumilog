from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.urls import reverse_lazy
from urllib.parse import urlencode


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            redirect_url = reverse_lazy('common:index')
            parameters = urlencode({'pm': 1})
            url = f'{redirect_url}?{parameters}'
            return redirect(url)
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'account/signup.html', context)
