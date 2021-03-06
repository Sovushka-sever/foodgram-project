from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    template_name = 'reg.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            return render(request, 'reg.html', {'form': form})

        user = form.save()
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        login(request, user)
        return redirect('index')
