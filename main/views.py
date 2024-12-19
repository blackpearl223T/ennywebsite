from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import ToDoList, Item
from .forms import CreateNewList
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
@login_required(login_url='/login/')
def index(response, id):
    ls = ToDoList.objects.get(id=id)
    if ls in response.user.todolist.all():
        if response.method == "POST":
            print(response.POST)
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()
                
            elif response.POST.get("newItem"):
                txt = response.POST.get("new")

                if len(txt) > 2:
                    ls.item_set.create(text=txt, complete=False)

                else:
                    print("invalid input")

        return render(response, "main/list.html", {"ls":ls})
    return render(response, "main/view.html",  {})
@login_required(login_url='/login/')
def home(response):
    return render(response, "main/home.html",  {})

@login_required(login_url='/login/')
def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            response.user.todolist.add(t)
        return HttpResponseRedirect("/%i" %t.id)
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form":form})

@login_required(login_url='/login/')
def view(response):
    return render(response, "main/view.html",  {})

def login_view(request):
    print("Login view hit! ----1")  # Debug print
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print("Form errors:", form.errors)  # Add this to see validation errors
        if form.is_valid():
            print("here")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username, password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                print("Authentication failed")  # Add this debug print
                form.add_error(None, "Invalid username or password")  # Add error message
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})