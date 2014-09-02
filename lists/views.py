from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items':items})

def new_list(request):
    list_ = List.objects.create() # creates a new list
    Item.objects.create(text=request.POST['item_text'], list=list_) # adds the text the user entered to the list
    return redirect('/lists/the-only-list-in-the-world/') # redirects to the list page