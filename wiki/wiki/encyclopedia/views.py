from markdown2 import markdown
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import os

from . import util

def index(request):
    if request.method == "POST":
        if 'q' in request.POST:
            return handle_search(request)
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def handle_search(request):
    query = request.POST['q']
    search_result = entry_exists(query)
    
    if search_result:
        return redirect('entry', search_result[0])
    
    return redirect('results', query)

def entry_view(request, entry_name):
    if request.method == "POST":
        if 'q' in request.POST:
            return handle_search(request)
    
    markdown_source = util.get_entry(entry_name)
    
    if markdown_source is not None:
        html = markdown(markdown_source)
        return render(request, "encyclopedia/entry_page.html", {
            "entry_name": entry_name,
            "html": html
        })
    
    return render(request, "encyclopedia/entry_page.html", {
        "error_message": "The requested entry does not exist."
    })

def results_view(request, query):
    if request.method == "POST":
        if 'q' in request.POST:
            return handle_search(request)
    
    query = query.lower()
    search_results = [entry for entry in util.list_entries() if query in entry.lower()]
    return render(request, "encyclopedia/results.html", {
        "search_results": search_results,
    })

def create_view(request):
    if request.method == "POST":
        if 'q' in request.POST:
            return handle_search(request)
        elif 'title' in request.POST:
            title = request.POST['title']
            if not title:
                return render(request, "encyclopedia/create.html", {
                        "message": "Please enter the title of the page."
                    })

            content = request.POST['content']
            
            search_results = entry_exists(title)
            if search_results:
                return render(request, "encyclopedia/create.html", {
                    "message": f"The entered item already exists in the wiki: ",
                    "entry_name": search_results[0]
                })
            
            write_markdown(title, content)
            return redirect('entry', title)
            
    return render(request, "encyclopedia/create.html")

def write_markdown(title, content):
    html = f"# {title}\n\n" + content
    file_directory = os.path.join(settings.BASE_DIR, "entries", f"{title}.md")

    with open(file_directory, "w") as new_page:
        new_page.write(html)

def entry_exists(query):
    return [entry for entry in util.list_entries() if query.lower() == entry.lower()]