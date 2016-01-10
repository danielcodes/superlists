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

    # now the error only displays depending on the form constructor
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})


# before, create list, get item from post and validate
# after, pass POST data to form constructor, if ok, create list and item
def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})

