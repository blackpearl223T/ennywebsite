from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        print("Form submitted")  # Debug print
        if form.is_valid():
            print("Form is valid")  # Debug print
            user = form.save()
            print(f"User created: {user.username}")  # Debug print
            login(request, user)
            return redirect("/home")
        else:
            print("Form errors:", form.errors)  # Debug print
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form})