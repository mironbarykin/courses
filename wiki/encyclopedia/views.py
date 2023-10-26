from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
import markdown2
import random as randomiser


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, name):
    page = util.get_entry(name)
    if page is not None:
        return render(request, "encyclopedia/wiki.html", {
            "page_title": name,
            "page_container": markdown2.markdown(page)
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error_description": "You are trying to reach a non-existent page!" 
        })

def edit(request, name):
    page = util.get_entry(name)
    if request.method == "POST":
        content = request.POST.get("updated_page_content")
        util.save_entry(name, content)
        return HttpResponseRedirect(reverse('wiki', args=[name]))
    
    if page is not None:
        return render(request, "encyclopedia/edit.html", {
            "page_title": name,
            "page_container": page
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error_description": "You are trying to reach a non-existent page!" 
        })

def add(request):
    if request.method == "POST":
        title = request.POST.get("new_page_title")
        content = request.POST.get("new_page_content")
        
        if (title.upper() or title.lower() or title.capitalize()) in util.list_entries():
            return render(request, "encyclopedia/error.html", {
            "error_description": "You are trying to add page with title that already exists!" 
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('wiki', args=[title]))
    return render(request, "encyclopedia/add.html")

def search(request):
    if request.method == "POST":
        question = request.POST.get("q")
        if util.get_entry(question) is not None:
            return HttpResponseRedirect(reverse('wiki', args=[question]))
        else:
            return render(request, "encyclopedia/search.html", {
                "entries": [i for i in util.list_entries() if question.lower() in i.lower()]
            })
    return HttpResponseRedirect(reverse('index'))

def random(request):
    name = randomiser.choice(util.list_entries())
    return HttpResponseRedirect(reverse('wiki', args=[name]))