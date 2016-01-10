from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from lists.models import Item, List
from lists.forms import ItemForm

# Create your views here.
def home_page(request):
    #form is passed as a dictionary key
    # to be used in the template, OHH
    return render(request, 'home.html', {'form': ItemForm()})

# handle post here too
def view_list(request, list_id):
    #only pass items from the list with the given id
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            # different from how the item was created down there
            item = Item(text=request.POST['text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            # form wasnt being passed after this error
            error = "You can't have an empty list item"

    return render(request, 'list.html', {'list': list_, 'error': error})

def new_list(request):
    #creating an object
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    #rm hardcoded url
    return redirect(list_)

