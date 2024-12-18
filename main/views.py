from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(response, id):
    try:

        ls = ToDoList.objects.get(id=id)
    except ToDoList.DoesNotExist:
        return render (response, "main/error.html", {"message": "List not found"})

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

@login_required(login_url='/login')
def home(response):
    return render(response, "register/home.html",  {})

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


def view(response):
     return render(response, "main/view.html",  {})
